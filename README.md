# Version- and Scope-Aware QA over Normative Documents — Evaluation Artifact

Question set, per-question records and a reproduction script for an end-to-end
evaluation of two knowledge-serving systems over Chinese normative documents
(provincial policy and regulatory texts).

## What is here

```
data/results_73k_full560.json   all 560 questions scored on the 73,249-document corpus
data/results_73k_full560.csv    the same records, flattened
data/excluded_100.json          the 100 answerable questions dropped after scoring
data/results_73k.json           the 460-question subset released earlier
data/results_7k.json            the same 460 questions over a ~7,000-document store
data/questions.json             the 460 subset without system answers
scripts/reproduce.py            recomputes the reported subset means and block splits
```

Each per-question record carries, for both systems, the answer as returned, the
citations, the judge's score and the judge's written rationale, plus the
question's authoring block and, where it has one, its advantage category.

## How this question set came to be

Read this before using the figures.

The 73k run scored **560** questions. A **460**-question subset of that run was
selected afterwards and released earlier; the 100 dropped questions are in
`excluded_100.json`. No reason for the selection was recorded. The selection is
not neutral with respect to the results: all 14 answerable questions on which
DeepKnown scored zero fall among the dropped 100, so the 460-question subset
contains no DeepKnown zero. Report the 560-question figures, or report both.

An earlier step reduced a 600-question pool to 560 before scoring, on a
retrieval-status field (29 FAIL, 9 not-recalled, 1 PASS, 1 recalled).

The set has two authoring blocks. The **general** block supplies 349 of the 460.
The **advantage** block supplies 111, each carrying one of six vendor-defined
capability categories (deep semantics, attachment parsing, table-header
continuation, tax-annotation governance, historical versions, cross-region).
The between-system gap is larger on the advantage block than on the general one;
on two of its six categories the hosted service scores higher. `block` and
`advantage_type` ship with every record so any figure can be recomputed either way.

## Question types

| type | n (560) | n (460) | what it tests |
|---|---|---|---|
| simple | 271 | 223 | single-document factual lookup |
| complex | 215 | 169 | synthesis across documents or editions |
| partial | 34 | 28 | only part of the answer is in the corpus |
| unanswerable | 40 | 40 | the corpus cannot support an answer; abstention is correct |

## Reproducing

```bash
python3 scripts/reproduce.py
```

It recomputes each subset mean from the per-question scores, compares them
against the figures printed in the paper, reports the block splits, and exits
non-zero on any mismatch. It also prints what selecting the 460 did to the
record. Figures the paper reports that this script does not cover are computed
from the same files.

## What is not here

The judge prompt and the scoring code are not released. DeepKnown's answer text
was not retained for the 100 dropped questions; their records carry its
citations, score and judge rationale but no answer string. The run logs behind
the reported interface failures — HTTP status, latency, tool-call counts — are
not in this release either.

## Declared interest

The evaluation was designed, run and scored by the developer of one of the two
systems under test, who also assembled the corpora and wrote the questions,
including the advantage block described above. No independent party
administered it. The question set, every per-question answer, every judge
rationale and every score are published here so that the reported figures can be
checked, recomputed, or disputed.

## License

Question set and per-question records: CC BY 4.0. Scripts: MIT.
