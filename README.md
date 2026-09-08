# Version- and Scope-Aware QA over Normative Documents — Evaluation Artifact

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

---

# 简体中文

[English](#version--and-scope-aware-qa-over-normative-documents--evaluation-artifact) | 简体中文

这里是一次端到端评测的全部材料：题集、逐题记录与复现脚本。评测对象是两套自动化知识服务系统，
语料为中文规范性文档（省级政策与规范性文件），在生产规模下运行。

## 重要：两次运行不可互相比较

本产物包含两个语料规模的逐题记录，但**两次运行使用的裁判标准并不相同**——较小语料那次为节省评测
成本，采用的是更早的一版标准。因此，任何通过比较两次运行得出的数字，都同时混入了语料规模的影响与
评分工具本身的变化，而这两者无法从这些记录中分离。配套论文只报告全量语料（73,249 份文档）那一次，
不做任何跨运行的论断。较小语料的记录出于完整性一并发布；**请勿把两者之间的差异读作规模效应**。

## 目录内容

```
data/questions.json      460 道题：编号、类型、题面、期望要点、来源文档
data/results_73k.json    73,249 份文档语料下的逐题记录
data/results_7k.json     约 7 千份文档语料下的逐题记录
data/results_*.csv       同样的记录，扁平化为表格便于查看
scripts/reproduce.py     从逐题记录复算论文所报的各子集均值
protocol/                评测协议与题集构建说明
```

每条逐题记录都包含两套系统各自的：原样返回的答案、引用到的文档、裁判给出的分数，以及裁判的书面理由。

## 题集构成

| 类型 | 数量 | 考察什么 |
|---|---|---|
| 简单 | 223 | 单份文档内的事实查找 |
| 复杂 | 169 | 跨文档、跨条件或跨时间的综合 |
| 部分答案 | 28 | 语料只能支持答案的一部分 |
| 无答案 | 40 | 语料无法支持作答，系统应当拒答 |

可答 420 题 + 不可答 40 题。

## 复现论文中的数字

```bash
python3 scripts/reproduce.py
```

脚本从逐题分数重新计算每个子集均值，与论文所印数字比对，任何一处对不上即以非零码退出。
它同时打印主表（含 95% 自助置信区间）与评分层审计。输出节选：

```
73k corpus — 460 questions (reported in the paper)
  ok  answerable    n=420  DeepKnown  97.7  Gemini  86.6  (recorded: 97.7 / 86.6)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  90.0  (recorded: 100.0 / 90.0)
  ok  overall       n=460  DeepKnown  97.9  Gemini  86.9  (recorded: 97.9 / 86.9)

Main table, full corpus (460 questions)
  the zero-citation rule zeroed 23 answerable items, unread
  Answerable                     n=420  DeepKnown  97.7  Gemini  86.6  gap +11.0  95% CI [8.1, 14.2]
  Overall                        n=460  DeepKnown  97.9  Gemini  86.9  gap +11.0  95% CI [8.1, 13.9]
  Answerable, less the zeroed    n=397  DeepKnown  97.5  Gemini  91.7  gap  +5.9  95% CI [3.6, 8.3]
  Overall, less the zeroed       n=437  DeepKnown  97.8  Gemini  91.5  gap  +6.3  95% CI [4.0, 8.7]

Scoring layer, full corpus (920 records)
  rule-assigned rather than judged: 47  (Gemini 45, DeepKnown 2)
  zero-citation rule fired on 23 answerable items; 5 carry an answer that was never read, 18 are empty
```

## 已知的评分缺陷

评分包含一个规则层：可答题若记录到零条引用，会被直接判 0 分而不送裁判评阅。该规则在 73k 语料上对
被测的托管服务触发了 23 次，其中 5 次的答案其实有实质内容却从未被评阅；而它对另一套系统一次也没有
触发过——因为后者的记录存的是被引文档标题而非引用条数。剔除这 23 题后，托管服务的可答均分由 86.6
变为 91.7。论文因此对每个主要数字都同时报告原始分与剔除后的修正分。

## 利益声明

本次评测由参与比较的两套系统之一的开发方执行。我们把题集、每一条逐题答案、每一条裁判理由和评分
代码全部公开，正是为了让所报数字可以被独立核对、重算或质疑。

## 许可

题集与逐题记录：CC BY 4.0。脚本：MIT。
