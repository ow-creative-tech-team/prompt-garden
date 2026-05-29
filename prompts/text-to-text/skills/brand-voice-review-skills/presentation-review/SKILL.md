---
name: presentation-review
description: Review Oliver Wyman presentations, PowerPoint decks, slide text, rendered slide images, screenshots, PDFs, and extracted PPTX text for AP Style, brand voice, naming, narrative flow, cognitive load, visual identity, template signals, typography, color, logo and endorsement usage, charts, tables, accessibility, and delivery readiness.
---

# Presentation Review

Use this skill for full decks, individual slides, rendered slide images, screenshots, PDFs, or extracted slide text. Review editorial quality, executive narrative, cognitive load, and visual brand compliance only when the relevant evidence is inspectable.

## Workflow

1. Identify the input type: `.pptx`, PDF, rendered slide image, screenshot, extracted slide text, or pasted slide copy.
2. Load `references/reviewer-prompt.md` for the full presentation review standard.
3. Load `references/brand-voice.md` for voice, copy, house style, and naming rules.
4. Load `references/brand-visual.md` only when visuals, screenshots, rendered slides, or PPTX package metadata are inspectable.
5. Load `references/review-output-template.md` when a compact findings format is needed.
6. For `.pptx` files, run the bundled scripts before making package-level claims:
   - `scripts/extract_pptx_text.py`
   - `scripts/inspect_pptx_package.py`
7. Review in this order: AP Style and brand writing, slide headlines and body copy, narrative flow, cognitive load, visual-text fit, visual brand compliance, global readiness, and accessibility.

## Guardrails

- Do not mark fonts, theme colors, logo files, master layouts, charts, tables, imagery, or rendered visuals as compliant unless they were directly inspected.
- If only extracted text is available, perform editorial and narrative review and state visual checks as not assessable.
- Preserve the presenter's intent and suggest concise, slide-ready revisions.
- Order findings by severity and include slide number and element whenever possible.

## Practical Commands

Extract slide text:

```bash
python3 scripts/extract_pptx_text.py path/to/deck.pptx
```

Inspect PPTX package metadata:

```bash
python3 scripts/inspect_pptx_package.py path/to/deck.pptx
```

## Output

Use the `## Presentation Review Summary` format from `references/reviewer-prompt.md`, or the compact format in `references/review-output-template.md` when the user asks for a shorter review.
