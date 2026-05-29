---
name: brand-voice-check
description: Review short Oliver Wyman copy for brand voice, clarity, credibility, confidence, concision, AP Style, house style, and naming. Use for sentences, paragraphs, messages, captions, labels, standalone slide copy, and quick tone-of-voice checks that do not require full email, publication, social media, or presentation review.
---

# Brand Voice Check

Use this skill for focused review of short-form copy. Do not use it for full emails, full publications, social posts with platform requirements, or full presentation/deck reviews when a dedicated review skill is available.

## Workflow

1. Read the user-provided copy for purpose, audience, and main point.
2. Load `references/reviewer-prompt.md` for the full review standard and output structure.
3. Load `references/brand-voice.md` when the copy raises a brand voice, house style, or naming question.
4. Apply the stricter or more current rule when references differ, and note that the prompt may need updating.
5. Identify only the highest-impact issues and preserve the author's intent.

## Review Focus

- Clear, credible, confident, objective-not-cold, and concise voice.
- Confident, approachable, and forward-leaning personality.
- AP Style baseline plus Oliver Wyman house style overrides.
- Correct naming, including Oliver Wyman, the company, colleagues, and forbidden shorthand.
- Short, practical revisions rather than broad rewriting.

## Output

Use the `## Brand Voice Check` format from `references/reviewer-prompt.md`.

Limit issues to the top three to five unless the copy has critical risk. Include a revised version only when it materially helps.
