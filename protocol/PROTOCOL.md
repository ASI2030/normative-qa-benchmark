# Evaluation protocol

> Sections marked **PENDING** are being supplied by the team and will be filled
> before release; nothing here is reconstructed from memory.

## 1. Corpora
Provincial policy and regulatory documents. Two scales, identical question set:
- **73k** — 73,249 documents (full corpus)
- **7k** — roughly 7,000 documents (subset) — *PENDING: exact document count*

## 2. Systems under test
- **DeepKnown** — knowledge-serving system with an explicit governance layer
- **Google Gemini File Search** — hosted retrieval over uploaded files

*PENDING: exact model versions, API dates, and per-system configuration.*

## 3. Question set construction
*PENDING (owner: 侍纪伟)* — how the 460 questions were written, how the four
types were assigned, who authored the expected points, and whether any
cross-review was performed.

## 4. Scoring
An LLM judge scores each answer against the expected points, awarding partial
credit; scores are not binary. Unanswerable questions score 1.0 only when the
system declines to answer rather than producing specifics.

*PENDING (owner: 金帅澎)* — judge model and version, temperature, the scoring
prompt verbatim, the rubric, and whether the 7k and 73k runs used the same
judge configuration.

## 5. Aggregation
Subset means over per-question scores, reported on a 0–100 scale:
answerable (n=420), unanswerable (n=40), overall (n=460).
`scripts/reproduce.py` recomputes all of them from the published records.
