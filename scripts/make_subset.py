#!/usr/bin/env python3
"""Build subset-200/ from the full 460-question release in this repository.

The 200 items are a stratified random sample of the 420 answerable questions in
data/. The selection reads only a question's type and the jurisdiction named in
its gold source document — both fixed before either system was run — and draws
with a seed fixed in advance. No score, answer, citation or judge rationale is
consulted while selecting, so which items are kept cannot depend on how either
system performed on them.

Usage:
  python3 scripts/make_subset.py            # write subset-200/
  python3 scripts/make_subset.py --check    # verify subset-200/, exit non-zero if it differs
"""
import argparse, collections, csv, json, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = "subset-200"
SUBSET_SIZE, SEED = 200, 0
SYSTEMS = ("deepknown", "gemini")
# Answerable items only; the 40 unanswerable questions stay in the full set.
TYPES = ("simple", "complex", "partial")

# Prefecture-level jurisdictions of Guangdong, plus the province itself. Used
# only to stratify; an item whose gold source names none of them falls in "other".
CITY = re.compile("|".join([
    "广州", "深圳", "珠海", "汕头", "佛山", "韶关", "河源", "梅州", "惠州",
    "汕尾", "东莞", "中山", "江门", "阳江", "湛江", "茂名", "肇庆", "清远",
    "潮州", "揭阳", "云浮", "龙川", "广东",
]))


def stratum(rec):
    """(question type, jurisdiction) — both known before any system was run."""
    m = CITY.search(rec.get("source_document") or "")
    return rec["type"], (m.group(0) if m else "other")


def select(records):
    """Stratified sample: proportional allocation by largest remainder, fixed seed."""
    pool = [r for r in records if r["type"] in TYPES]
    buckets = collections.defaultdict(list)
    for r in pool:
        buckets[stratum(r)].append(r)
    keys = sorted(buckets)
    for k in keys:
        buckets[k].sort(key=lambda r: r["qid"])

    exact = {k: len(buckets[k]) * SUBSET_SIZE / len(pool) for k in keys}
    quota = {k: int(exact[k]) for k in keys}
    short = SUBSET_SIZE - sum(quota.values())
    for k in sorted(keys, key=lambda k: (-(exact[k] - quota[k]), k))[:short]:
        quota[k] += 1

    rng = random.Random(SEED)
    picked = []
    for k in keys:
        picked += rng.sample(buckets[k], min(quota[k], len(buckets[k])))
    return sorted(picked, key=lambda r: r["qid"])


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return json.load(fh)


def as_json(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def as_csv(rows):
    import io
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["qid", "type", "question", "source_document", "expected_points",
                *(f"{s}_{f}" for s in SYSTEMS
                  for f in ("answer", "n_citations", "score", "judge_rationale", "returned_no_answer"))])
    for r in rows:
        pts = r.get("expected_points")
        w.writerow([r["qid"], r["type"], r["question"], r.get("source_document", ""),
                    " ".join(pts) if isinstance(pts, list) else (pts or ""),
                    *(r[s].get(f, "") for s in SYSTEMS
                      for f in ("answer", "n_citations", "score", "judge_rationale", "returned_no_answer"))])
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify instead of writing")
    args = ap.parse_args()

    questions, results = read("data/questions.json"), read("data/results_73k.json")
    keep = [r["qid"] for r in select(results)]
    order = {q: i for i, q in enumerate(keep)}
    sub_q = sorted((q for q in questions if q["qid"] in order), key=lambda q: order[q["qid"]])
    sub_r = sorted((r for r in results if r["qid"] in order), key=lambda r: order[r["qid"]])
    assert len(sub_q) == len(sub_r) == SUBSET_SIZE

    artifacts = [(f"{OUT}/questions.json", as_json(sub_q)),
                 (f"{OUT}/results.json", as_json(sub_r)),
                 (f"{OUT}/results.csv", as_csv(sub_r))]
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    for name, text in artifacts:
        path = os.path.join(ROOT, name)
        if args.check:
            if not os.path.exists(path) or open(path, encoding="utf-8").read() != text:
                sys.exit(f"{name} differs from what this script generates")
            print(f"ok  {name}")
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"wrote {name}")

    counts = collections.Counter(r["type"] for r in sub_r)
    print("  composition: " + ", ".join(f"{t} {counts[t]}" for t in TYPES))


if __name__ == "__main__":
    sys.exit(main())
