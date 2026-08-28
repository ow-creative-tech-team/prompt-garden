---
name: powerpoint-proofing
description: Findings-only proofing for existing PowerPoint decks, with deterministic PPTX inspection, optional source-versus-designed comparison, visual review, delivery readiness, ownership attribution, and self-contained HTML/PDF reports. Never edits or produces corrected presentations.
---

# PowerPoint Proofing

Proof an existing presentation without changing it. The designer-facing prompt is simply:

```text
Proof this PowerPoint.
```

## Hard boundary

- Findings only. Never modify, patch, rewrite, save, or deliver a corrected presentation.
- Never use an editable-deck skill as part of this workflow.
- Chat must contain the complete findings. An HTML or PDF report may duplicate them.
- Do not assess Service from deck content and do not create a numerical scorecard.

## Defaults

Apply these without asking routine questions and show them at the top of every response/report:

- Stage: `pre_delivery`
- Audience: `internal`
- Language: `en-US`
- Scope: all slides
- Speaker notes: excluded
- Comments, hidden objects, and off-canvas objects: inventoried but excluded from readiness

Accept a designed `.pptx` and, when supplied, a source `.pptx`. For screenshots or PDFs, run visual/copy review only and mark OOXML-dependent coverage `Not assessed`.

## Required references

Read only what the task needs:

- `references/rules.json`: authoritative, versioned machine-readable rules.
- `references/rule-packet.md`: deterministic writing checks and attribution behavior.
- `references/brand-guidelines.md`: traceable Oliver Wyman PowerPoint rules and unsupported areas.
- `references/visual-guidelines.md`: visual-evidence protocol and model response contract.
- `references/proofing-levels.md`: severity, ownership, readiness, and coverage definitions.
- `references/finding-schema.json`: report/finding interchange schema.
- `references/pilot.md`: lightweight designer pilot and labelled-quality gates.

The full source guides are bundled as `references/Oliver-Wyman-Visual-Guidelines.md` and `references/writing-style-guide.md`. The shorter references are the operational subset. Approved logo masters used for exact-match checks are bundled in `assets/logos/`. User-supplied rules take precedence and conflicts become `Needs decision`.

## Workflow

### 1. Build the normalized inventory

For `.pptx`, run deterministic inspection first:

```bash
python3 scripts/pptx_text.py extract designed.pptx --out inventory.json
```

The inventory resolves slide order, slide/layout/master relationships, placeholders, theme and template colors, backgrounds, object types, geometry, z-order, group membership, canvas visibility, text runs, explicit styles, pictures, charts, tables, notes, and comments. PowerPoint break elements remain whitespace.

Do not treat `off_canvas`, `hidden`, `notes`, or `comment` content as delivered slide content. Off-canvas working material never affects readiness.

### 2. Compare source and designed decks

When a source deck is supplied:

```bash
python3 scripts/pptx_text.py compare source.pptx designed.pptx --out comparison.json
```

Use the one-to-many mapping candidates rather than assuming equal slide numbers. Normalize Unicode, case, whitespace, and line breaks for matching while preserving raw evidence. Protect numbers, currency, dates, percentages, URLs, citations, acronyms, and deliberate bold/italic emphasis.

Record ownership independently from severity for internal evidence and source comparison:

- `designer_introduced`
- `inherited_from_source`
- `requester_decision`
- `template_or_system`
- `unresolved`

### 3. Run deterministic review

```bash
python3 scripts/proofing_engine.py designed.pptx --source source.pptx --out review.json
```

Omit `--source` when none exists. The engine applies the visible defaults, validates source fidelity, runs traceable copy/style/geometry checks, creates stable finding IDs, and calculates readiness. It must not infer visual defects that require a rendered slide.

Line rules apply only when the rule's applicability matches the object role. A connector line is not interchangeable with a rectangle border, table border, or chart border. Template/theme-derived colors and components are valid when provenance is established.

Alternative covers, option labels, placeholders, and WIP artifacts become `Needs decision`; they are not automatically designer failures. Off-canvas instances have no readiness impact. A final template-derived back cover may contain no ordinary slide text and still be valid.

Requester sticky notes and directive working material such as `@DTP, please add…` are excluded from findings. Do not run copy, brand, typography, visual-defect, or readiness checks against the guidance object itself.

### 4. Render and run visual judgment

Render every slide with the presentation runtime. Inspect the actual slide pixels for hierarchy, density, alignment, contrast, whitespace, image treatment, crop, and clarity. Give the model:

1. the slide render;
2. the slide's structured inventory;
3. deterministic candidates and source mapping; and
4. the JSON contract in `references/visual-guidelines.md`.

Every visual finding needs slide-level evidence and an object ID/name when identifiable. If rendering or font substitution makes evidence uncertain, confidence must be reduced and the finding cannot be `Critical` or `High` on visual judgment alone.

Merge validated visual findings by passing them to the engine:

```bash
python3 scripts/proofing_engine.py designed.pptx --source source.pptx \
  --visual-findings visual-findings.json --renders rendered-slides --out review.json
```

### 5. Calculate readiness

- `Not ready`: a required fix or an in-frame content decision remains.
- `Ready after minor fixes`: only recommended improvements or optional polish remain.
- `Ready`: no open findings in assessed areas.

Readiness and ownership are separate. An inherited source error can block delivery; an off-canvas designer artifact cannot. Present findings to designers in these action groups: `Fix before delivery`, `Check with the content owner`, `Recommended improvements`, and `Optional polish`.

### 6. Report

Create the self-contained interactive HTML report for full-deck reviews:

```bash
python3 scripts/report_artifact.py review.json --out deck-proofing-report.html
```

The HTML starts with readiness and a compact action list, then groups findings by designer action. It includes slide thumbnails, priority/slide filters, stable IDs, collapsed technical evidence, coverage, limitations, and print styling. Generate a PDF only when requested:

```bash
python3 scripts/report_artifact.py review.json --out deck-proofing-report.pdf
```

## Chat contract

Use a balanced working-review format: concise enough to scan, but complete enough for a designer to act without opening the HTML report. Always provide:

1. delivery readiness, the number of required fixes/decisions, and which slides to address first;
2. every finding, grouped as `Fix before delivery`, `Check with the content owner`, `Recommended improvements`, or `Optional polish`;
3. a short plain-language description of what was reviewed; and
4. only the limitations that could change how the designer interprets or acts on a finding.

Never replace the complete findings with a `Key blockers` list or a list of slide labels and IDs. For every finding, include the slide and issue name plus these four labelled lines:

```markdown
### Slide 2 — Spelling

**Found:** “Markting”
**Action:** Change “Markting” to “Marketing”.
**Priority:** Fix before delivery
**Reference:** `PPT-002-E095CE3F`
```

Keep evidence specific and actions direct. For render-dependent findings, state what appears in the render and ask the designer to verify it in PowerPoint with the approved font before changing the layout. Do not promote uncertain font-substitution artefacts to confirmed blockers.

Translate review settings into natural language and place them after the findings. For example: `Reviewed before delivery for an internal, US-English presentation. All slides were reviewed; speaker notes were not included.` Do not expose values such as `pre_delivery`, `in_frame`, or `ownership=unresolved` in the default chat response.

When no source deck was supplied, say once that the review cannot determine where most issues originated. Keep object IDs, visibility, rule/version, confidence, ownership, readiness impact, and source comparison in the HTML report's collapsed `Review details` and in machine-readable output.

## Pilot validation

During the pilot, evaluate reviewed labels with `scripts/evaluate_labels.py review.json labels.json`. Do not claim the 95% precision or attribution gates until enough human-labelled findings pass them. The source repository contains the automated test suite; tests are not part of the distributed skill package.

Do not claim complete Brand coverage without an approved PowerPoint template and chart/table component examples. Bundled logo masters and licensed fonts support partial checks; exact rendered appearance and visually altered assets still require render evidence. Mark unsupported areas `Not assessed`.
