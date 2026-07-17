---
name: create-brand-social-media-assets
description: Create on-brand Oliver Wyman social media assets without needing the Figma file. Use for HTML, web, static image, banner, story, portrait, square, thumbnail, or video-format assets that need concrete brand dimensions, colors, typography, spacing, and layout rules from the design-system variables.
---

# Create Brand Social Media Assets

## Purpose

Create social media assets from bundled design-system values. This skill is intended for agents that do not have the Figma file available.

## Required References

Read these before creating an asset:

- `references/social-media-spec.md`: concrete dimensions, colors, typography, spacing, and layout constants.
- `references/token-hierarchy.md`: source collections and primitive foundations.
- `references/asset-rules.md`: production rules, HTML/CSS guidance, and fallback behavior.

Use these references as the source of truth. Do not ask for Figma unless the user explicitly wants live-file inspection or updates.

## Workflow

1. Identify the requested asset type: `banner`, `portrait`, `story`, `square`, `thumbnail`, or `video`.
2. Use the exact canvas size, aspect ratio, margin, and gutter from `social-media-spec.md`.
3. Choose a composition pattern: brand-led, text-led, stat-led, quote-led, CTA-led, or media-led.
4. Apply concrete color, typography, logo, divider, spacing, and media rules from the references.
5. Build the asset in the requested medium, such as HTML/CSS, SVG, canvas, PNG, or a Figma frame if available.
6. Verify dimensions, text hierarchy, color contrast intent, and safe-area spacing before finishing.

## Non-Negotiables

- Use `#000F47` as the primary brand blue.
- Use `#FFBF00` as the primary accent gold.
- Use Marsh Serif for headings, quotes, stats, CTA headings, and monograms.
- Use Noto Sans for body, eyebrow, labels, and CTA body copy.
- Keep letter spacing at `0`.
- Use exact canvas dimensions and margins for each asset type.
- Do not invent alternate brand colors, type sizes, or format dimensions.

## Output Expectations

When finishing, report:

- Asset type and final dimensions.
- Main colors and typography roles used.
- Any manual fallbacks.
- File path or preview URL when an artifact was created.
