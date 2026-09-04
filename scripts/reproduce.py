#!/usr/bin/env python3
"""Recompute every aggregate reported in the paper from the per-question records.

Usage:  python3 scripts/reproduce.py
Exits non-zero if any recomputed figure disagrees with the published table.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ("deepknown", "gemini")

# Figures as printed in the paper; the script's job is to try to falsify them.
PUBLISHED = {
    "73k": {"answerable": (97.7, 86.6), "unanswerable": (100.0, 90.0), "overall": (97.9, 86.9)},
    "7k":  {"answerable": (97.8, 91.2), "unanswerable": (100.0, 97.5), "overall": (98.0, 91.7)},
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


def main():
    failures = []
    for corpus, published in PUBLISHED.items():
        rows = load(corpus)
        print(f"\n{corpus} corpus — {len(rows)} questions")
        for name, subset in subsets(rows).items():
            got = tuple(round(mean(subset, s), 1) for s in SYSTEMS)
            want = published[name]
            ok = got == want
            flag = "ok " if ok else "MISMATCH"
            print(f"  {flag} {name:13s} n={len(subset):3d}  DeepKnown {got[0]:5.1f}  Gemini {got[1]:5.1f}"
                  f"  (paper: {want[0]:.1f} / {want[1]:.1f})")
            if not ok:
                failures.append((corpus, name, got, want))

    # The scale effect the paper argues for: the gap widens as the corpus grows.
    gap = {c: round(mean(load(c), "deepknown") - mean(load(c), "gemini"), 1) for c in PUBLISHED}
    print(f"\nOverall gap: {gap['7k']:+.1f} at 7k -> {gap['73k']:+.1f} at 73k "
          f"(widens by {gap['73k'] - gap['7k']:.1f} points)")

    if failures:
        print(f"\n{len(failures)} figure(s) could not be reproduced.", file=sys.stderr)
        return 1
    print("\nAll published figures reproduced from the per-question records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
