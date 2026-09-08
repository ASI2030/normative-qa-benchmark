# Version- and Scope-Aware QA over Normative Documents — Evaluation Artifact

Question set, per-question records and reproduction script for an end-to-end
evaluation of two automated knowledge-serving systems over Chinese normative
documents (provincial policy and regulatory texts), run at two corpus scales.

## Important: the two runs are not comparable

This release contains per-question records for two corpus sizes, but **the two
runs did not use the same judging standard** — the smaller-corpus run was scored
under an earlier standard to save evaluation cost. Any figure computed by
comparing the two runs therefore mixes a corpus-size effect with a change in the
scoring instrument, and the two cannot be separated from these records. The
accompanying paper reports the full-corpus (73,249-document) run only, and makes
no cross-run claim. The smaller-corpus records are included for completeness;
please do not read a difference between them as a scale effect.

## What is here

```
data/questions.json      460 questions: id, type, question, expected points, source document
data/results_73k.json    per-question records over the 73,249-document corpus
data/results_7k.json     per-question records over the ~7k-document corpus
data/results_*.csv       the same records, flattened for spreadsheet use
scripts/reproduce.py     recomputes every aggregate in the paper from the records
protocol/               evaluation protocol and question-construction rules
```

Each per-question record carries, for both systems, the answer as returned, the
documents cited, the judge's score and the judge's written rationale.

## Question set

| type | n | what it tests |
|---|---|---|
| simple | 223 | single-document factual lookup |
| complex | 169 | synthesis across documents, conditions, or time |
| partial | 28 | only part of the answer is present in the corpus |
| unanswerable | 40 | the corpus cannot support an answer; the system should abstain |

420 answerable + 40 unanswerable. The same 460 questions are run against both
corpus scales, so the two runs are directly comparable.

## Reproducing the reported figures

```bash
python3 scripts/reproduce.py
```

It recomputes each subset mean from the per-question scores and compares it
against the figures printed in the paper, exiting non-zero on any mismatch.

```
73k corpus — 460 questions
  ok  answerable    n=420  DeepKnown  97.7  Gemini  86.6  (paper: 97.7 / 86.6)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  90.0  (paper: 100.0 / 90.0)
  ok  overall       n=460  DeepKnown  97.9  Gemini  86.9  (paper: 97.9 / 86.9)

7k corpus — 460 questions
  ok  answerable    n=420  DeepKnown  97.8  Gemini  91.2  (paper: 97.8 / 91.2)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  97.5  (paper: 100.0 / 97.5)
  ok  overall       n=460  DeepKnown  98.0  Gemini  91.7  (paper: 98.0 / 91.7)

Overall gap: +6.3 at 7k -> +11.0 at 73k (widens by 4.7 points)
```

## Declared interest

The evaluation was run by the developer of one of the two systems under test.
The question set, every per-question answer, every judge rationale and the
scoring code are published here so that the reported figures can be checked,
recomputed, or disputed independently.

## License

Question set and per-question records: CC BY 4.0. Scripts: MIT.
