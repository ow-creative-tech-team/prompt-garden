# Brand Voice Review Skills

This folder contains installable skills for reviewing Oliver Wyman content against brand voice, house style, AP Style, naming, clarity, channel expectations, and readiness standards.

Use these skills when a workflow can load a complete skill folder with a `SKILL.md` file, supporting references, optional scripts, and tool-specific metadata.

For standalone prompts that can be pasted into any AI tool, use `../../brand-voice/brand-voice-reviewers/`.

## Available Skills

| Skill | Use when | Do not use when |
| --- | --- | --- |
| `brand-voice-check` | Reviewing short copy, labels, captions, standalone paragraphs, messages, or quick tone checks. | Reviewing a full email, publication, social post, or presentation. |
| `email-review` | Reviewing complete internal, external, client, stakeholder, follow-up, update, request, bad-news, recognition, or time-sensitive emails. | The content is not structured as an email. |
| `publication-review` | Reviewing long-form or structured content, including articles, blog posts, website copy, reports, newsletters, or internal communications. | The content is mainly a slide deck, email, or social post. |
| `presentation-review` | Reviewing full decks, individual slides, rendered slide images, screenshots, PDFs, extracted slide text, or PPTX files. | You only need a quick sentence-level tone check. |
| `social-media-review` | Reviewing LinkedIn, X, executive social copy, campaign posts, event posts, research promotion, colleague recognition, hashtags, mentions, and platform fit. | The content is long-form editorial, an email, or a full presentation. |

## Skill Structure

Each skill follows this basic structure:

```text
brand-voice-review-skills/[skill-name]/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── reviewer-prompt.md
    └── brand-voice.md
```

`presentation-review` also includes:

```text
references/
├── brand-visual.md
└── review-output-template.md
scripts/
├── extract_pptx_text.py
└── inspect_pptx_package.py
```

## File Roles

- `SKILL.md` defines the skill name, description, trigger scope, workflow, guardrails, and expected output.
- `references/reviewer-prompt.md` contains the full review standard and output structure.
- `references/brand-voice.md` contains shared Oliver Wyman brand voice, house style, naming, and writing guidance.
- `agents/openai.yaml` contains tool-specific metadata for OpenAI agent workflows.
- `scripts/` contains helper scripts for file inspection when a skill needs more than text review.

## Updating A Skill

Start with the relevant folder under `brand-voice-review-skills/`.

1. Update `SKILL.md` when the skill's scope, trigger behavior, workflow, guardrails, or output expectations change.
2. Update `references/reviewer-prompt.md` when the review criteria, severity model, or output format changes.
3. Update `references/brand-voice.md` only when the underlying brand voice, house style, naming, or editorial rules change.
4. Update `agents/openai.yaml` when the agent display name, description, or default prompt metadata changes.
5. Keep related standalone prompts in `../../brand-voice/brand-voice-reviewers/` aligned when the same review standard changes.

Keep changes narrow and preserve the author's intent in any suggested revisions.

When updating both a skill and a standalone reviewer prompt, keep version and modified-date metadata in the prompt frontmatter. Do not duplicate version history in the prompt body unless users of that prompt need to see it.

## Installing Or Copying Skills

Install or copy the individual skill folder, not just `SKILL.md`, so the agent can access the required references and scripts.

For example, copy:

```text
brand-voice-review-skills/email-review/
```

as a complete folder into the target skills directory.

## Agent Instruction Files

This folder does not need its own `AGENTS.md` unless behavior inside `brand-voice-review-skills/` should differ from the rest of the repository.

If project-wide coding-agent instructions are needed later, add `AGENTS.md` at the repository root. Do not add `agent.md` or `angent.md`; those are not standard files for this project.
