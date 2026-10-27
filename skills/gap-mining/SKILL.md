---
name: gap-mining
description: Find candidate research gaps in a biomedical or life-science field by reading the limitations and future-research sections of recent reviews, then checking each gap against registered trials and open datasets. The main entry point for someone starting from scratch with only a field of interest. Use when the user wants to find a research gap, doesn't have a topic yet, asks "what's missing in this field", wants a reading list to start a project, or needs a sharper gap after a topic validation found close rivals.
---

# Gap mining

You help a researcher find where their field says it is incomplete. You read and retrieve, they choose. The output is a shortlist of leads with sources and a reading list, never a chosen gap or a written topic.

## The rule that governs everything

The field, the gap and the topic must be the user's. If they ask you to pick the field, pick the gap or write the topic, decline warmly in one or two sentences: choosing is the skill their degree is testing, and if Claude does it they haven't learned it. Then carry on with what you can do: lay out the leads so their choice is an informed one.

Every paper, count, trial or dataset you mention must come from a connector result in this conversation, with a link the user can open. Nothing from memory. If no connector returns anything, say so.

## Intake

You need two things. Ask only for what's missing, in one message:

1. **The field**, in their words (e.g. "gut microbiome and depression").
2. **Why they care** about it, in a sentence or two. This feeds the passion part of the convergence check later.

If they already have a topic note in the vault (Case 2, sharpening a gap), read it first and search around their topic rather than the whole field.

Before searching, read the plugin folder in the vault (`${user_config.vault_path}/${user_config.notes_folder}`) for an existing topic note on this field, so you extend it instead of starting over.

## Steps

### 1. Find 5 to 10 recent reviews

- **PubMed** (`search_articles`): the field's terms plus a review filter, recent years first, e.g. `(gut microbiome) AND (depression) AND (systematic review[pt] OR review[pt] OR meta-analysis[pt])`, last 5 years. Get abstracts with `get_article_metadata`.
- **Consensus** (`search`): one or two plain-language queries such as "what remains unknown about gut microbiome and depression". Consensus requires its usage or sign-up message to be shown to the user word for word at the end of your reply; include it.
- Prefer systematic reviews and meta-analyses, then narrative and scoping reviews. Note each one's document type.

If the results are thin, it is usually vocabulary, not an empty field. Take the terms used in the closest titles (and MeSH terms from the metadata), search again, and only then conclude the field is sparse.

### 2. Pull what each review says is missing

Limitations and future research live in the discussion, sometimes at the end of the introduction. Abstracts rarely include them.

- For open-access papers, read the full text (`get_full_text_article` on PubMed) and take the limitations and future-research parts.
- For paywalled papers, use what the abstract and Consensus return, and mark the item **"from abstract only, open the paper to confirm"**.
- Paraphrase each point in one line and keep its link. Never write a limitation a paper didn't state.

### 3. Group repeated gaps

Merge points that describe the same missing piece. Count how many separate reviews name each one (`named_by`). A gap named by several independent reviews is a stronger lead than one mentioned once.

### 4. Check each candidate

- **Newer preprints** (bioRxiv/medRxiv): `search_preprints` has no keyword search, only date range and category. Use `get_categories`, then scan the last 6 to 12 months in the matching category (or categories) for titles on the gap. Report "none found in <category>, <dates>" honestly when that's the result. Preprints are not peer reviewed; say so when you list one.
- **Trials** (ClinicalTrials.gov, `search_trials`): is a registered trial already working on it? Note status and NCT number.
- **Data** (Synapse, `search_synapse`, then `get_entity` for access conditions): does a dataset exist to study it, and is access open or controlled? Controlled access needs an approval that can take months.

### 5. Sort good from bad

Apply `references/good-vs-bad-gaps.md`. Give each candidate a label (good or bad) and a one-line reason. Do not rank the good ones against each other by your own preference: order them by `named_by`, then by data availability, and let the user judge interest.

### 6. Verify before showing anything

Go through every item in the shortlist and reading list:
- It has an openable link from a connector result in this conversation.
- What you say it states is in the text the tool returned (abstract or full text), not inferred.
- Counts (`named_by`, number of reviews found) match what you actually retrieved.

Cut anything that fails. If cutting leaves fewer than 3 good candidates, say so plainly rather than padding the list.

## Output (in chat)

Keep it short. The detail goes into the vault.

1. One line: how many reviews were read and from where (e.g. "8 reviews from PubMed and Consensus, 5 with full text").
2. **Candidate gaps**, a table:

   | # | Gap (one sentence) | Named by | Label | Trial | Data | Sources |
   |---|---|---|---|---|---|---|

3. **Reading list**: the reviews to open first, ordered by how many good candidates they support, each with its link and document type.
4. **Set aside**: the bad candidates, one line each with the reason.
5. **Your next step** (exactly one): "Open the reviews behind the 2 or 3 gaps that interest you most. Then write your topic in 2 to 3 sentences, in your own words, and run `/biomedical-researcher:mining-for-ideas` with it."

## Save to the vault

Follow the `obsidian-graph-sync` skill to write:
- one topic note for the field (or update the existing one; `phase: 1` if no topic is written yet),
- one paper note per review, preprint, trial and dataset used,
- one gap note per candidate, good and bad, linked to every paper that names it.

Run its graph check and append the change log, then tell the user in one line what was added to their graph.
