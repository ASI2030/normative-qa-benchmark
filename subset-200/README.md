# 200-question evaluation subset

The 200 questions in this directory are a **stratified random sample** of the
420 answerable questions in the full benchmark one level up (`../data/`). They
are the evaluation set behind the paper that reports 200 questions.

| file | contents |
|---|---|
| `questions.json` | 200 questions: id, type, question, expected points, gold source document |
| `results.json` | per-question records for both systems: answer, citations, score, judge rationale, `returned_no_answer` |
| `results.csv` | the same records, flattened |

**How they were chosen.** `../scripts/make_subset.py` stratifies the 420
answerable items by question type and by the jurisdiction named in the gold
source document — both fixed before either system was run — allocates
proportionally, and draws with a seed fixed in advance. It reads no score,
answer, citation or judge rationale, so which items it keeps cannot depend on
how either system performed on them.

```bash
python3 ../scripts/make_subset.py --check     # regenerate this directory byte for byte and compare
python3 ../scripts/reproduce_200.py           # recompute every figure the paper reports
```

| type | n | DeepKnown | Gemini | gap | 95% CI |
|---|---|---|---|---|---|
| overall | 200 | 97.7 | 88.1 | +9.6 | [5.7, 13.8] |
| simple | 106 | 99.0 | 91.1 | +7.9 | [3.2, 13.3] |
| complex | 81 | 96.8 | 86.6 | +10.2 | [3.5, 18.0] |
| partial | 13 | 92.3 | 73.1 | +19.2 | [7.7, 30.8] |

The seed was fixed before the draw. Across seeds 0–9 the overall gap on a
200-item draw ranges +7.6 to +12.7 (median +11.3) against +11.0 on all 420
answerable items; this subset's +9.6 is one draw from that distribution, not a
separate result. The full set, the scorecard, the judge prompts and the
licence are in the [repository root](../).
