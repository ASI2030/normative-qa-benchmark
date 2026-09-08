#!/usr/bin/env python3
"""Recompute every aggregate reported in the paper from the per-question records.

Usage:  python3 scripts/reproduce.py
Exits non-zero if any recomputed figure disagrees with the published table.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ("deepknown", "gemini")

# Figures as printed in the paper; the script's job is to try to falsify them.
# Reference figures as printed in the paper.
PUBLISHED = {
    "73k": {"answerable": (97.7, 86.6), "unanswerable": (100.0, 90.0), "overall": (97.9, 86.9)},
}


def load(corpus):
    with open(f"{ROOT}/data/results_{corpus}.json", encoding="utf-8") as f:
        return json.load(f)


def mean(rows, system):
    vals = [r[system]["score"] for r in rows if r[system]["score"] is not None]
    if not vals:
        raise ValueError("no scores")
    return 100.0 * sum(vals) / len(vals)


def subsets(rows):
    answerable = [r for r in rows if r["type"] != "unanswerable"]
    unanswerable = [r for r in rows if r["type"] == "unanswerable"]
    return {"answerable": answerable, "unanswerable": unanswerable, "overall": rows}



# ---------------------------------------------------------------------------
# The paper's main table, recomputed with 95% percentile bootstrap intervals.
#
# Recomputes the figures the paper reports, with 95% percentile bootstrap
# intervals on each difference.
# ---------------------------------------------------------------------------

BOOTSTRAP_DRAWS = 10000
BOOTSTRAP_SEED = 0


def main_table():
    import random

    rows = load("73k")

    def mean(subset, system):
        return 100.0 * sum(r[system]["score"] for r in subset) / len(subset)

    def interval(subset):
        rng = random.Random(BOOTSTRAP_SEED)
        draws = []
        for _ in range(BOOTSTRAP_DRAWS):
            s = [subset[rng.randrange(len(subset))] for _ in subset]
            draws.append(mean(s, "deepknown") - mean(s, "gemini"))
        draws.sort()
        return draws[int(0.025 * BOOTSTRAP_DRAWS)], draws[int(0.975 * BOOTSTRAP_DRAWS)]

    print(f"\nMain table, full corpus ({len(rows)} questions)")
    cases = [
        ("Answerable",   lambda r: r["type"] != "unanswerable", frozenset()),
        ("Unanswerable", lambda r: r["type"] == "unanswerable", frozenset()),
        ("Overall",      lambda r: True,                        frozenset()),
    ]
    for label, pred, exclude in cases:
        subset = [r for r in rows if pred(r) and r["qid"] not in exclude]
        dk, gm = mean(subset, "deepknown"), mean(subset, "gemini")
        lo, hi = interval(subset)
        print(f"  {label:30s} n={len(subset):3d}  DeepKnown {dk:5.1f}  Gemini {gm:5.1f}"
              f"  gap {dk - gm:+5.1f}  95% CI [{lo:.1f}, {hi:.1f}]")



def scoring_layer():
    """Recompute the scoring-layer figures the paper quotes for this condition."""
    RULE_RATIONALES = {
        "无答题: 未输出", "非安全题无引用→判错", "非安全题: 未召回/未答",
        "无答题: 正确表示无法回答", "合并无引用/无答→0",
    }
    rows = load("73k")
    rat = lambda r, s: (r[s].get("judge_rationale") or "").strip()

    ruled = {s: sum(1 for r in rows if rat(r, s) in RULE_RATIONALES) for s in SYSTEMS}
    print(f"\nScoring layer, full corpus ({len(rows) * len(SYSTEMS)} records)")
    print(f"  rule-assigned rather than judged: {sum(ruled.values())}"
          f"  (Gemini {ruled['gemini']}, DeepKnown {ruled['deepknown']})")


    fractional = sum(1 for r in rows for s in SYSTEMS
                     if r[s]["score"] not in (0.0, 1.0))
    print(f"  fractional judgments: {fractional}")


def main():
    failures = []
    for corpus, published in PUBLISHED.items():
        rows = load(corpus)
        note = "reported in the paper" if corpus == "73k" else "released, not reported in the paper"
        print(f"\n{corpus} corpus — {len(rows)} questions ({note})")
        for name, subset in subsets(rows).items():
            got = tuple(round(mean(subset, s), 1) for s in SYSTEMS)
            want = published[name]
            ok = got == want
            flag = "ok " if ok else "MISMATCH"
            print(f"  {flag} {name:13s} n={len(subset):3d}  DeepKnown {got[0]:5.1f}  Gemini {got[1]:5.1f}"
                  f"  (recorded: {want[0]:.1f} / {want[1]:.1f})")
            if not ok:
                failures.append((corpus, name, got, want))

    main_table()
    scoring_layer()

    if failures:
        print(f"\n{len(failures)} figure(s) could not be reproduced.", file=sys.stderr)
        return 1
    print("\nAll published figures reproduced from the per-question records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
