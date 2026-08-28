# Oliver Wyman PowerPoint brand checks

Bundled source guide: `Oliver-Wyman-Visual-Guidelines.md`, version `2026-08-04`. Operational rule IDs are in `rules.json`.

## Assessable rules

- Headline: Marsh Serif Regular/Italic (400). Supporting/body: Noto Sans. Approved system fallbacks are Georgia (or Georgia Pro Light) and Arial where the brand fonts are unavailable.
- Presentation copy uses sentence case.
- Core colors: Midnight Blue `#000F47`, Sky Blue `#CEECFF`, White `#FFFFFF`.
- Secondary colors: Gold `#CB7E03/#FFBF00/#FFD98A/#FFF3DA`; Blue `#000F47/#0B4BFF/#82BAFF/#CEECFF`; Green `#2F7500/#6ABF30/#B0DC92/#DFECD7`; Purple `#5E017F/#8F20DE/#DEB1FF/#F5E8FF`; Neutral `#3D3C37/#7B7974/#B9B6B1/#F7F3EE`.
- Extended neutral: `#D1CEC9` is accepted in practice as a subtle fill (e.g., table row backgrounds and layout bands where full Neutral 500 would be too strong). It is not in the published guide but is confirmed by design review as valid.
- Traffic colors: success `#14853D`, caution `#FFBE00`, critical `#C53532`. Traffic success and support Green 1000 are distinct.
- Do not create new colors, gradients, transparency, shadows, or effects.
- Use supplied Oliver Wyman master lockup with “A Marsh business”; do not recreate or distort it.
- Cover endorsed-lockup height is `0.52 in`; clear space equals logo cap height.
- Approved logo variants depend on background: Midnight Blue on light, White on dark/photo, Sky Blue only on controlled Midnight Blue template treatments.
- Use the approved PowerPoint template. Template/theme-derived colors and components are not violations merely because an explicit object token is absent from the short palette.

## Applicability safeguards

- A color check must distinguish slide background, text, shape fill, chart/table content, image pixels, and template-derived styling.
- A line-width rule applies only to the named line role. No authoritative general `0.75 pt` rule is present in the supplied guide, so the engine does not apply one to connectors, shape borders, table borders, or chart borders.
- Logo identity requires comparison with approved master assets; filenames or shape names alone are insufficient.
- Exact visual hierarchy, crop, contrast, and whitespace require rendered-slide evidence.
- Off-canvas working objects are inventory evidence only and never affect readiness.

## Coverage prerequisites

Do not claim complete Brand coverage without:

- the approved PowerPoint template and its named layouts/components;
- approved chart and table component examples;
- installed licensed Marsh Serif font files in the rendering runtime;
- authoritative logo master files integrated for identity/aspect-ratio matching.

Bundled fonts and logo masters support partial deterministic coverage. Report template components, chart/table styling, rendered font appearance, and visually altered/recreated logos as `Partially assessed` or `Not assessed` until the remaining prerequisites and visual evidence are available.
