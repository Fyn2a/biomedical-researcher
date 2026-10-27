# The tests

Run in order. Each test says which connector to use. Every result you report needs its link.

## Phase 1: Convergence (both tracks)

Feasibility × passion × debate. All three must be present.

- **Passion:** from what the user told you (interest level, why they care). A feasible topic they don't care about stalls a few months in.
- **Debate:** search Consensus with a plain-language question on the topic, and PubMed for recent reviews. Look for conflicting findings, low-certainty evidence, or explicit calls for more research. A topic with no debate won't publish.
- **Feasibility:** a first look only (time, resources). The full test is in Phase 2.

If the user can't name a neighbourhood where all three meet, they are in Phase 1. Verdict: back to the worksheet, and the next step is `/biomedical-researcher:gap-mining` or writing the topic sentences.

## Phase 2

### 1. Duplication test (both tracks)

The centrepiece: find the nearest published work and check the user's stated add over and above it.

- Start from the 1 to 3 nearest papers the user supplied. Then search PubMed (`search_articles`, `find_related_articles` on their nearest papers) and Consensus for others they may have missed.
- **Systematic review track:** the rivals that decide duplication are existing reviews, not primary studies. Search with a review filter (`systematic review[pt] OR meta-analysis[pt]`), then run one more pass with the words "systematic review" in the query before treating the lane as clear. Primary studies found along the way are feasibility and debate evidence, not rivals.
- **Grade reviews by method and question, never by label.** State the document type whenever you present one.
  - Searched and screened systematically, same question → **systematic rival**. Pushes the verdict towards pivot or narrow.
  - No systematic method (narrative overview, editorial, bibliometric map), or a clearly adjacent question → **differentiation evidence**. The user reads it and states their add. The lane stays open until they do.
  - Method not described in what the tool returned (many abstracts don't; some records have no abstract) → **possible rival, method unverified**. Never guess. Opening it becomes the user's named next step.
- **Check the user's difference.** Is it a real add, or "nobody has done this in my country"? A real gap is something the field is actively debating, not a geographic reshuffle.

### 2. Feasibility test

- **Systematic review track:** count original studies with PubMed (`search_articles`, report the total and the query used). Around 5 or more suggests a viable review, 8 to 10 for the final PICO question. Fewer: too narrow or too new. Hundreds: too broad. A thin count may be vocabulary: harvest terms and MeSH from the closest on-topic titles and rerun before reading thinness as originality. Check ClinicalTrials.gov for completed trials with results that would add to the pool.
- **General track:** execution. Access to data, participants or materials; the skills needed; fit within the timeframe. Search Synapse (`search_synapse`, then `get_entity`) for datasets and state whether access is open or controlled. Controlled access needs an approval that can take months of the timeframe. Check ClinicalTrials.gov for an ongoing trial asking the same question, which would report first.

### 3. Impact test (general track; for reviews, folded into the debate check)

Will this paper get cited?

- **Citations:** ask the user for Google Scholar counts on their nearest papers (they check by hand). Are the neighbours accumulating citations or sitting near zero? Never estimate counts yourself.
- **Venues:** from the PubMed metadata, which journals is the debate appearing in?
- **Relevance:** is there clinical, policy or practical demand? Effort is not value; demand shows in the neighbours' citation record.

### 4. Crystallise the question with PICO (both tracks)

The end of Phase 2 is one precise, researchable question.

- Identify Population, Intervention/Exposure, Comparison, Outcome.
- Name any element that is missing or fuzzy.
- Check the four belong to one coherent question, not four ideas stapled together. This is the most common way a PICO looks right and isn't.
- **Systematic review track:** strict PICO review question.
- **General track:** use PICO where it fits the project type; a qualitative or descriptive project may need only some elements.
- **Never write the corrected question.** Point to the element to fix and let the user redraft it.

### 5. Grandmother rule (both tracks, exit check of Phase 2)

Can the topic be explained in 2 to 3 clear sentences to someone outside the field? If their statement took a paragraph of jargon, flag it. Phase 3 conversations fail without it.

## Phase 3: Human vetting

Supervisor alignment, a mentor conversation, a research group or lab meeting. The plugin's verdict is the pressure test that gets the topic ready for this, never a substitute for it.
