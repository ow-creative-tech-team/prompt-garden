---
name: powerpoint-proofing
description: Findings-only proofing for existing PowerPoint decks, single slides, screenshots, PDFs, or slide text. Reports copy, brand, layout, typography, color, chart, table, shape, cover-slide, and template issues directly in the response, with an optional proofing report PDF or HTML artifact. Does not edit, rewrite, generate, or deliver corrected decks.
---

# PowerPoint Proofing

## Purpose

Audit existing PowerPoint material against presentation proofing rules and return a clear list of issues for the user or designer to fix. This skill is for findings-only proofing, not deck correction, slide generation, redesign, or PowerPoint file production.

Hard boundary:

- Do not modify, save, export, or deliver a corrected `.pptx`, `.ppt`, slide image, PDF export of revised slides, or replacement deck.
- Do not apply patches. The helper script must expose extraction/reporting only.
- Do not rewrite slides, tables, charts, speaker notes, or visual layouts.
- Do not present proposed wording or design adjustments as completed changes.
- If the user asks for an edited deck, explain that this skill reports proofing findings only and can list exact issues plus required actions.
- Report artifacts are allowed only when they contain the same proofing findings as the chat response. They must never be revised decks or slide exports.

## Designer Prompt

Use this default prompt when a designer wants a full proofing pass:

```text
Use $powerpoint-proofing to proof this PowerPoint deck against the presentation proofing rules. Put the full findings directly in the response and, if useful, create a proofing report PDF or HTML artifact. Do not edit or create a corrected deck.
```

## Workflow

1. Identify the source input and scope.
   - Accept `.pptx`, `.ppt`, screenshots, PDFs, exported slide images, or pasted slide text.
   - For `.ppt`, ask for `.pptx` when package/style inspection is needed and no local converter is available.
   - For original/input deck plus designed/output deck, compare source content against designed content before other checks.
   - For a selected slide, inspect only that slide unless the user asks for deck-wide consistency checks.
   - For screenshots, PDFs, or pasted text, proof only the visible content and state any checks that require source deck metadata.
2. Select proofing references.
   - Use explicit user rules first.
   - For spelling, grammar, punctuation, terminology, capitalization, voice, numbers, currency, acronyms, and copy rules, use explicit user rules first and the conservative writing defaults in `references/visual-guidelines.md`.
   - For font, size, brand color, cover, chart, table, shape, and line compliance, read `references/brand-guidelines.md`.
   - For template, layout, cover, chart, table, shape, color, line, arrow, placeholder, and design-principle checks, read `references/visual-guidelines.md`.
   - If the user asks for scoring, use only explicit user-provided scoring criteria; otherwise report findings without numeric scores.
   - Convert brand rules into concrete checks: preferred terms, prohibited terms, exact capitalization, trademark/product naming, required phrasing, banned phrasing, logo/layout/color requirements, slide canvas/background rules, object color rules, and protected copy.
   - For color checks, distinguish the slide canvas/background fill from shapes, charts, tables, illustrations, images, and text. The canvas/background may use only the approved core background colors in `visual-guidelines.md`; secondary colors are evaluated only as in-slide content/object colors.
   - If rules conflict, follow explicit user rules first and flag the conflict as an unresolved finding.
3. Inventory the deck before judging it.
   - Use extraction only. Do not create patch JSON or output decks.
   - Use `scripts/pptx_text.py extract <deck.pptx> --format markdown` for a readable transcript.
   - For Brand, Discipline, typography, color, cover, chart, table, shape, or line checks, extract explicit style metadata:

```bash
python3 scripts/pptx_text.py extract input.pptx --format markdown --include-style
```

   - Use JSON extraction only when structured review is needed:

```bash
python3 scripts/pptx_text.py extract input.pptx --out deck-text.json
```

   - For visual proofing, inspect rendered slides when a local rendering path is available. If only OOXML inspection is possible, state which visual rules could not be verified.
   - Do not report Brand or Discipline checks as clean unless font, size, text color, slide background/canvas fill, shape fill, line, and slide-size metadata were inspected or the limitation is explicitly reported.
4. Proof slide by slide.
   - Treat slide fragments, labels, headings, table cells, chart labels, callouts, and speaker notes in scope as presentation copy.
   - Flag spelling, duplicated words, grammar, punctuation/spacing, capitalization, terminology, number/currency, and protected-language issues as findings.
   - Flag brand, typography, color, chart, table, shape, line, cover, template, and layout noncompliance as findings.
   - Report slide canvas/background violations separately from object color violations. Do not call a compliant canvas noncompliant because shapes, chart fills, table fills, or illustrations use secondary colors; evaluate those object colors against the approved palette and usage rules instead.
   - Preserve meaning in the recommendation: do not invent claims, change numbers, alter labels, reinterpret legal text, or revise source wording beyond the rule violation being reported.
   - Do not flag subjective preferences unless they violate a supplied rule, the deck's own pattern, or the default proofing references.
5. Classify each finding.
   - `Critical`: content omission, incorrect number/date/name, legal/compliance risk, unreadable text, or major brand/template failure.
   - `High`: visible typo, brand violation, wrong font/color/logo usage, chart/table error, or slide-level layout issue likely to affect delivery quality.
   - `Medium`: consistency, punctuation, hierarchy, spacing, alignment, or formatting issue that should be fixed before delivery.
   - `Low`: minor polish issue with limited delivery risk.
   - `Unresolved`: conflicting rules, ambiguous source wording, missing brand evidence, or checks blocked by input limitations.
6. Verify the review.
   - Re-check slide numbers and object contexts before reporting.
   - Spot-check protected terms, numbers, dates, citations, legal wording, chart labels, and names.
   - Confirm that no final response claims edits were applied or a corrected deck was produced.
   - Report any inspection limits, such as no rendered slide review, no source `.pptx`, missing brand assets, unavailable font metadata, or screenshot-only input.
7. Prepare user-friendly output.
   - Put the complete proofing findings directly in the model response. Do not provide only a file path, attachment, or external report.
   - For full-deck reviews, or when the user asks for something shareable, also create a proofing report artifact if the environment supports file creation.
   - Prefer a PDF report. If PDF creation is unavailable, create a standalone HTML report that opens in a browser.
   - Name report artifacts clearly, for example `deck-name-proofing-report.pdf` or `deck-name-proofing-report.html`. Do not use `proofed`, `revised`, `corrected`, or similar names that imply the deck was changed.
   - The report artifact must contain the same findings and review limits as the chat response.

## Output Standards

- Deliver findings directly in the chat response. The response must be complete without requiring the user to open a file.
- Deliver findings only. Do not attach or create edited PowerPoint files, revised slide exports, or corrected decks.
- A separate PDF or HTML proofing report may be created for sharing. It must be a report, not a revised deck, and must duplicate the chat findings.
- Group findings by slide number. Include a deck-level section only for issues that apply across multiple slides.
- Deck-level findings must still be actionable: name the affected slides and available object/shape names, and include the observed value for each instance when metadata is available.
- Avoid vague quantity-only wording such as "several lines" or "some shapes" unless followed by a concrete evidence list.
- Separate copy/content findings from brand/visual/template findings when both are in scope.
- For Brand and Discipline assessments, mention whether style metadata and rendered slide review were available.
- Include unresolved questions only for genuinely ambiguous, blocked, or rule-conflicting items.
- If no issues are found in scope, say that clearly and state the evidence reviewed.

Use this final response structure:

```text
Proofing findings

Deck-level
- Severity: ...
- Area: ...
- Issue: ...
- Rule: ...
- Required action: ...

Slide 1 - Cover
- Severity: High
- Area: Brand / cover
- Issue: Cover title appears in ALL CAPS.
- Rule: Do not use ALL CAPS on the cover.
- Required action: Convert the title to sentence case while preserving the approved cover layout.

Slide 4 - Chart
- Severity: Medium
- Area: Chart / color
- Issue: Chart labels use a non-approved accent color.
- Rule: Use Midnight Blue #000F47 for chart text.
- Required action: Set chart title, axis labels, legend, and data labels to Midnight Blue #000F47.

Review limits
- Rendered slide review unavailable, so visual findings are based on OOXML/text inspection.
```

## Script

`scripts/pptx_text.py` is a standard-library helper for inspecting visible slide text, optional speaker notes, and optional style metadata:

- Use `extract` for Markdown or JSON inventories with slide numbers, part paths, paragraph ids, shape names, text-node indexes, and available style metadata.
- It does not provide patching, applying, or verification commands. This is intentional.

Run `python3 scripts/pptx_text.py extract --help` for extraction options.

`scripts/report_artifact.py` creates optional proofing report artifacts from the final report text:

```bash
python3 scripts/report_artifact.py proofing-report.md --out proofing-report.pdf
python3 scripts/report_artifact.py proofing-report.md --out proofing-report.html
```

Use it only for report artifacts. Do not use it to export, render, or revise slide content.
