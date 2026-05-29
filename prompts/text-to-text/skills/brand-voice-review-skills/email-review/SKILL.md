---
name: email-review
description: Review Oliver Wyman emails before sending for purpose, audience fit, subject line, opening, body structure, closing, tone, brand voice, AP Style, house style, naming, clarity, concision, and send-readiness.
---

# Email Review

Use this skill for complete internal, external, client, stakeholder, follow-up, update, request, bad-news, recognition, and time-sensitive emails.

## Workflow

1. Identify the email type, audience, purpose, and urgency from the draft and surrounding context.
2. Load `references/reviewer-prompt.md` for the email review standard and output structure.
3. Load `references/brand-voice.md` when the draft raises a brand voice, house style, or naming question.
4. Review the email as practical communication, not just polished writing.
5. Prioritize issues that affect clarity, response likelihood, tone, credibility, brand alignment, or risk.
6. Preserve the author's intent and voice while making the email easier to act on.

## Review Focus

- Subject line specificity, sentence case, length, and usefulness.
- Point-first opening, sufficient context, and clear ask or next step.
- Short paragraphs, scannable structure, and one main idea per paragraph.
- Direct but respectful tone calibrated to audience, urgency, and relationship.
- Clear, credible, confident, objective-not-cold, and concise brand voice.
- AP Style, house style, and naming rules.

## Output

Use the `## Email Review` format from `references/reviewer-prompt.md`.

Provide a revised email when the verdict is not fully approved or when small edits would materially improve send-readiness.
