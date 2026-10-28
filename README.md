# Biomedical Researcher (working notes)

These notes started from Prof. David Stuckler's YouTube channel and his `fasttrack-topic-validator` skill. I changed a lot of it with my own thinking (and some help from Claude).

A typical research workflow looks like this:

Brainstorming a topic → Preliminary literature review → Identifying a research gap → Formulating the research question and hypothesis → ...

The journey keeps going after that, but for now this plugin covers only the first part: **brainstorming** and **identifying a research gap**.

Scope: biomedical and life sciences. That's why the connectors are PubMed, bioRxiv, ClinicalTrials.gov, Synapse.org and Consensus.

Who it's for:

- **Mainly, people starting from scratch.** No topic, no nearest papers, no data or lab. Just a field they care about. This is the main route, and it starts with gap mining.
- **Second, people who already have an idea.** They have a rough topic and maybe a few papers, and want it pressure-tested. This route starts with mining for ideas.

The one thing the plugin can't supply is the field of interest. That has to come from the user.
<img width="1920" height="1032" alt="Obsidian_gQpdPYchbF" src="https://github.com/user-attachments/assets/b0c22529-c4c9-427b-b90e-4aa3d59b7fd9" />

<hr style="border: 1px solid #D6BCFA">

## Install and setup

1. Install the plugin from inside Claude Code:
   ```
   /plugin marketplace add Fyn2a/biomedical-researcher
   /plugin install biomedical-researcher@biomedical-researcher
   ```
   Or, from a local clone, run `claude --plugin-dir ./biomedical-researcher`.
2. When it's enabled, Claude Code asks for the **Obsidian vault** folder and a **notes folder** inside it (default `Research`). Change them later in `/config`.
3. Run `/mcp` and sign in to **Consensus** and **Synapse.org**. PubMed, bioRxiv and ClinicalTrials.gov need no sign-in.
4. The graph check hook needs `python3` on your machine.

What's inside:

```
biomedical-researcher/
├── .claude-plugin/
│   ├── plugin.json                 # name, version, vault settings
│   └── marketplace.json            # lets /plugin install it straight from GitHub
├── .mcp.json                       # PubMed, Consensus, bioRxiv, ClinicalTrials.gov, Synapse.org
├── skills/
│   ├── gap-mining/                 # main entry point (starting from scratch)
│   ├── mining-for-ideas/           # topic validation (already have an idea)
│   └── obsidian-graph-sync/        # link rules, templates, change log
├── hooks/
│   ├── hooks.json                  # graph check before Claude finishes a turn that touched the vault
│   └── check-links.py
└── README.md
```

<hr style="border: 1px solid #D6BCFA">

## Thought process

Why build this instead of just using the Prof's skill?

- His skill depends on his own connector (FastTrack Literature). It has tools like `run_duplication_test`, `check_gap_saturation`, `map_topic_debate` and `get_paper`. I don't have access to it, so I need to rebuild those same checks on top of connectors I can actually use.
- The method is solid and I want to keep it: Convergence → Test and refine → Human validation. What I'm replacing is the plumbing underneath.
- The core rule stays. Claude checks the researcher's thinking, it doesn't replace it. The gap and the question have to come from me (or whoever uses the plugin). Claude retrieves and pressure-tests.
- Hallucinated citations are the biggest risk with AI in research. So every paper, count or citation number has to come from a live connector with a link I can open. Nothing from memory.
- The Prof's skill assumes you already have a topic and nearest papers. Most beginners don't, and that's who I'm building this for. So the plugin needs a way in before validation: start from a field, find what the reviews say is missing, see what data exists, and only then write a topic.
- I want the output to stick around. Instead of a chat reply that disappears, results go into my Obsidian vault as linked notes, so the knowledge graph grows each time I run the workflow.

What I'm adding on top of the Prof's skill:

- My own connector stack (below) instead of FastTrack Literature.
- A separate gap-mining skill that reads limitations and future-work sections of review papers. It's the entry point for anyone starting from scratch. It finds candidates, but you still pick.
- Synapse.org, so someone with no data or lab can see what open datasets already exist.
- Obsidian output that keeps the graph view current every time a note changes.

<hr style="border: 1px solid #D6BCFA">

## Brainstorming

A skill called **"Mining for ideas"** that uses Claude connectors for the literature side. It follows the same three phases as the Prof's skill.

Before anything runs, the skill asks one question: is this for a **systematic review** or **another kind of project** (empirical study, thesis, qualitative work)? The tests differ, so running the wrong track wastes time.

### Topic Neighborhood

Find the area where three things meet: **feasibility × passion × debate**. All three are needed. A feasible topic you don't care about stalls a few months in. A topic you love with no debate won't publish.

- The user brings a rough topic (2 to 3 sentences), their interest level, timeframe and resources.
- Claude searches the connectors to check whether the debate is live: conflicting findings, recent calls for more research, emerging evidence.
- If the user only brings a broad field and can't name a neighborhood yet, they stay here. No amount of searching fixes a topic that hasn't converged.

### Validating Topic

The tests, run in order:

1. **Duplication test (both tracks).** Find the 1 to 3 published papers closest to the idea, then the user states what they add beyond them. "Nobody did this in my country" isn't a gap on its own. For systematic reviews, the rivals that matter are existing reviews, so search with "systematic review" in the query too. If a paper's method can't be confirmed from the abstract, flag it as "possible rival, method unverified" and tell the user to open it.
2. **Feasibility test.**
   - Systematic review: roughly 5+ original studies suggests it's viable, 8 to 10 for the final question. Fewer means too narrow, hundreds means too broad.
   - General: access to data or participants, skills, fit within the timeframe. Search Synapse.org for existing datasets and note whether access is open or controlled, since a controlled-access approval can eat months of the timeframe.
3. **Impact test (general track).** Are the nearest papers getting cited, or sitting at zero? Is the debate showing up in strong journals?
4. **Crystallise the question.** Use PICO (Population, Intervention/Exposure, Comparison, Outcome). Claude points out the weak element. The user rewrites the question themselves.
5. **Grandmother rule.** Can the topic be explained in 2 to 3 plain sentences to someone outside the field? If not, it isn't ready.

A thin search result doesn't automatically mean the idea is original. It often means the search used the wrong vocabulary. Take terms from the closest titles and search again before calling it a gap.

### Human Vetting

This step belongs to people, not Claude. The plugin's verdict is a pressure test, not an approval.

- Take the topic to a supervisor, a mentor or a research group.
- A topic the supervisor won't approve isn't validated, however well it scored.
- Every run of the skill ends by pointing the user here.

Verdict format (borrowed from the Prof): **Green light**, **Adjust before proceeding**, or **Back to the worksheet**. Max 3 issues, one next step.

<hr style="border: 1px solid #D6BCFA">

## Connectors

The point of connectors is to avoid hallucination. Claude only cites what it actually retrieved.

Planned: Consensus, PubMed, bioRxiv, ClinicalTrials.gov and Synapse.org.

Synapse.org (Sage Bionetworks) hosts shared biomedical datasets. It answers a question the others can't: is there data I can actually get for this topic? That makes it the main tool for the general track's Feasibility test.

How each one replaces a FastTrack tool:

| FastTrack tool | My replacement |
|---|---|
| `run_duplication_test` | Consensus + PubMed search for nearest papers and existing reviews |
| `check_gap_saturation` | PubMed result counts, ClinicalTrials.gov for ongoing/registered studies |
| `map_topic_debate` | Consensus (agreement/disagreement across findings), bioRxiv for emerging work |
| `get_paper` (citations) | Google Scholar, checked manually by the user |
| (no FastTrack equivalent) | Synapse.org for data availability and access conditions |

### Consensus & PubMed

| Connector | Can Claude analyze the full text of paid papers? | Can YOU download the full paid PDF for free? | Best used for |
|---|---|---|---|
| **Consensus MCP** | Yes, through publisher data partnerships | No, links go to the publisher's paywall | Getting insight from paid papers without buying them |
| **PubMed** | No, usually abstract only for paid papers | No, paid papers stay locked | Free, open-access medical and life science deep dives |

I rely on Consensus for exact, forensic searches. Google Scholar stays manual on purpose: I use it myself to filter for highly cited papers, follow the related-papers loop, and check citation counts for the Impact test. Claude asks me for those numbers instead of guessing them.

<hr style="border: 1px solid #D6BCFA">

## Research Gaps

The usual way to find gaps: read review papers in your field and look at the discussion section (sometimes the introduction). That's where authors mention limitations and suggestions for future research. A researcher normally reads 5 to 10 papers, pulls out the gaps, filters them into good and bad, and ends with a shortlist.

### Gap mining (separate skill)

This is its own skill, not part of "Mining for ideas". It's the main entry point of the plugin. The only input it needs is a field of interest and why the user cares about it. It can also run after validation, when a topic needs a sharper gap.

1. Search PubMed and Consensus for 5 to 10 recent review papers in the field. Check bioRxiv for newer preprints that may already be closing a gap.
2. Pull the limitations and future-research parts from each one, with the source linked.
3. Group repeated gaps. A gap named by several reviews is a stronger lead than one mentioned once.
4. Check each candidate against ClinicalTrials.gov to see if a registered trial is already working on it, and against Synapse.org to see if data exists to study it.
5. Sort candidates into good and bad. Good: the field is actively arguing about it. Bad: a geographic reshuffle, already answered, or only mentioned in passing.

6. Check every item against its source before showing the shortlist. Anything without an openable link gets cut.

The output is a shortlist of leads, each with its sources. For a beginner, the reviews it found double as a first reading list and, later, as candidate nearest papers. Reading them and choosing the gap is still the researcher's job. The chosen gap then goes into "Mining for ideas" for validation.

<hr style="border: 1px solid #D6BCFA">

## Output formats

The plugin is meant for Claude Code (CLI), and its main output is the Obsidian graph view. Obsidian builds the graph from `[[wikilinks]]` between notes, so keeping the graph correct means keeping the links correct. Every time the plugin touches the vault, in any way, the graph has to stay accurate.

Rules for every add, edit, rename or delete:

- **Add:** a new note is never left orphaned. It links to at least one existing note (its topic, paper or gap) and that note links back.
- **Edit:** if a note's content changes what it connects to (a gap is dropped, a paper turns out to be a rival), the links change too, not just the text.
- **Rename:** update every `[[wikilink]]` that pointed to the old name, so no link breaks.
- **Delete:** remove links pointing to the deleted note so the graph doesn't show ghost nodes.
- **Tags in frontmatter** (`topic`, `paper`, `gap`, `review`, `preprint`, `trial`, `dataset`) so the graph can be filtered and coloured by type.
- **Change log:** each run appends a short entry to a log note listing what was added, edited or removed, linked to the notes it touched.

Note types:

- Topic note: verdict, track, phase.
- Paper note: link, type (review, primary study, preprint, trial, dataset), which test it came from.
- Gap note: linked to every paper that mentions it.

Claude needs access to the working vault, so the vault path is set when the plugin is installed.

<hr style="border: 1px solid #D6BCFA">

## Ethical lens

The human has to stay in the loop, because the goal is to *become* a researcher, not to outsource being one. Two rules run through every skill in the plugin:

- **Verify output.** Every paper, number or claim comes with a source the user can open and check. No source, no claim.
- **Disclose AI use.** Each Obsidian note records which parts came from a connector search and which came from the user, so disclosure is easy when writing up.

Claude never generates the gap, the topic or the research question. It finds evidence and points at weak spots. This matters most for beginners. Starting from scratch is exactly when it's tempting to let Claude pick, and exactly when picking yourself teaches you the most.

<hr style="border: 1px solid #D6BCFA">

## Typical usage

### Case 1: Starting from scratch (main route)

You have a field you care about and nothing else.

1. **Run gap mining on the field.**
   `/biomedical-researcher:gap-mining I'm starting from scratch. My field of interest is [field] because [why I care]. Find recent reviews and candidate gaps, and show what open data exists on Synapse.org.`
   The vault gets a topic note holding the field, plus paper notes (reviews, trials, datasets) and gap notes, all linked.
2. **Read.** Open the reviews behind the 2 or 3 gaps that interest you most. This step is yours and can take a few days.
3. **Write the topic yourself.** 2 to 3 sentences, built on one gap. The reviews you read become your nearest papers.
4. **Validate it.**
   `/biomedical-researcher:mining-for-ideas Topic: [my 2–3 sentences]. It's for [a systematic review / another kind of project]. Nearest papers: [from step 2]. Timeframe: [X]. Interest level: [honest rating].`
5. **Fix and repeat.** If the verdict is "adjust" or "back to the worksheet", fix the named issue and run it again.
6. **Take it to a human.** On a green light, bring the topic note to your supervisor or mentor.

### Case 2: Already have an idea

You have a rough topic and maybe a few papers.

1. **Validate straight away.**
   `/biomedical-researcher:mining-for-ideas Topic: [my 2–3 sentences]. It's for [a systematic review / another kind of project]. Timeframe: [X]. Resources: [data, lab, skills]. Interest level: [honest rating].`
2. **Give the comparison.**
   `My nearest papers are [1–3 titles or links], and my idea differs because [difference]. The live debate is [what's being argued]. Run the validation.`
3. **Sharpen the gap if needed.** If the duplication test finds close rivals, run `/biomedical-researcher:gap-mining` on your topic to find a sharper angle, then validate again.
4. **Take it to a human.** On a green light, bring the topic note to your supervisor or mentor.

Both routes end the same way: a topic note in the graph, linked to its papers, gaps and datasets, and a human conversation as the next step.
