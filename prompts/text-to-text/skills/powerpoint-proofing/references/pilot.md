# Lightweight designer pilot

No portal, account system, queue, database, or central storage is required.

## Operation

- Recruit 10 presentation designers.
- Review approximately 20 decks per week through the normal Codex prompt: “Proof this PowerPoint.”
- Designers reference stable finding IDs when they accept, dismiss, or reclassify an issue.
- Keep each deck and its review local to the Codex task. Store only sanitized regression examples in this project.

## Weekly triage

For every dismissed or reclassified finding, record a local JSON label:

```json
{
  "PPT-004-1234ABCD": {
    "correct": false,
    "ownership": "inherited_from_source",
    "note": "Template-derived footer; not a designer issue."
  }
}
```

Run:

```bash
python3 scripts/evaluate_labels.py review.json labels.json
```

The evaluator fails unless deterministic precision and source/designer attribution accuracy are each at least 95%. It also refuses to calculate a gate when no relevant human labels exist.

Convert confirmed failure patterns into sanitized tests. Do not weaken a rule solely to improve a metric; fix applicability, provenance, ownership, or evidence handling.

## Exit gates

- No false-positive Critical/High findings in the supplied designer-review case.
- At least 95% precision for human-labelled deterministic findings.
- At least 95% source-versus-designer attribution accuracy.
- Repeatable inventory and deterministic rule output.
- Every visual finding linked to slide-level render evidence.

Complete Brand coverage remains out of scope until the approved template, chart/table component examples, and licensed Marsh Serif files are available.
