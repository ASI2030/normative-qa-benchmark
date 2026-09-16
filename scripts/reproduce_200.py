#!/usr/bin/env python3
"""Recompute every figure reported for the 200-item subset from its per-question records.

Usage:  python3 scripts/reproduce_200.py
Exits non-zero if any recomputed figure disagrees with the published table.
"""
import collections, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ("deepknown", "gemini")
TYPES = ("simple", "complex", "partial")
BOOTSTRAP_DRAWS, BOOTSTRAP_SEED = 10000, 0

# Figures as printed in the paper; this script's job is to try to falsify them.
PUBLISHED = {
    "overall": (200, 97.7, 88.1),
    "simple":  (106, 99.0, 91.1),
    "complex": (81,  96.8, 86.6),
    "partial": (13,  92.3, 73.1),
}
# Items at full credit / partial credit / zero, per type and system.
PUBLISHED_CREDIT = {
    "simple":  {"deepknown": (103, 3, 0), "gemini": (95, 3, 8)},
    "complex": {"deepknown": (75, 6, 0),  "gemini": (65, 9, 7)},
    "partial": {"deepknown": (11, 2, 0),  "gemini": (6, 7, 0)},
}


def load():
    with open(f"{ROOT}/subset-200/results.json", encoding="utf-8") as fh:
        return json.load(fh)


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


def main():
    rows = load()
    failures = []

    print(f"\nStratified 200-item subset — {len(rows)} answerable questions")
    print("  drawn from data/ by scripts/make_subset.py (type and jurisdiction only, seed 0)")
    print("  verify the selection: python3 scripts/make_subset.py --check\n")

    subsets = [("overall", rows)] + [(t, [r for r in rows if r["type"] == t]) for t in TYPES]
    for name, subset in subsets:
        n, dk_want, gm_want = PUBLISHED[name]
        dk, gm = round(mean(subset, "deepknown"), 1), round(mean(subset, "gemini"), 1)
        lo, hi = interval(subset)
        ok = (len(subset), dk, gm) == (n, dk_want, gm_want)
        if not ok:
            failures.append(name)
        print(f"  {'ok ' if ok else 'MISMATCH'} {name:8s} n={len(subset):3d}  DeepKnown {dk:5.1f}  Gemini {gm:5.1f}"
              f"  gap {dk - gm:+5.1f}  95% CI [{lo:.1f}, {hi:.1f}]   (recorded: {dk_want:.1f} / {gm_want:.1f})")

    print("\nCredit breakdown (full / partial / zero)")
    for t in TYPES:
        subset = [r for r in rows if r["type"] == t]
        for s in SYSTEMS:
            full = sum(1 for r in subset if r[s]["score"] == 1.0)
            zero = sum(1 for r in subset if r[s]["score"] == 0.0)
            got, want = (full, len(subset) - full - zero, zero), PUBLISHED_CREDIT[t][s]
            ok = got == want
            if not ok:
                failures.append(f"credit:{t}:{s}")
            print(f"  {'ok ' if ok else 'MISMATCH'} {t:8s} {s:9s} {got[0]:3d} / {got[1]:3d} / {got[2]:3d}"
                  f"   (recorded: {want[0]}/{want[1]}/{want[2]})")

    RULE_RATIONALES = {
        "无答题: 未输出", "非安全题无引用→判错", "非安全题: 未召回/未答",
        "无答题: 正确表示无法回答", "合并无引用/无答→0",
    }
    rat = lambda r, s: (r[s].get("judge_rationale") or "").strip()
    ruled = {s: sum(1 for r in rows if rat(r, s) in RULE_RATIONALES) for s in SYSTEMS}
    fractional = sum(1 for r in rows for s in SYSTEMS if r[s]["score"] not in (0.0, 1.0))
    docs = {(r.get("source_document") or "").strip() for r in rows if r.get("source_document")}
    print(f"\nScoring layer ({len(rows) * len(SYSTEMS)} records)")
    print(f"  rule-assigned rather than judged: {sum(ruled.values())}"
          f"  (Gemini {ruled['gemini']}, DeepKnown {ruled['deepknown']})")
    print(f"  fractional judgments: {fractional}")
    print(f"  distinct gold source documents: {len(docs)}")

    if failures:
        print(f"\n{len(failures)} figure(s) could not be reproduced: {', '.join(failures)}", file=sys.stderr)
        return 1
    print("\nAll published figures reproduced from the per-question records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
