---
type: paper
tags: [paper, {{review | primary | preprint | trial | dataset}}]
doc_type: {{systematic review | meta-analysis | narrative review | scoping review | primary study | preprint | registered trial | dataset}}
title: "{{exact title as returned by the connector}}"
authors: "{{first author et al.}}"
year: {{YYYY}}
journal: "{{journal, preprint server, registry or Synapse project}}"
doi: "{{DOI}}"
pmid: "{{PMID}}"
nct: "{{NCT number, trials only}}"
synapse_id: "{{syn ID, datasets only}}"
access: {{open | controlled, datasets only}}
url: "{{openable link}}"
retrieved_from: {{PubMed | Consensus | bioRxiv | medRxiv | ClinicalTrials.gov | Synapse | user}}
retrieved: {{YYYY-MM-DD}}
found_by: [{{gap-mining | duplication test | feasibility test | debate check | impact test | user}}]
rival_status: {{systematic rival | differentiation | method unverified | not a review}}
citations: "{{only if the user gave a Google Scholar count, with the date}}"
---

# {{Title}}

[Open the source]({{url}})

## Retrieved

*From {{connector}} on {{YYYY-MM-DD}}. This is a summary for orientation, not a substitute for reading the paper.*

- **What it is:** {{one line: document type and question}}
- **Method (as stated in the record):** {{how it searched/screened, or "not described in the abstract, open it to check"}}
- **Limitations and future research named:** {{only what the record actually says, or "not in the abstract"}}

## From you

{{Empty until the user adds their own reading notes.}}

## Links

- Topic: {{[[Topic name]]}}
- Gaps it names: {{[[Gap - ...]]}}
