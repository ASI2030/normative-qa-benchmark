#!/usr/bin/env python3
"""Recompute the figures the paper reports from the released per-question records.

Usage:  python3 scripts/reproduce.py
Exits non-zero if any recomputed figure disagrees with the published table.

The 73k condition was scored on 560 questions; 460 of them were later selected
for an earlier release. Both sets are recomputed here. The 7k condition covers
only those 460.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ("deepknown", "gemini")

PUBLISHED = {
    "73k full (560)":  {"answerable": (94.7, 82.1), "unanswerable": (100.0, 90.0), "overall": (95.1, 82.6)},
    "73k subset (460)": {"answerable": (97.7, 86.6), "unanswerable": (100.0, 90.0), "overall": (97.9, 86.9)},
    "7k subset (460)":  {"answerable": (97.8, 91.2), "unanswerable": (100.0, 97.5), "overall": (98.0, 91.7)},
}
FILES = {
    "73k full (560)": "results_73k_full560.json",
    "73k subset (460)": "results_73k.json",
    "7k subset (460)": "results_7k.json",
}
BLOCKS = {"general": (98.2, 88.6), "advantage": (96.9, 81.7)}  # over the 460 subset


def load(name):
    with open(f"{ROOT}/data/{FILES[name]}", encoding="utf-8") as f:
        return json.load(f)


def mean(rows, system):
    vals = [r[system]["score"] for r in rows if r[system]["score"] is not None]
    return 100.0 * sum(vals) / len(vals)


def subsets(rows):
    return {"answerable": [r for r in rows if r["type"] != "unanswerable"],
            "unanswerable": [r for r in rows if r["type"] == "unanswerable"],
            "overall": rows}


def main():
    failures = []
    for cond, published in PUBLISHED.items():
        rows = load(cond)
        print(f"\n{cond} — {len(rows)} questions")
        for name, subset in subsets(rows).items():
            got = tuple(round(mean(subset, s), 1) for s in SYSTEMS)
            want = published[name]
            ok = got == want
            print(f"  {'ok ' if ok else 'MISMATCH'} {name:13s} n={len(subset):3d}  "
                  f"DeepKnown {got[0]:5.1f}  Gemini {got[1]:5.1f}  (paper: {want[0]:.1f} / {want[1]:.1f})")
            if not ok:
                failures.append((cond, name, got, want))

    # The question set is two authoring blocks; the paper reports them separately.
    full = load("73k full (560)")
    released = [r for r in full if r["in_released_460"]]
    print("\nBy authoring block, over the 460-question subset")
    for block, want in BLOCKS.items():
        rows = [r for r in released if r["block"] == block]
        got = tuple(round(mean(rows, s), 1) for s in SYSTEMS)
        ok = got == want
        print(f"  {'ok ' if ok else 'MISMATCH'} {block:10s} n={len(rows):3d}  "
              f"DeepKnown {got[0]:5.1f}  Gemini {got[1]:5.1f}  (paper: {want[0]:.1f} / {want[1]:.1f})")
        if not ok:
            failures.append(("blocks", block, got, want))

    # What selecting the 460 did to the record.
    excluded = [r for r in full if not r["in_released_460"]]
    zeros_full = sum(1 for r in full if r["type"] != "unanswerable" and r["deepknown"]["score"] == 0)
    zeros_kept = sum(1 for r in released if r["type"] != "unanswerable" and r["deepknown"]["score"] == 0)
    blank_full = sum(1 for r in full if r["type"] != "unanswerable" and r["gemini"]["returned_no_answer"])
    blank_kept = sum(1 for r in released if r["type"] != "unanswerable" and r["gemini"]["returned_no_answer"])
    print(f"\nSelection of the 460: {len(excluded)} answerable questions were dropped after scoring.")
    print(f"  DeepKnown zero-scored answerable items: {zeros_full} in the full set, {zeros_kept} in the subset")
    print(f"  Gemini blank answerable responses:      {blank_full} in the full set, {blank_kept} in the subset")

    if failures:
        print(f"\n{len(failures)} figure(s) could not be reproduced.", file=sys.stderr)
        return 1
    print("\nAll published figures reproduced from the per-question records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
