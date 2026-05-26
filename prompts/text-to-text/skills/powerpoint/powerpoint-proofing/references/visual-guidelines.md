# PowerPoint Visual Guidelines

Use this reference when the user asks to proof a deck against visual, template, layout, chart, table, shape, or cover-slide rules.

- These are **review criteria for existing PowerPoint decks**.
- **Report issues as findings only** (do not apply edits or redesigns).
- Put visual findings directly in the response; an optional report artifact may duplicate them for sharing.

---

## Proofing Approach

1. **Confirm scope**: whole deck, selected slides, cover only, charts/tables only, or another findings-only scope.
2. **Inspect the actual deck** when possible.
   - Prefer rendered slides for visual checks.
   - Use OOXML/package inspection for properties when rendering is unavailable (slide size, fonts, color fills, line styles, theme references, object metadata).
3. Treat **exact user-provided rules** as authoritative. Use these defaults only when the user asks for generic visual guideline proofing or supplies this rule set.
4. **Do not make deterministic fixes**, even when the source deck is available and the correction is unambiguous. Report a finding with slide number, issue, rule, and required action.
5. **Preserve template structure** in recommendations. Do not invent new layouts, colors, crops, chart styles, or visual systems.

Implementation note: for brand-specific checks, use the extracted style metadata when available (e.g., a text extraction pipeline that includes font, size, color, level/indent, and shape/chart/table styling).

---

## Template Setup

- Use the approved PowerPoint template and the appropriate template variant for the context:
  - **Default** for general use.
  - **White** for printing.
  - **Dark** for on-screen presentations.
- Use a **16:9** aspect ratio.
- Do not export revised slide PDFs under this skill. PDF output, when created, is a **proofing report artifact only**.

### PDF export (brand quality)
When saving a deck as PDF for sharing, prefer **Export → Create Adobe PDF** to avoid font rendering or pixelation issues.

---

## Color

### Core palette (primary / default)
Lead with these for brand recognition.

| Role | Name | HEX | RGB | Notes |
|---|---|---:|---:|---|
| Core | Midnight Blue (1000) | #000F47 | 0, 15, 71 | Main dark text/background |
| Core | Sky Blue (250) | #CEECFF | 206, 236, 255 | Main light accent/background |
| Core | White | #FFFFFF | 255, 255, 255 | Main background/text |

### Slide background rule (PowerPoint slide canvas)
This rule applies **only to the slide background/canvas** (i.e., the master/background fill), not to shapes, tables, charts, or images.

**Permitted slide background colors (canvas only):**
- **White (#FFFFFF)**
- **Sky Blue (#CEECFF)**
- **Midnight Blue (#000F47)**

**Non-compliant slide backgrounds:** any other solid background color, custom tints, client brand colors, “matched to image” backgrounds, gradients, transparency effects, textures.

### Secondary palette (controlled use for objects, not slide canvas)
Secondary colors may be used to support hierarchy and clarity, especially in **data visualization** and **illustrations**, but use is intentionally limited.

> Note: Secondary colors are allowed **inside slide content** (charts, tables, illustrations, small accents). They should **not** be used as the **slide background/canvas**.

**Golds**
- Gold 1000 — **#CB7E03** (RGB 203, 126, 3)
- Gold 750 — **#FFBF00** (RGB 255, 191, 0) → **active / highlight**
- Gold 500 — **#FFD98A** (RGB 255, 217, 138)
- Gold 250 — **#FFF3DA** (RGB 255, 243, 218)

**Blues (additional)**
- Blue 750 (Active) — **#0B4BFF** (RGB 11, 75, 255)
- Blue 500 — **#82BAFF** (RGB 130, 186, 255)

**Greens (use sparingly)**
- Green 1000 — **#2F7500** (RGB 47, 117, 0)
- Green 750 — **#6ABF30** (RGB 106, 191, 48)
- Green 500 — **#B0DC92** (RGB 176, 220, 146)
- Green 250 — **#DFECD7** (RGB 223, 236, 215)

**Purples (use only when needed for complex datasets)**
- Purple 1000 — **#5E017F** (RGB 94, 1, 127)
- Purple 750 — **#8F20DE** (RGB 143, 32, 222)
- Purple 500 — **#DEB1FF** (RGB 222, 177, 255)
- Purple 250 — **#F5E8FF** (RGB 245, 232, 255)

**Neutrals (structure / dividers / subtle fills)**
- Neutral 1000 — **#3D3C37** (RGB 61, 60, 55)
- Neutral 750 — **#7B7974** (RGB 123, 121, 116)
- Neutral 500 — **#B9B6B1** (RGB 185, 182, 177)
- Neutral 250 — **#F7F3EE** (RGB 247, 243, 238)

### Traffic colors (semantic status only)
Use traffic colors to convey meaning at a glance in data (not as general decoration).

- **Success green:** #2F7500
- **Warning yellow:** #FFBE00
- **Danger crimson:** #C53532

### Highlight vs. status colors (clarification)
To avoid confusion between **Gold 750** and **Warning yellow**:

- **Gold 750 (#FFBF00)** is the preferred **non-semantic highlight** color (call-outs, emphasis). Use sparingly.
- **Warning yellow (#FFBE00)** is reserved for **semantic status** meaning (e.g., RAG / risk warnings) and should not be used as general decoration.

### Color do/don’t checks
**Do**
- Lead with core colors (Sky Blue + Midnight Blue + White).
- Use **Gold 750** sparingly as an action/highlight color.
- Keep white space generous.
- Use colors intentionally (hierarchy, emphasis, meaning).

**Don’t**
- Don’t use too many colors at once.
- **Don’t create new colors**.
- **Avoid gradients, transparency, or effects**.
- Don’t use client colors or off-brand colors in charts/tables.
- Don’t use any non-core color as the **slide background/canvas**.

### Accessibility / contrast
Ensure sufficient contrast for on-screen text in buttons, charts, and tables. When possible, validate against **WCAG 2.1** contrast expectations.

---

## Typography

### Approved typefaces
**Headline font:** *Marsh Serif*
- Use for headlines, section titles, large quotes/statements, large numerals/key figures.

**Supporting font:** *Noto Sans*
- Use for subheads, captions, body copy, supporting labels/data points.

### Case and color guidance (clarified)
- Use **sentence case**.
- Text should predominantly appear in **Midnight Blue, Sky Blue, or White**.
- **Exceptions (allowed when functional):**
  - Traffic colors for semantic status (positive/negative/RAG) in data contexts
  - Table-specific contrast cases (see Tables section)

### Typesetting principles (what to enforce)
- **Clarity first:** maximum legibility, clean alignment, balanced spacing.
- **Consistent rhythm:** consistent line spacing, letter spacing, and alignment.
- **Purposeful hierarchy:** size/weight/color guide attention; use Marsh Serif to create emphasis moments.
- **Create impact:** large-scale Marsh Serif for short statements, key words, important numbers.

### Quote marks (special brand element)
- Quote marks are created from the **Marsh symbol**.
- Use quote marks only when they create **clear visual impact**.
- **Always use the approved quote mark artwork** in core colors.
- **Do not recreate or modify** quote marks.
- Quote marks must **touch the top and bottom edges** of the screen/canvas/frame.

**Fallback behavior**
- If approved graphic quote artwork cannot be used:
  - Use **Marsh Serif** quotation marks for headline quotes.
  - Use **Noto Sans** quotation marks for body copy.

### Font fallbacks (localization and system limitations)
- If Marsh Serif does not support a script, use **Noto Serif** (e.g., JP/KR/SC variants).
- If only system fonts are available:
  - Headlines: **Georgia Pro Light** (or **Georgia**)
  - Body: **Arial**

### Typography don’ts
- Avoid overly tight or loose leading.
- Avoid substitute serif/sans fonts.
- Avoid previous typefaces (explicitly: **MMC Display**).
- **Do not** use Marsh Serif for body copy.

---

## Logo

- Use approved logo files only. Do not stretch, distort, rotate, recolor, or apply gradients, shadows, or effects.
- Color version selection:
  - Midnight Blue on light solid or photographic backgrounds.
  - Sky Blue only in Midnight Blue layouts where surrounding typography is also Sky Blue.
  - White on dark backgrounds.
  - Black only for true black-and-white technical output.
- Maintain clear space equal to the cap-height of the logo on all sides.
- Preferred placement is top-left, aligned to margins. Other corners are permitted for composition.
- Centered placement is acceptable only when the logo is the hero element.
- Do not rearrange or alter any part of the “A Marsh business” endorsement lockup.
- Avoid busy or low-contrast backgrounds behind the logo.
- Sub-business names such as Innopay, Veritas, and Vector are descriptors set in Noto Sans, clearly separated from the logo. They do not get their own logo.
- Third-party logos must be at equal visual weight to the primary logo, separated by a 1 pt Midnight Blue rule, and aligned horizontally or vertically.

---

## Cover Slides (high-priority proofing)

### Must-follow cover constraints
- Follow the standard cover layout and element placement.
- **Do not** alter line spacing.
- **Do not** use ALL CAPS on the cover.
- Use only predefined cover background options: **White, Sky Blue, or Midnight Blue**.
- Do not change cover font or text color.
- Do not adjust cover colors to match an image, client branding, or topic.
- Do not resize the primary logo.
- Do not reposition the title or subtitle.
- Do not resize the cover image placeholder.
- Do not create new photo cover layouts outside the template system.
- When using a photo, keep the crop intentional within the frame.

### Cover title sizing guidance
- If title is short:
  - Up to **66 pt** on covers without a photo
  - Up to **54 pt** on covers with an image
- Do not make long titles too large.

### Client logo constraints (if present)
- Client logo should be similar in size to the primary logo, but **never larger**.
- Client logo should be:
  - Visually **top-aligned** with the primary logo
  - **Right-aligned** with the slide’s right margin

### Affiliate handling (if required)
Do not add subsidiary or affiliate endorsements to the primary logo. If an affiliate must appear on the cover, place the affiliate name in the upper-right corner using **Noto Sans, 14 pt, Regular**.

---

## Layouts and Placeholders

- Use provided template layouts for covers, section dividers, standard legal or administrative slides, back covers, CV slides, one-pagers, and column placeholder combinations.
- Do not create separate heading placeholders. Create headings by adjusting list indentation levels or using text style tools.

### Text styles & indentation levels (PowerPoint)
The template does not rely on distinct placeholders for headings; headings are created via indentation/text style levels:

- **Level 1:** body text
- **Levels 2–4:** bullet points
- **Levels 5–6:** headings and subheadings
- **Levels 7–9:** big headlines (**quotes** or **big numbers** only)

**Proofing checks**
- Big-headline levels (7–9) used only for quote/big-number slides.
- Avoid “manual formatting” that breaks style consistency.

### Consistency across layouts
Structural slides (cover, section, agenda, back cover) should share the **same style** for coherence.

**Proofing checks**
- Structural slides use a consistent color scheme.
- No arbitrary switching between template variants mid-deck without intent.

---

## Charts (PowerPoint + think-cell)

### Allowed chart creation methods
- Native PowerPoint charts
- think-cell add-in charts

They are not fully compatible, but must follow the same **color scheme and typography**.

### Chart text color rule
Ensure **Midnight Blue** is used for **all chart text** (axes, labels, titles), not a theme accent.

### Chart color usage guidance
- For complex charts you may use additional colors.
- **Purple and green are secondary** and should not be primary chart colors.
- When using multiple colors, **group them in sets of 2–3** to create smoother gradations.
- Use color intentionally for **highlight vs. deemphasis**.

### Chart don’t checks
- Avoid using colors randomly.
- Avoid low contrast against the background.
- Avoid client colors and non-brand colors.

### Add-in arrow note (think-cell)
If arrow-end formatting is needed and think-cell doesn’t provide it directly: **Tools → Match Size → Unify Arrows**.

---

## Tables

### Allowed table styles
There are **four** table styles in the template’s Table Styles library.

Apply styles by right-clicking and choosing **Apply (and Clear Formatting)**.

### Table text alignment rules
- Top row/header text: **bottom-aligned**
- Other cells: preferably **top and left** aligned
- Middle alignment: allowed selectively for graphic elements (e.g., Harvey balls, flags)

### Table style caution
Avoid using **Style 3** (Midnight Blue header) in text-heavy tables with colored cells and a legend if the header is not the most important element.

### Highlights in tables
- Subtle: **Neutral 250** and **Sky Blue**
- Bold highlight: **Gold 750** and **Active Blue**

**Contrast rule (clarified):**
- Use **yellow text** in tables **only on dark backgrounds**.
- Prefer **White** text on dark backgrounds where possible; use yellow only when it improves clarity without changing meaning.

### Table don’t checks
- Avoid random custom colors and tints.
- Avoid client colors.
- Avoid modifying banded-row colors (contrast risk).

---

## Shapes

### Shape defaults
- Default shape fill is **Neutral 250** (except the highlight sticker).

### Preferred shape colors
Primary shape choices:
- **Neutral 250**
- **Sky Blue**
- **Midnight Blue**

Avoid using “Accent 2” for large blocks of text due to insufficient contrast with white or Midnight Blue text.

**Highlight-only colors:**
- Yellow
- Active Blue

### Shape don’t checks
- Don’t use highlight colors as the main fills.
- Don’t use random custom/off-brand colors for highlighting or deemphasis.

---

## Lines and Arrows

- Line thickness: **0.75 pt**.
- Use lines to create hierarchy or separate elements (e.g., body text from a quote).
- Arrow rule: **do not use filled arrow tips**.
- When reporting line thickness or arrowhead issues, identify each affected slide and available object/shape name, with the observed value. If the pattern is deck-wide, summarize once but include an evidence list, for example: `Slide 3 - Connector 12: 1.0 pt; Slide 5 - Straight Connector 8: 0.5 pt`.

---

## Illustration

- Three types:
  - **Explainer** (clarifies and simplifies information)
  - **Symbolic** (signals and orients the viewer)
  - **Metaphorical** (expresses a specific insight)
- Use Explainer for products, how-it-works diagrams, instructions, and internal communications.
- Use Symbolic to introduce an idea with shared visual language.
- Use Metaphorical for high-stakes or defining moments.
- Style rules: combine color fills with outlined shapes; keep compositions simple and balanced with clear hierarchy; use a limited palette from core colors, neutrals, and one secondary color.
- Do not use multiple secondary colors in a single illustration.
- Do not use a secondary color as a background.
- Do not overuse outlines.
- Use pre-generated Explainer and Symbolic assets from the illustration library as provided. Do not modify, deconstruct, or recreate them independently.
- If no suitable asset exists, consult the Creative Studio team.

---

## Photography

- Photography is evidence, not decoration. Images should show expertise, perspective, and humanity.
- Three subject categories:
  - Industries and sectors (dramatic, expertise-driven)
  - People and lifestyle (honest, warm, connected — avoid staged or generic shots)
  - Conceptual and evocative (abstract or symbolic; meaning deepens with copy)
- Avoid images or icons of country flags.
- Style characteristics: photojournalistic, cinematic impact, single clear point of interest, authentic, open copy space, and unique vantage points.
- Retouching: apply subtle refinements only. Add gentle warmth for images with people; slightly increase saturation, vibrance, and contrast. Avoid heavy filters, over-saturation, and unrealistic warming of landscapes.
- Colleague portraits: centered framing, natural or diffused light, shallow depth of field, high contrast, medium-high saturation, warm tone. Simple solid wardrobe colors; avoid black, white, stripes, or busy patterns.
- Follow copyright requirements for all third-party images.

---

## Writing and Punctuation

- Follow the user's approved writing and punctuation style rules when supplied.
- If no organization-specific writing style is supplied, use conservative defaults for copy-editing.

---

## Proofing Checklist (quick rules for an automated agent)

### High-severity (should fail)
- Slide background/canvas fill is not **White / Sky Blue / Midnight Blue**.
- Fonts not using **Marsh Serif** (headlines) and **Noto Sans** (body/supporting), without an approved fallback case.
- Use of gradients/transparency/effects on brand colors.
- Cover slide elements repositioned/resized vs. template; primary logo resized.
- Client logo larger than primary logo (if present).
- Quote mark artwork recreated/modified; quote marks not touching top & bottom edges when used as the graphic element.
- Chart text not set to **Midnight Blue** (or otherwise inconsistent with rules).

### Medium-severity (should warn)
- Too many colors used on one slide/data viz.
- Overuse of Gold 750 (not “sparingly”).
- Green/purple used as primary chart colors.
- Tables not using one of the four styles / manual formatting.
- Poor contrast for text (potential WCAG issue).

### Low-severity (style guidance)
- Inconsistent spacing/leading/tracking.
- Misuse of big headline levels (7–9) outside quotes/big numbers.
- Excessive use of traffic colors outside performance/status contexts.

---

## Implementer Notes

- Many rules are easiest to enforce by checking **theme colors**, **font names**, **slide background fills**, **object fill colors**, **master layouts**, and **style level usage**.
- Contrast checking requires computing relative luminance for foreground/background (WCAG 2.1).

---

## Findings Boundary

Report visual issues as slide-level findings for the designer to fix in PowerPoint.

Do not auto-fix visual properties, create an edited deck, or present recommendations as completed corrections.

Report visual findings when:

- The correction depends on design judgment (hierarchy, balance, emphasis, white space, rhythm).
- Exact brand assets, inherited placeholder styles, or template component names are not available in the extracted metadata.
- The issue concerns image crop, logo placement, chart styling, table style, or layout drift and the exact intended value is unknown.
- The deck can only be inspected through screenshots, PDF, pasted text, or non-rendered OOXML.

---

## Finding Format

Use this format for visual issues:

```text
Slide 1 - Cover
- Severity: High
- Area: Brand / cover
- Issue: Cover title appears in ALL CAPS.
- Rule: Do not use ALL CAPS on the cover.
- Required action: Convert the title to sentence case while preserving the approved cover layout.

Slide 6 - Chart
- Severity: Medium
- Area: Chart / color
- Issue: Chart text appears in a theme accent color.
- Rule: Use Midnight Blue for all chart text.
- Required action: Set chart title, axis labels, legend, and data labels to Midnight Blue.
```
