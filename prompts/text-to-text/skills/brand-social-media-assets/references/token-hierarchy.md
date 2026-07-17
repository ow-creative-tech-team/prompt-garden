# Token Hierarchy

Use this hierarchy to understand where the offline values came from. Agents do not need the Figma file to use this skill.

## Collections Found In Figma

The source Figma file contained 3 local variable collections:

| Collection | Mode | Variables | Types |
|---|---:|---:|---|
| `primitive` | `Mode 1` | 122 | 26 color, 29 string, 67 float |
| `alias` | `oliver-wyman` | 95 | 41 color, 2 string, 52 float |
| `mapped` | `default` | 383 | 217 color, 53 string, 113 float |

Alias edges found:

| Edge | Count |
|---|---:|
| `mapped -> alias` | 259 |
| `mapped -> primitive` | 90 |
| `alias -> primitive` | 68 |
| `alias -> alias` | 14 |
| `mapped -> null` | 11 |

## Primitive Foundations

Primitive variables apply to all asset types and include:

- `color/*`
- `font/*`
- `scale/*`
- `aspect-ratio/*`
- supporting enum values used by mapped layout variables

For offline generation, use the resolved values in `social-media-spec.md`.

## Primitive Color Foundations

| Token | Value |
|---|---:|
| `color/blue/1000` | `#000F47` |
| `color/blue/750` | `#0B4BFF` |
| `color/blue/500` | `#82BAFF` |
| `color/blue/250` | `#CEECFF` |
| `color/gold/1000` | `#CB7E03` |
| `color/gold/750` | `#FFBF00` |
| `color/gold/500` | `#FFD98A` |
| `color/gold/250` | `#FFF3DA` |
| `color/neutral/1000` | `#3D3C37` |
| `color/neutral/750` | `#7B7974` |
| `color/neutral/500` | `#B9B6B1` |
| `color/neutral/250` | `#F7F3EE` |
| `color/neutral/black` | `#000000` |
| `color/neutral/white` | `#FFFFFF` |
| `color/traffic/warning` | `#C53532` |
| `color/traffic/attention` | `#FFBE00` |
| `color/traffic/success` | `#14853D` |

## Font Foundations

- Headline family resolves to `Marsh Serif`.
- Supportive family resolves to `Noto Sans`.
- Marsh Serif supports `Regular` and `Italic`.
- Noto Sans supports `Regular`, `Italic`, `Light`, `Medium`, `Bold`, and italic variants.

## Scale Foundations

Important resolved scale values:

| Token | Value |
|---|---:|
| `scale/space/500` | 20 |
| `scale/space/1000` | 40 |
| `scale/space/1200` | 48 |
| `scale/space/1500` | 60 |
| `scale/space/1800` | 72 |
| `scale/canvas/200` | 512 |
| `scale/canvas/300` | 640 |
| `scale/canvas/400` | 1350 |
| `scale/canvas/600` | 1080 |
| `scale/canvas/700` | 1920 |
