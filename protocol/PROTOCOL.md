# Evaluation protocol

## 1. Corpus
Guangdong provincial policy and normative documents: **73,249 documents**, the
full corpus the deployed system serves. Both systems indexed this corpus in
full; corpus size is the operating point, not a variable.

## 2. Systems under test
- **DeepKnown** — knowledge-serving system with an explicit governance layer:
  version, scope and force are extracted at ingest, stored as typed fields and
  enforced as predicates before ranking; generation is confined to the
  admissible candidate set and abstains when that set does not determine an
  answer.
- **Google Gemini File Search** (gemini-2.5 family) — hosted retrieval over
  uploaded files; ingestion, chunking, retrieval and grounding are managed by
  the provider.

Both systems answered the same 460 questions; `data/questions.json` and the
per-question records confirm identical question text, type labels, expected
answer points and gold source documents on both sides.

## 3. Question set construction
Stems and expected answer points come from rule-guided, AI-assisted
construction with evidence grounding and business-owner review. The business
owner set the type standards, the jurisdictional and currency-of-force
conventions, and the evidence boundary of an acceptable answer. Items were
built with model assistance from extracted source passages and frozen by
script under programmatic checks — source existence, jurisdiction, currency of
force, title collision, evidence and format — followed by human spot-checks and
anomaly review.

| type | n | definition |
|---|---|---|
| simple | 223 | answerable from a single provision |
| complex | 169 | spans several constraints, conditions or documents |
| partial | 28 | the corpus supports only part of the answer |
| unanswerable | 40 | the corpus contains no supporting document; the correct output is a refusal |

Every answerable item carries a gold `source_document`; unanswerable items
carry none.

## 4. Scoring
Two layers.

1. **Rule layer.** Records meeting mechanical conditions are scored
   deterministically: an answerable item whose answer carries no citation
   scores 0.0 (in knowledge-base QA an answer without provenance counts as
   wrong); an unanswerable item on which the system declines, or returns
   nothing, scores 1.0. Rule-assigned records are identifiable by their
   rationale string; `scripts/reproduce.py` counts them (47 of 920).
2. **LLM judge.** All other records are scored by one LLM judge against the
   expected answer points with partial credit; scores are not binary (58 of
   920 are fractional). One judge, one configuration, held constant across
   both systems.

Every record stores the answer as returned, the citations as reported, the
score and the judge's written rationale, plus a `returned_no_answer` flag
distinguishing an empty return from a written refusal — for both systems.

## 5. Aggregation
Per-question means on a 0–100 scale: answerable (n=420), unanswerable (n=40),
overall (n=460), and by question type. Differences carry 95% percentile
bootstrap intervals (10,000 draws, seed 0) resampling questions.
`scripts/reproduce.py` recomputes every published figure from the records and
exits non-zero on any mismatch.
