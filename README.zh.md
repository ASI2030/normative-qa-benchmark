# 规范性文档的版本感知与适用范围感知问答 —— 评测产物

<p align="center">
  <a href="https://aaai.org/conference/aaai/aaai-27/iaai-27-call/"><img alt="论文" src="https://img.shields.io/badge/%E8%AE%BA%E6%96%87-IAAI--27%20%E6%8A%95%E7%A8%BF-blue?style=for-the-badge&labelColor=555"></a>
  <a href="https://creativecommons.org/licenses/by/4.0/"><img alt="数据许可" src="https://img.shields.io/badge/%E6%95%B0%E6%8D%AE-CC%20BY%204.0-green?style=for-the-badge&labelColor=555"></a>
  <a href="LICENSE"><img alt="代码许可" src="https://img.shields.io/badge/%E4%BB%A3%E7%A0%81-MIT-green?style=for-the-badge&labelColor=555"></a>
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/LANG-English-blue?style=for-the-badge&labelColor=555"></a>
</p>

<p align="center"><sub>Read this in <a href="README.md">English</a></sub></p>

这里是一次端到端评测的全部材料：题集、逐题记录与复现脚本。评测对象是两套自动化知识服务系统，
语料为中文规范性文档（省级政策与规范性文件），在生产规模下运行。

## 目录内容

```
data/questions.json      460 道题：编号、类型、题面、期望要点、来源文档
data/results_73k.json    73,249 份文档语料下的逐题记录
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

73k corpus — by question type (Table 2)
  ok  simple        n=223  DeepKnown  98.7  Gemini  87.3  (recorded: 98.7 / 87.3)
  ok  complex       n=169  DeepKnown  97.2  Gemini  88.9  (recorded: 97.2 / 88.9)
  ok  partial       n= 28  DeepKnown  92.3  Gemini  67.9  (recorded: 92.3 / 67.9)
  ok  unanswerable  n= 40  DeepKnown 100.0  Gemini  90.0  (recorded: 100.0 / 90.0)

Main table, full corpus (460 questions)
  Answerable                     n=420  DeepKnown  97.7  Gemini  86.6  gap +11.0  95% CI [8.1, 14.2]
  Unanswerable                   n= 40  DeepKnown 100.0  Gemini  90.0  gap +10.0  95% CI [2.5, 20.0]
  Overall                        n=460  DeepKnown  97.9  Gemini  86.9  gap +11.0  95% CI [8.1, 13.9]
    by type: simple              n=223  DeepKnown  98.7  Gemini  87.3  gap +11.5  95% CI [7.3, 15.9]
    by type: complex             n=169  DeepKnown  97.2  Gemini  88.9  gap  +8.3  95% CI [3.9, 13.2]
    by type: partial             n= 28  DeepKnown  92.3  Gemini  67.9  gap +24.4  95% CI [14.3, 35.1]

Scoring layer, full corpus (920 records)
  rule-assigned rather than judged: 47  (Gemini 45, DeepKnown 2)
  fractional judgments: 58

All published figures reproduced from the per-question records.
```

## 已部署的系统

本文评测的带治理层系统是一款商业产品，运行于
<https://yun.dknowc.cn/wlcb/dknowc-chat/>，可自助注册使用。

## 开放性

题集、每一条逐题答案、每一条裁判理由和评分代码全部公开，所报每一个数字都可以被独立核对与重算，
任何一题也都可以在其他裁判配置下重新评分。

## 许可

题集与逐题记录：CC BY 4.0。脚本：MIT。
