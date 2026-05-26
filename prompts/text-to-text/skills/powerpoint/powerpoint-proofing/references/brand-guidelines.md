# PowerPoint Brand Guidelines

Use this reference for findings-only brand compliance checks involving typography, type size, colors, logos, covers, charts, tables, shapes, and lines. These rules come from the supplied proofing brief and sanitized presentation rules. Put brand findings directly in the response; an optional report artifact may duplicate them for sharing.

## Required Inspection

For `.pptx` files, run style extraction before judging Brand or Discipline:

```bash
python3 scripts/pptx_text.py extract input.pptx --format markdown --include-style
```

Use the style inventory to inspect:

- Slide size and 16:9 setup.
- Text font face, size, weight, and color.
- Slide background/canvas fill color, including master/background fills when available.
- Shape fill colors.
- Chart, table, illustration, and other in-slide object colors when available.
- Line width, line color, and arrow endings.
- Cover title sizing and all-caps usage.

Also inspect rendered slides when available. If inherited placeholder styles or template component names are not visible in extracted metadata, report that limitation instead of calling the brand check clean.

## Typography

- Headline font: Marsh Serif.
  - Use for headlines, section titles, large quotes/statements, large numerals, and key figures.
  - Use at generous scale only for short statements, key words, or important numbers.
  - Approved styles shown: Regular 400 normal and Italic 400 italic.
- Supporting font: Noto Sans.
  - Use for subheads, captions, body copy, paragraphs, supporting labels, and data points.
  - Approved weights/styles shown: 300, 400, 500, and 700, normal and italic.
- Alternative script font: Noto Serif for writing systems Marsh Serif does not support.
  - Japanese: Noto Serif JP.
  - Korean: Noto Serif KR.
  - Simplified Chinese: Noto Serif SC.
- System fallbacks:
  - Headlines: Georgia Pro Light, or Georgia when limited to legacy fonts.
  - Body copy: Arial if Noto Sans is unavailable.
- Typesetting principles: clarity first, consistent rhythm, purposeful hierarchy.
- Use sentence case.
- Text should predominantly appear in Midnight Blue, Sky Blue, or White.
- Traffic colors may be used selectively for positive/negative data.
- Do not change cover fonts or cover text colors.
- Cover title maximum size for short titles:
  - 66 pt on covers without a photo.
  - 54 pt on covers with an image.
- Long cover titles should not be oversized or visually aggressive; flag them when size or hierarchy looks excessive.
- If an affiliate name must appear on the cover, place it in the upper-right corner using Noto Sans, 14 pt, Regular, not bold.
- For charts and add-in charts, typography must match the deck's approved color scheme and template typography.

## Color Rules

Use only approved brand palette colors. Compare extracted `srgb` values directly to the approved HEX values. For extracted `scheme` colors, use the extracted theme color mapping when available.

Evaluate slide canvas/background fills separately from in-slide objects:

- Slide canvas/background means the slide background or master/background fill, not shapes, charts, tables, illustrations, images, or text boxes.
- Slide canvas/background fills may use only core background colors: White `#FFFFFF`, Sky Blue `#CEECFF`, or Midnight Blue `#000F47`.
- Secondary colors are allowed only inside slide content when functional, for example data visualization, illustrations, highlights, small accents, or semantic status indicators. They must use exact approved palette values and should not become the primary slide background.
- If the slide canvas is compliant but in-slide objects use off-palette colors, report an object/shape/chart/table color issue rather than a background issue.

- Core palette:
  - Midnight Blue 1000: `#000F47` / RGB `0, 15, 71`.
  - Sky Blue 250: `#CEECFF` / RGB `206, 236, 255`.
  - White: `#FFFFFF` / RGB `255, 255, 255`.
- Secondary palette:
  - Gold 1000: `#CB7E03` / RGB `203, 126, 3`.
  - Gold 750: `#FFBF00` / RGB `255, 191, 0`.
  - Gold 500: `#FFD98A` / RGB `255, 217, 138`.
  - Gold 250: `#FFF3DA` / RGB `255, 243, 218`.
  - Active Blue 750 / Electric Blue: `#0B4BFF` / RGB `11, 75, 255`.
  - Blue 500: `#82BAFF` / RGB `130, 186, 255`.
  - Green 1000: `#2F7500` / RGB `47, 117, 0`.
  - Green 750: `#6ABF30` / RGB `106, 191, 48`.
  - Green 500: `#B0DC92` / RGB `176, 220, 146`.
  - Green 250: `#DFECD7` / RGB `223, 236, 215`.
  - Purple 1000: `#5E017F` / RGB `94, 1, 127`.
  - Purple 750: `#8F20DE` / RGB `143, 32, 222`.
  - Purple 500: `#DEB1FF` / RGB `222, 177, 255`.
  - Purple 250: `#F5E8FF` / RGB `245, 232, 255`.
- Neutral palette:
  - Neutral 1000: `#3D3C37` / RGB `61, 60, 55`.
  - Neutral 750: `#7B7974` / RGB `123, 121, 116`.
  - Neutral 500: `#B9B6B1` / RGB `185, 182, 177`.
  - Neutral 250: `#F7F3EE` / RGB `247, 243, 238`.
- Traffic colors:
  - Success green: `#2F7500` / RGB `47, 117, 0`.
  - Danger crimson: `#C53532` / RGB `197, 53, 50`.
  - Warning yellow: `#FFBE00` / RGB `255, 190, 0`.

Usage rules:

- Slide canvas/background fills: White `#FFFFFF`, Sky Blue `#CEECFF`, or Midnight Blue `#000F47` only.
- Cover backgrounds: White, Sky Blue, or Midnight Blue.
- Chart text: Midnight Blue `#000F47` for all chart text.
- Table highlights:
  - Subtle: Neutral 250 `#F7F3EE`, Sky Blue `#CEECFF`.
  - Bold: Gold 750 `#FFBF00`, Active Blue/Electric Blue `#0B4BFF`.
- Shape primary colors: Neutral 250 `#F7F3EE`, Sky Blue `#CEECFF`, Midnight Blue `#000F47`.
- Gold is an action/highlight color; Gold 750 should be used sparingly.
- Yellow/Warning Yellow and Active Blue are reserved only for highlighting important information.
- Purple and green: controlled secondary colors; in charts, they should not be primary chart colors.
- Traffic colors are only for positive/negative/warning data semantics.

Avoid:

- Non-core colors as the slide canvas/background.
- Arbitrary custom colors or tints.
- Client colors unless the rule explicitly allows them.
- Random colors in charts, tables, shapes, or deemphasis text.
- Highlight colors as main colors.
- Highlight colors for main text.
- Accent 2 for large text blocks because it has insufficient contrast with white or Midnight Blue text.
- Low contrast against the background.
- New colors, gradients, transparency, and effects.

## Cover And Logo Rules

- Follow the standard cover layout and element placement.
- Use only approved cover background options: White, Sky Blue, or Midnight Blue.
- Do not alter cover line spacing.
- Do not use ALL CAPS on the cover.
- Do not resize the primary logo.
- Do not reposition title or subtitle.
- Do not resize the cover image placeholder.
- Do not create new photo cover layouts outside the provided system.
- Do not adjust cover colors to match a cover image, client branding, or topic.
- Client logo, if present, must be similar in size to and never larger than the primary logo.
- Client logo should be visually top-aligned with the primary logo and right-aligned to the slide's right margin.

## Tables, Shapes, Lines, And Arrows

- Use approved table styles from the template's Table Styles library.
- Header or top-row table text should be bottom-aligned.
- Remaining table cells should preferably be top- and left-aligned.
- Use yellow text in tables only on dark backgrounds.
- Shape fills should use approved shape colors unless the shape is a dedicated highlight sticker.
- Line thickness should be 0.75 pt.
- Do not use filled arrow tips.

## Finding Examples

```text
Slide 1 - Cover
- Severity: High
- Area: Brand / cover
- Issue: Cover title is 72 pt.
- Rule: Short cover titles may be up to 66 pt without a photo or 54 pt with an image.
- Required action: Reduce the cover title to the approved template size.

Slide 4 - Chart
- Severity: Medium
- Area: Brand / chart color
- Issue: Chart labels use scheme accent2 resolved to #8F20DE.
- Rule: All chart text should be Midnight Blue #000F47.
- Required action: Set chart title, axis labels, legend, and data labels to Midnight Blue #000F47.

Slide 6 - Shape
- Severity: Medium
- Area: Brand / shape color
- Issue: Shape fill uses #FF00FF, which is not one of the approved shape colors.
- Rule: Primary shape colors are Neutral 250 #F7F3EE, Sky Blue #CEECFF, and Midnight Blue #000F47; highlight colors are reserved for emphasis.
- Required action: Replace the fill with an approved template color.
```
