# Version- and Scope-Aware QA over Normative Documents — Evaluation Artifact

<p align="center">
[![PAPER](https://img.shields.io/badge/PAPER-IAAI----27%20submission-blue?style=for-the-badge&labelColor=555)](https://aaai.org/conference/aaai/aaai-27/iaai-27-call/)
[![DATA](https://img.shields.io/badge/DATA-CC%20BY%204.0-green?style=for-the-badge&labelColor=555)](https://creativecommons.org/licenses/by/4.0/)
[![CODE](https://img.shields.io/badge/CODE-MIT-green?style=for-the-badge&labelColor=555)](LICENSE)
[![LANG](https://img.shields.io/badge/LANG-%E4%B8%AD%E6%96%87-red?style=for-the-badge&labelColor=555)](README.zh.md)
</p>

English | [简体中文](#简体中文)
Question set, per-question records and reproduction script for an end-to-end
evaluation of two automated knowledge-serving systems over Chinese normative
documents (provincial policy and regulatory texts) at production scale.

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
scripts/reproduce.py     recomputes the subset means the paper reports from the records
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

420 answerable + 40 unanswerable.

## Reproducing the reported figures

```bash
python3 scripts/reproduce.py
```

It recomputes each subset mean from the per-question scores and compares it
against the figures printed in the paper, exiting non-zero on any mismatch.

```
73k corpus — 460 questions (reported in the paper)
  ok  answerable    n=420  DeepKnown  97.7  Gemini  86.6  (recorded: 97.7 / 86.6)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  90.0  (recorded: 100.0 / 90.0)
  ok  overall       n=460  DeepKnown  97.9  Gemini  86.9  (recorded: 97.9 / 86.9)

7k corpus — 460 questions (released, not reported in the paper)
  ok  answerable    n=420  DeepKnown  97.8  Gemini  91.2  (recorded: 97.8 / 91.2)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  97.5  (recorded: 100.0 / 97.5)
  ok  overall       n=460  DeepKnown  98.0  Gemini  91.7  (recorded: 98.0 / 91.7)

Main table, full corpus (460 questions)
  the zero-citation rule zeroed 23 answerable items, unread
  Answerable                     n=420  DeepKnown  97.7  Gemini  86.6  gap +11.0  95% CI [8.1, 14.2]
  Unanswerable                   n= 40  DeepKnown 100.0  Gemini  90.0  gap +10.0  95% CI [2.5, 20.0]
  Overall                        n=460  DeepKnown  97.9  Gemini  86.9  gap +11.0  95% CI [8.1, 13.9]
  Answerable, less the zeroed    n=397  DeepKnown  97.5  Gemini  91.7  gap  +5.9  95% CI [3.6, 8.3]
  Overall, less the zeroed       n=437  DeepKnown  97.8  Gemini  91.5  gap  +6.3  95% CI [4.0, 8.7]

Scoring layer, full corpus (920 records)
  rule-assigned rather than judged: 47  (Gemini 45, DeepKnown 2)
  zero-citation rule fired on 23 answerable items; 5 carry an answer that was never read, 18 are empty
  on the remaining answerable items Gemini cites 8.97 sources on average, median 7
  fractional judgments: 58

All published figures reproduced from the per-question records.
```

## Declared interest

The evaluation was run by the developer of one of the two systems under test.
The question set, every per-question answer, every judge rationale and the
scoring code are published here so that the reported figures can be checked,
recomputed, or disputed independently.

## License

Question set and per-question records: CC BY 4.0. Scripts: MIT.
