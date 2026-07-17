# Social Media Spec

These values are resolved from the Figma design-system variables and are safe to use when the Figma file is unavailable.

## Asset Formats

All dimensions are pixels.

| Type | Width | Height | Aspect Ratio | Orientation | Margin | Gutter |
|---|---:|---:|---:|---|---:|---:|
| `banner` | 1080 | 512 | 135:64 | landscape | 48 | 48 |
| `portrait` | 1080 | 1350 | 4:5 | portrait | 72 | 72 |
| `story` | 1080 | 1920 | 9:16 | portrait | 72 | 72 |
| `square` | 1080 | 1080 | 1:1 | square | 60 | 60 |
| `thumbnail` | 640 | 640 | 1:1 | square | 48 | 48 |
| `video` | 1920 | 1080 | 16:9 | landscape | 72 | 72 |

Use the margin as the minimum safe area from all frame edges. Use the gutter between major content groups.

## Colors

### Core Palette

| Role | Hex |
|---|---:|
| Primary blue | `#000F47` |
| Interactive blue | `#0B4BFF` |
| Light blue | `#CEECFF` |
| Accent gold | `#FFBF00` |
| Gold hover/deep | `#CB7E03` |
| Gold muted | `#FFF3DA` |
| Neutral dark | `#3D3C37` |
| Neutral mid | `#7B7974` |
| Neutral inactive | `#B9B6B1` |
| Neutral light | `#F7F3EE` |
| White | `#FFFFFF` |
| Black | `#000000` |
| Success | `#14853D` |
| Attention | `#FFBE00` |
| Error | `#C53532` |

### Text Colors

| Role | Hex |
|---|---:|
| On light heading default | `#000F47` |
| On light body default | `#000F47` |
| On light default neutral text | `#3D3C37` |
| On light label default | `#3D3C37` |
| On light footnote | `#7B7974` |
| On light placeholder | `#B9B6B1` |
| On light accent primary | `#FFBF00` |
| On light accent secondary | `#0B4BFF` |
| On dark heading default | `#FFFFFF` |
| On dark body default | `#FFFFFF` |
| On dark neutral text | `#F7F3EE` |
| On dark brand text | `#CEECFF` |
| On dark accent primary | `#FFBF00` |
| On dark placeholder | `#B9B6B1` |

### Surface Colors

| Role | Hex |
|---|---:|
| Background light | `#FFFFFF` |
| Background brand | `#000F47` |
| Background accent | `#CEECFF` |
| Background neutral | `#F7F3EE` |
| Background dark | `#3D3C37` |
| Foreground on light brand | `#000F47` |
| Foreground on light accent 01 | `#FFBF00` |
| Foreground on light accent 02 | `#0B4BFF` |
| Foreground on dark default | `#FFFFFF` |
| Foreground on dark accent 01 | `#FFBF00` |
| Foreground on dark accent 02 | `#0B4BFF` |

### Border And Logo Colors

| Role | Hex |
|---|---:|
| Border on light default | `#3D3C37` |
| Border on light neutral | `#B9B6B1` |
| Border on light brand | `#000F47` |
| Border on dark default | `#F7F3EE` |
| Border button default | `#FFBF00` |
| Logo on light default | `#000F47` |
| Logo on light neutral | `#3D3C37` |
| Logo on light black | `#000000` |
| Logo on dark default | `#FFFFFF` |
| Logo on dark accent | `#CEECFF` |
| Logo on dark neutral | `#F7F3EE` |

## Typography

Use `font-family: "Marsh Serif", Georgia, serif` for headline/display roles. Use `font-family: "Noto Sans", Arial, sans-serif` for supportive roles.

All letter spacing is `0`.

### Heading

| Size | Family | Style | Font Size | Line Height |
|---|---|---|---:|---:|
| `lg` | Marsh Serif | Regular or Italic | 132 | 132 |
| `md` | Marsh Serif | Regular or Italic | 95 | 105 |
| `sm` | Marsh Serif | Regular or Italic | 80 | 96 |

### Body

| Size | Family | Style | Font Size | Line Height |
|---|---|---|---:|---:|
| `lg` | Noto Sans | Regular, Bold, or Italic | 52 | 68 |
| `md` | Noto Sans | Regular, Bold, or Italic | 40 | 52 |
| `sm` | Noto Sans | Regular, Bold, or Italic | 34 | 44 |

### Eyebrow

| Family | Style | Font Size | Line Height |
|---|---|---:|---:|
| Noto Sans | Bold | 34 | 44 |

### Quote

| Size | Family | Style | Font Size | Line Height |
|---|---|---|---:|---:|
| `lg` | Marsh Serif | Regular or Italic | 96 | 132 |
| `md` | Marsh Serif | Regular or Italic | 80 | 96 |
| `sm` | Marsh Serif | Regular or Italic | 64 | 80 |

### CTA

| Role | Family | Style | Font Size | Line Height |
|---|---|---|---:|---:|
| Heading | Marsh Serif | Regular or Italic | 80 | 96 |
| Body | Noto Sans | Regular, Bold, or Italic | 52 | 68 |

### Stats And Monogram

| Role | Family | Style | Font Size | Line Height |
|---|---|---|---:|---:|
| Stats `lg` | Marsh Serif | Regular | 300 | 330 |
| Stats `md` | Marsh Serif | Regular | 250 | 250 |
| Stats `sm` | Marsh Serif | Regular | 120 | 100 |
| Monogram | Marsh Serif | Regular | 150 | 100 |

## Layout Constants

| Role | Value |
|---|---:|
| Section gap standard | 40 |
| Section gap compact | 20 |
| Eyebrow-title gap | 8 |
| Divider-body gap | 40 |
| Divider line width | 1 |
| Logo height standard | 62 |
| Logo height compact | 52 |
| Logo divider gap standard | 31 |
| Logo divider gap compact | 26 |
| Logo content offset standard | 62 |
| Logo content offset compact | 52 |

Allowed horizontal alignment values: `left`, `center`.

Allowed vertical position values: `top`, `center`, `bottom`.

## Media Layout Constants

Use these values for image-tile media when enough resolved values exist.

| Type | Slot X | Slot Y Top | Slot Height | Source Ratio |
|---|---:|---:|---:|---|
| `story` | 72 | 0 | unresolved | portrait |
| `portrait` | 72 | 0 | unresolved | landscape |
| `square` | 60 | 0 | unresolved | landscape |
| `banner` | 48 | 0 | 72 | landscape |

Known unresolved media values from the source system:

- `story`: slot bottom y, width, height
- `portrait`: slot bottom y, width, height
- `square`: slot bottom y, width, height
- `banner`: slot bottom y, width

For offline asset generation, avoid media-tile templates that require unresolved width or height unless the user approves a visual approximation.

Display modes:

- Text tile default: `full-bleed`
- Image full default: `full-bleed`

## Recommended Composition Patterns

### Brand-Led

Use brand background `#000F47`, white or light-blue text, logo on dark, and Marsh Serif heading.

### Editorial Light

Use white or neutral-light background, primary blue heading/body, gold accent, and Noto Sans eyebrow.

### Stat-Led

Use stats typography as the dominant element. Pair `stats lg` or `stats md` with `body sm/md` supporting copy.

### Quote-Led

Use quote typography, preferably Marsh Serif Italic, with neutral or brand surfaces.

### CTA-Led

Use CTA heading and CTA body roles. Use gold as emphasis or button surface, with primary blue active state.
