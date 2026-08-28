# Deterministic writing and fidelity rules

Machine-readable definitions live in `rules.json`. Each rule has a stable ID, version, source, scope, and applicability. The bundled source guide is `writing-style-guide.md`.

## Deterministic checks

- Preserve PowerPoint `a:br`, tabs, and paragraph boundaries as whitespace before testing word adjacency.
- Detect repeated adjacent words, obvious high-confidence spelling substitutions, malformed punctuation spacing, and currency-symbol order.
- Use US English by default. Apply local spelling only when the user changes `language`.
- Do not use `&` for ordinary prose unless it belongs to an official name or accepted acronym. A line break immediately before `&` is whitespace, not concatenation.
- Protect numbers, percentages, currencies, dates, citations, names, URLs, labels, claims, and deliberate emphasis during source/output comparison.
- Do not propose a changed claim or number. Report the mismatch and ask for source confirmation.

## Source attribution

For each candidate, compare normalized issue context against all plausible source-slide mappings:

- Candidate exists in a mapped source: `inherited_from_source`.
- Candidate does not exist in any plausible mapped source: `designer_introduced`.
- Mapping or intent is ambiguous: `unresolved`.
- Options, alternatives, and placeholders: `requester_decision`.

Do not punish the designer for inherited copy. Still include the finding if it affects delivery.

## Format fidelity

Text comparison alone is insufficient. Compare deliberate run-level bold and italic emphasis after text alignment. Missing source emphasis is a `format_fidelity` finding even when wording matches.

## Non-deterministic checks

Grammar, tone, sentence meaning, and specialist terminology may need model judgment. They must use the same finding schema and quote exact evidence. If a rule cannot be traced to the writing guide, user instructions, AP Stylebook, or Merriam-Webster, do not enforce it as a brand rule.
