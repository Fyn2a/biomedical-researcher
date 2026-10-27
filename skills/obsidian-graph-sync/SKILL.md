---
name: obsidian-graph-sync
description: Write, edit, rename or delete research notes in the user's Obsidian vault so the graph view stays correct, then log every change. Use whenever gap-mining or mining-for-ideas saves results, or whenever the user asks to add, change, rename, move or remove a topic, paper, gap or dataset note in their research vault.
---

# Obsidian graph sync

Obsidian builds its graph view from `[[wikilinks]]` between notes. A note with no links floats alone, a link to a missing note shows a ghost node, and a link left after a change shows a connection that is no longer true. So every change to the vault is a change to the links, not only to the text.

Obsidian watches the vault folder, so the graph refreshes on its own as soon as a file changes on disk. Nothing needs restarting.

## Where notes live

- Vault: `${user_config.vault_path}`
- Plugin folder inside the vault: `${user_config.notes_folder}`

Only create, edit, rename or delete notes inside the plugin folder. The user's other notes are theirs: you may link to them, never change them.

```
<vault>/<notes folder>/
├── Topics/
├── Papers/        # reviews, primary studies, preprints, trials, datasets
├── Gaps/
└── Change log.md
```

Create the folders and the change log from the templates the first time they are needed.

## Note types and templates

Fill the templates in `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-graph-sync/templates/`. Replace every `{{placeholder}}`. Delete a line whose value you don't have, rather than guessing it.

| Note | Template | File name |
|---|---|---|
| Topic | `topic.md` | Short field or topic name, e.g. `Gut microbiome and depression` |
| Paper (any source) | `paper.md` | `First-author Year - Short title`, under 70 characters |
| Gap | `gap.md` | `Gap - short phrase`, e.g. `Gap - microbiome in adolescent depression` |
| Change log | `change-log.md` | `Change log` (one per plugin folder) |

A Case 1 user starts with only a field. Their topic note then holds just the field, with `phase: 1`. When they write their topic sentences, fill in the same note and rename it if they want. Never make a second topic note for the same field.

Datasets from Synapse are paper notes with `doc_type: dataset` and an `access` value (open or controlled).

File names can't contain `[ ] # ^ | \ / : * ? " < >`. Drop those characters.

## Before writing: look first

1. **Find existing notes.** Search the plugin folder for the same DOI, PMID, NCT number or Synapse ID before creating a paper note. If it exists, edit it (add the new `found_by`, link it to the new topic or gap). Never create a duplicate node.
2. **Find the topic note.** Every run belongs to one topic note. Reuse it if it exists.

## Link rules

**Add.** A new note is never left alone. Every paper and gap note links to its topic. Every gap links to each paper that names it. The other note links back, in its `Links` section, so the connection is visible from both sides.

**Edit.** If the meaning changes, the links change too:
- A gap is dropped: set `label: dropped`, keep its links to the papers that name it (that history is useful), and move its link in the topic note from `Candidate gaps` to `Dropped gaps`.
- A review turns out to be a duplication rival: set `rival_status`, and move its link in the topic note into `Rivals`.
- The user chooses a gap: set `chosen: true` on the gap and put it under `Chosen gap` in the topic note.

**Rename.** Search the whole vault for `[[Old name`, including `[[Old name|alias]]` and `[[Old name#heading]]`, and update every match, including links in the user's own notes (link text only, nothing else). Then rename the file with `mv`.

**Delete.** Only when the user asks. List every note that links to it, remove those links, then delete the file. Deleting a file is permanent, so confirm the list with the user first.

**Tags.** Every note has frontmatter `tags` (`topic`, `paper`, `gap`, plus `review`, `primary`, `preprint`, `trial` or `dataset` for papers). The user can colour the graph by tag. Tell them once, the first time the plugin folder is created: in Obsidian's graph view, open Groups and add `tag:#topic`, `tag:#gap`, `tag:#review`, `tag:#dataset` with different colours.

## Disclosure

Each note keeps what came from a connector apart from what came from the user:
- Retrieved content sits under `## Retrieved`, with the connector name and date.
- The user's own words (field, reasons, topic sentences, nearest papers they chose, their difference statement) sit under `## From you`.
- Never move Claude-written text into `## From you`.

This is what lets the user disclose AI use accurately later.

## After writing: check, then log

1. Run the graph check:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/hooks/check-links.py" --vault "${user_config.vault_path}" --folder "${user_config.notes_folder}"
   ```
   Fix every broken link and orphan it reports, then run it again until it passes. The plugin's Stop hook runs the same check before you finish a turn that touched the vault, as a safety net.
2. Append one entry to `Change log.md` using the entry format in `change-log.md`. Removed notes are listed as plain text, not links, because a link to a deleted note is a broken link.
3. Tell the user in one line what changed in their graph (e.g. "Added 1 topic, 7 papers, 4 gaps to your graph").
