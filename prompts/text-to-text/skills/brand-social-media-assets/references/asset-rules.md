# Asset Rules

Use these rules for HTML, web, SVG, canvas, image, or Figma output.

## Offline Rule

Do not require access to the Figma file. The concrete values in `social-media-spec.md` are the source of truth.

## HTML/CSS Implementation

For web output:

- Create a fixed-size asset root using the exact dimensions for the requested type.
- Use CSS custom properties for brand values.
- Use absolute positioning or CSS grid inside the fixed canvas.
- Use `box-sizing: border-box`.
- Use the asset margin as the safe area.
- Export or screenshot at 1x unless the user requests another scale.

Recommended CSS base:

```css
:root {
  --ow-blue-1000: #000F47;
  --ow-blue-750: #0B4BFF;
  --ow-blue-250: #CEECFF;
  --ow-gold-750: #FFBF00;
  --ow-gold-1000: #CB7E03;
  --ow-neutral-1000: #3D3C37;
  --ow-neutral-750: #7B7974;
  --ow-neutral-500: #B9B6B1;
  --ow-neutral-250: #F7F3EE;
  --ow-white: #FFFFFF;
}

.asset {
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  background: var(--ow-white);
}
```

## Format Selection

Use:

- `banner`: 1080 x 512 for wide social or site-promotional crops.
- `portrait`: 1080 x 1350 for feed portrait posts.
- `story`: 1080 x 1920 for vertical stories or reels covers.
- `square`: 1080 x 1080 for standard feed posts.
- `thumbnail`: 640 x 640 for compact thumbnails.
- `video`: 1920 x 1080 for 16:9 video covers.

## Typography Use

- Use heading `lg` for hero headlines on story, portrait, square, and video.
- Use heading `md` when the asset has multiple content groups.
- Use heading `sm` for banner and thumbnail headlines.
- Use body `lg` sparingly; body `md` and `sm` are safer for dense copy.
- Use eyebrow above heading with an 8 px gap.
- Use quote roles only for quoted editorial content.
- Use stats roles for numeric proof points and keep supporting copy subordinate.

## Layout Use

- Keep all primary content inside the asset margin.
- Use standard section gap 40 for normal layouts.
- Use compact section gap 20 for dense banners and thumbnails.
- Use logo height 62 for standard layouts and 52 for compact layouts.
- Use divider line width 1.
- Keep logo and divider spacing at 31 standard or 26 compact.

## Color Use

- On light backgrounds, use `#000F47` for brand headings and body by default.
- On dark brand backgrounds, use `#FFFFFF` for primary text and `#CEECFF` for secondary brand text.
- Use `#FFBF00` for primary accent, CTA emphasis, and key highlights.
- Use `#3D3C37` for neutral body text when a softer non-brand tone is needed.
- Use `#F7F3EE` as a warm neutral surface.
- Do not create new tints or gradients unless the user explicitly asks for exploration.

## Media Use

The source system has unresolved image-tile width/height values for story, portrait, square, and banner. For offline work:

- Prefer full-bleed image backgrounds when media is needed.
- Use safe-area overlays for text.
- Avoid promising exact image-tile slot dimensions unless using a manual approximation.
- Report manual approximation if image tiles are required.

## Verification

Before finishing:

- Confirm exact canvas width and height.
- Confirm typography values match the spec.
- Confirm all major colors are from the spec.
- Confirm content stays inside the safe margin unless intentionally full-bleed.
- Confirm text does not overflow or collide.
