# Visual review protocol

Visual findings require a rendered slide. XML geometry may nominate candidates but cannot establish hierarchy, density, crop quality, contrast, or overall clarity by itself.

## Review sequence

For every rendered slide inspect:

1. hierarchy and focal point;
2. density, legibility, and whitespace;
3. alignment, spacing, and intended grouping;
4. foreground/background contrast;
5. image crop, treatment, and relevance;
6. chart/table clarity without inventing component rules;
7. brand/template consistency supported by `brand-guidelines.md`;
8. alternatives, WIP labels, and placeholders that require a choice.

Use the render, normalized inventory, source mapping, and deterministic candidates together. Do not infer an object is visible merely because it exists in XML.

## Required model response

Return JSON only:

```json
{
  "schema_version": "1.0",
  "slides_reviewed": [1],
  "findings": [
    {
      "slide_number": 1,
      "object_id": "4",
      "object_name": "Title 3",
      "visibility": "in_frame",
      "category": "hierarchy",
      "rule_id": "VISUAL-001",
      "rule_version": "1.0",
      "observed_evidence": "The subtitle is visually larger than the title in the slide render.",
      "expected_rule": "The main message should be the clearest focal point.",
      "required_action": "Restore a clear title-first hierarchy while preserving the wording.",
      "severity": "Medium",
      "confidence": "high",
      "ownership": "designer_introduced",
      "readiness_impact": true,
      "evidence": {"render": "slide-1.png", "region": [0.08, 0.10, 0.82, 0.30]}
    }
  ]
}
```

`region` uses normalized `[left, top, right, bottom]` coordinates. If an object cannot be identified, use `null` for its ID/name and explain the region.

## Guardrails

- No evidence-free subjective preferences.
- No Critical/High visual finding when rendering or font fidelity is uncertain.
- No finding based solely on an off-canvas/hidden object.
- Alternatives and WIP are `Needs decision`, not automatic High findings.
- Blank final back-cover layouts are accepted when template/background/logo evidence supports that role.
- Every visual finding links to slide-level render evidence.
