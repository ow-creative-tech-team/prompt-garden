#!/usr/bin/env python3
"""Evaluate human-labelled proofing findings against the 95% pilot gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path, help="review JSON from proofing_engine.py")
    parser.add_argument("labels", type=Path, help="JSON object keyed by finding_id with correct and optional ownership fields")
    parser.add_argument("--threshold", type=float, default=0.95)
    args = parser.parse_args()
    review = json.loads(args.review.read_text(encoding="utf-8"))
    labels = json.loads(args.labels.read_text(encoding="utf-8"))
    deterministic = [f for f in review["findings"] if f["rule_id"] != "VISUAL-001"]
    labelled = [(f, labels[f["finding_id"]]) for f in deterministic if f["finding_id"] in labels]
    if not labelled:
        raise SystemExit("No deterministic findings were labelled; pilot gates cannot be calculated.")
    precision = sum(bool(label.get("correct")) for _, label in labelled) / len(labelled)
    ownership_labels = [(f, label) for f, label in labelled if label.get("ownership")]
    attribution = (sum(f["ownership"] == label["ownership"] for f, label in ownership_labels) / len(ownership_labels)) if ownership_labels else None
    result = {
        "labelled_deterministic_findings": len(labelled),
        "deterministic_precision": round(precision, 4),
        "ownership_labels": len(ownership_labels),
        "attribution_accuracy": round(attribution, 4) if attribution is not None else None,
        "threshold": args.threshold,
        "passes_precision": precision >= args.threshold,
        "passes_attribution": attribution is not None and attribution >= args.threshold,
    }
    print(json.dumps(result, indent=2))
    if not result["passes_precision"] or not result["passes_attribution"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
