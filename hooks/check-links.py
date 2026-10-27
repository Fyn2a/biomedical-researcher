#!/usr/bin/env python3
"""Check the plugin's Obsidian notes for broken wikilinks and orphan notes.

Three ways to run it:

  --mark  (PostToolUse hook, after Write/Edit)
      If the edited file is a note in the plugin's notes folder, leave a marker
      saying "this session changed the vault". Never blocks. Checking after each
      single write would be noise, because a run writes several linked notes
      and the links only resolve once all of them exist.

  --stop  (Stop hook, when Claude is about to end its turn)
      If the marker exists, check the whole notes folder once. On problems,
      print them to stderr and exit 2, so Claude fixes the links before it
      finishes. If the hook already fired once this turn, let Claude stop, so
      it can never loop.

  manual  (called by the obsidian-graph-sync skill)
      python3 check-links.py --vault /path/to/vault --folder Research

The vault path and notes folder come from the plugin settings
(CLAUDE_PLUGIN_OPTION_VAULT_PATH, CLAUDE_PLUGIN_OPTION_NOTES_FOLDER) unless
passed as arguments.

Only notes inside the notes folder are checked. Links in those notes may point
anywhere in the vault. Nothing outside the notes folder is ever reported, so the
user's own notes are left alone.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

WIKILINK = re.compile(r"!?\[\[([^\]\|#\^]+)(?:[#\^][^\]\|]*)?(?:\|[^\]]*)?\]\]")
CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
OBSIDIAN_COMMENT = re.compile(r"%%.*?%%", re.DOTALL)
# The change log links to everything it touched, so it doesn't count as a
# real connection when deciding whether a note is an orphan.
LOG_NAMES = {"change log", "change-log"}


def strip_code(text: str) -> str:
    for pattern in (CODE_BLOCK, HTML_COMMENT, OBSIDIAN_COMMENT, INLINE_CODE):
        text = pattern.sub("", text)
    return text


def build_index(vault: Path):
    """Map every linkable name in the vault to its files."""
    index = {}
    for path in vault.rglob("*"):
        if not path.is_file() or any(p.startswith(".") for p in path.relative_to(vault).parts):
            continue
        rel = path.relative_to(vault).as_posix()
        keys = {path.name.lower(), rel.lower()}
        if path.suffix.lower() == ".md":
            keys.add(path.stem.lower())
            keys.add(rel[:-3].lower())
        for k in keys:
            index.setdefault(k, set()).add(path)
    return index


def resolve(target: str, index):
    t = target.strip().replace("\\", "/").lower()
    return index.get(t) or index.get(t + ".md") or set()


def check(vault: Path, folder: str):
    notes_dir = (vault / folder) if folder else vault
    if not notes_dir.is_dir():
        return [], []
    index = build_index(vault)
    notes = [p for p in notes_dir.rglob("*.md")
             if not any(part.startswith(".") for part in p.relative_to(vault).parts)]

    broken = []
    linked = {}  # note -> set of real neighbours
    for note in notes:
        try:
            text = strip_code(note.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        for m in WIKILINK.finditer(text):
            target = m.group(1).strip()
            if not target:
                continue
            hits = resolve(target, index)
            if not hits:
                broken.append((note.relative_to(vault).as_posix(), target))
                continue
            if note.stem.lower() in LOG_NAMES:
                continue
            for hit in hits:
                if hit == note or hit.stem.lower() in LOG_NAMES:
                    continue
                linked.setdefault(note, set()).add(hit)
                linked.setdefault(hit, set()).add(note)

    orphans = [n.relative_to(vault).as_posix() for n in notes
               if n.stem.lower() not in LOG_NAMES and not linked.get(n)]
    return broken, orphans


def report(broken, orphans) -> str:
    lines = []
    if broken:
        lines.append("Broken wikilinks (target note doesn't exist):")
        lines += [f"  - {src} -> [[{tgt}]]" for src, tgt in broken]
    if orphans:
        lines.append("Orphan notes (no links in or out, invisible in the graph's connections):")
        lines += [f"  - {o}" for o in orphans]
    return "\n".join(lines)


def marker_path(session_id: str) -> Path:
    data = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(
        os.path.expanduser("~"), ".claude", "biomedical-researcher-data")
    safe = re.sub(r"[^A-Za-z0-9_-]", "-", session_id or "default")
    return Path(data) / f"vault-changed-{safe}"


def read_payload():
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--mark", action="store_true")
    mode.add_argument("--stop", action="store_true")
    ap.add_argument("--vault")
    ap.add_argument("--folder")
    args = ap.parse_args()

    vault = args.vault or os.environ.get("CLAUDE_PLUGIN_OPTION_VAULT_PATH", "")
    folder = args.folder if args.folder is not None else os.environ.get(
        "CLAUDE_PLUGIN_OPTION_NOTES_FOLDER", "Research")
    folder = folder.strip().strip("/")

    if args.mark:
        payload = read_payload()
        file_path = (payload.get("tool_input") or {}).get("file_path", "")
        if not vault or not file_path.lower().endswith(".md"):
            sys.exit(0)
        try:
            Path(file_path).resolve().relative_to((Path(vault) / folder).resolve())
        except (ValueError, OSError):
            sys.exit(0)  # not one of the plugin's notes
        try:
            m = marker_path(payload.get("session_id", ""))
            m.parent.mkdir(parents=True, exist_ok=True)
            m.touch()
        except OSError:
            pass
        sys.exit(0)

    if args.stop:
        payload = read_payload()
        m = marker_path(payload.get("session_id", ""))
        if not m.exists():
            sys.exit(0)  # this session didn't touch the vault
        if payload.get("stop_hook_active"):
            m.unlink(missing_ok=True)  # already asked once, don't loop
            sys.exit(0)
        if not vault or not Path(vault).is_dir():
            m.unlink(missing_ok=True)
            sys.exit(0)
        broken, orphans = check(Path(vault), folder)
        m.unlink(missing_ok=True)
        if not broken and not orphans:
            sys.exit(0)
        print("Obsidian graph check found problems in the notes written this turn. "
              "Fix the links, then append the fix to the change log "
              "(see the obsidian-graph-sync skill):\n" + report(broken, orphans),
              file=sys.stderr)
        sys.exit(2)

    if not vault or not Path(vault).is_dir():
        print("Vault path not set or not found. Set it in the plugin's settings (/config).")
        sys.exit(1)
    broken, orphans = check(Path(vault), folder)
    if not broken and not orphans:
        print("Graph check passed: no broken links, no orphan notes.")
        sys.exit(0)
    print(report(broken, orphans))
    sys.exit(1)


if __name__ == "__main__":
    main()
