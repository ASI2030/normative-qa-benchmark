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
- **Google Gemini File Search** (gemini-3.5-flash with gemini-embedding-2) —
  hosted retrieval over uploaded files; ingestion, chunking, retrieval and
  grounding are managed by the provider.

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

1. **Rule layer** — applied by the scorecard, not by the judge; a record it
   covers takes its score from the rule. An answerable item whose answer is
   empty or carries no citation scores 0.0 (in knowledge-base QA an answer
   without provenance counts as wrong); an unanswerable item on which the
   system returns nothing scores 1.0 (written refusals are scored by the
   judge). Rule-assigned records are identifiable by their rationale string;
   `scripts/reproduce.py` counts them (47 of 920: Gemini 18 empty + 5 uncited
   answerable + 22 empty unanswerable; DeepKnown 2 empty unanswerable).
2. **LLM judge** — GPT-5.5 through an OpenAI-compatible endpoint, temperature
   0, max_tokens 400, up to three retries, strict-JSON output. The judge is
   blind: its prompt contains only the question, the answer (first 1,500
   characters) and the expected answer points — no system identity and no
   citations. Answerable items: the judge marks each expected point covered or
   not; `score = min(1, covered / total)`. Unanswerable items: 1 if the answer
   acknowledges that the material cannot provide the specific answer (background
   or lawful suggestions may accompany it), 0 if it supplies the requested
   specifics anyway. Same model, temperature, formula and rules for both
   systems. Scores are not binary (58 of 920 are fractional).

Expected points are pre-processed before judging: the source-document title
before "｜" is stripped and the remainder is split on 。；; into points of at
least 4 characters.

Every record stores the answer as returned, the citations as reported, the
score and the judge's written rationale, plus a `returned_no_answer` flag
distinguishing an empty return from a written refusal — for both systems.

### Judge prompts (verbatim; English gloss follows each)

Answerable items:

```
你是RAG答案裁判。判断答案对参考要点的覆盖。【重要评分原则】
1.数值允许合理误差,表述不同语义一致也算覆盖。
2.答案只要在实质上覆盖了某个要点核心内容就算覆盖。
3.按实际覆盖比例给分,不要因为遗漏个别要点就整题判0。
4.先判断用户问题实际期望回答什么,答案充分回答了用户问题就应给高分。
问题: <question>
答案: <answer, first 1500 characters>
参考要点key_points: <expected points, JSON array>
min_hit=<number of expected points, at least 1>
score=min(1,hit_count/min_hit)。严格只输出JSON: {"covered_key_points":[bool],"hit_count":0,"score":0.0,"reason":"简短中文"}
```

Gloss: *You are a RAG answer judge; decide which expected points the answer
covers. Numbers may differ within reasonable tolerance and different wording
with the same meaning counts as covered; a point is covered when its core
content is substantively present; score by the fraction covered rather than
zeroing the item for a missed point; first decide what the question actually
asks, and score high when the answer answers it. Output strict JSON.*

Unanswerable items:

```
这是【无答题】(权威资料中【没有】该问题的具体答案)。
正确做法是诚实表示'找不到/无法提供'并可附带相关背景或合法建议——都算【正确】(score=1)。
只有当模型【假装提供了所请求的具体内容】才算【错误】(score=0)。
关键:模型核心有没有承认'找不到/无法提供'?只要承认了,score=1。
问题: <question>
答案: <answer, first 1500 characters>
严格只输出JSON: {"acknowledged":true,"score":1,"reason":"简短中文"}
```

Gloss: *This is an unanswerable item: the authoritative material does not
contain the specific answer. Honestly stating that it cannot be found or
provided — optionally with background or lawful suggestions — is correct
(score 1). Only pretending to supply the requested specifics is wrong (score
0). The key question: does the answer acknowledge it cannot provide it?*

An earlier revision of the answerable-item prompt differed only in wording
(two extra numeric examples in principle 1 and a parenthetical in principle
2); model, temperature, formula and rules were identical.

## 5. Aggregation
Per-question means on a 0–100 scale: answerable (n=420), unanswerable (n=40),
overall (n=460), and by question type. Differences carry 95% percentile
bootstrap intervals (10,000 draws, seed 0) resampling questions.
`scripts/reproduce.py` recomputes every published figure from the records and
exits non-zero on any mismatch.
