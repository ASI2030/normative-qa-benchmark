# Evaluation protocol

> Everything below is stated from project records. Where a fact was not
> recorded, this document says so rather than reconstructing it.

## 1. Corpora
Provincial policy and regulatory documents. One scale:
- **73k** — 73,249 documents (full corpus)

## 2. Systems under test
- **DeepKnown** — knowledge-serving system with an explicit governance layer
- **Google Gemini File Search** — hosted retrieval over uploaded files

We do not hold either system's exact model version, API dates, or per-system
configuration for these runs.

## 3. Question set construction

Documented in the project's own methodology audit (2026-09-04), whose counts we
verified against the parent workbook.

**Provenance.** The released 460 are a post hoc curated subset of a larger
authored question bank. Items were removed after both systems had been run, and
one stated aim of that removal was to adjust how the two systems' score ranges
related to each other. Every unanswerable item was retained. This set is
therefore a development set, not a held-out or pre-registered benchmark.

**Authoring.** Stems and expected points come from rule-guided, AI-assisted
construction with evidence grounding and business-owner review — not from
independent per-item drafting by policy experts. Some items reuse points from an earlier round; the rest were
rebuilt with fresh evidence mapping, under programmatic source, jurisdiction,
currency-of-force, title-collision, evidence and format checks.

**Human review.** No full double-blind annotation with adjudicated
disagreements exists. Review consists of programmatic checks, business spot
checks, and one targeted pass over 29 items on which DeepKnown scored below
full marks — neither random nor doubly annotated. That pass found expected
points that overreached the question, points from a superseded version, points
absent from the source, and mis-recognised characters.

**Known artifact limit.** The audit counts 96 of the 169 complex items as
single-source and 73 as multi-source. These records cannot confirm that split:
each item stores a single `source_document`.

## 4. Scoring
An LLM judge scores each answer against the expected points, awarding partial
credit; scores are not binary. Unanswerable questions score 1.0 only when the
system declines to answer rather than producing specifics.

We do not hold the judge configuration: model and version, temperature, the
scoring prompt verbatim, or the rubric. Nor can we confirm that the two runs
shared one configuration — they did not; see the note at the top of the README.
Anyone can re-judge the released answers; no one can reproduce these scores.

## 5. Aggregation
Subset means over per-question scores, reported on a 0–100 scale:
answerable (n=420), unanswerable (n=40), overall (n=460).
`scripts/reproduce.py` recomputes all of them from the published records.
