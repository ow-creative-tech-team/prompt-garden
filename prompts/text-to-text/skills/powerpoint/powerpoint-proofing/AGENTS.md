# Agent Guide

This directory contains one shareable Codex skill for PowerPoint proofing. Treat `SKILL.md` as the source of truth for behavior, boundaries, and user-facing workflow.

This `AGENTS.md` is the directory-level guide for the PowerPoint proofing skill. Follow this guide plus the repository-level `prompt-garden/AGENTS.md`.

## Project Structure

Key paths from the `prompt-garden/` repository root:

```text
prompts/text-to-text/skills/powerpoint/powerpoint-proofing/
├── AGENTS.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── brand-guidelines.md
│   └── visual-guidelines.md
└── scripts/
    ├── pptx_text.py
    └── report_artifact.py
```

- `AGENTS.md` is this directory-level contributor and agent guide.
- `SKILL.md` defines the PowerPoint proofing skill.
- `agents/openai.yaml` defines the display name, short description, and default prompt for the skill.
- `references/` contains the visual and brand guidance used by the skill.
- `scripts/` contains helper scripts for extraction and report artifacts.
- Keep temporary work outside this source directory unless an ignored scratch path is configured.

## Working Guidelines

- Keep the skill findings-only unless the skill definition is intentionally changed.
- Do not create, revise, patch, or deliver corrected PowerPoint decks from the `powerpoint-proofing` skill.
- Use `scripts/pptx_text.py` for extracting text and style metadata from decks.
- Use `scripts/report_artifact.py` only for proofing report artifacts, not for revised decks or slide exports.
- Update the files in `references/` when changing proofing rules instead of duplicating rules in prompts or scripts.
- Keep generated proofing outputs out of source changes unless they are intentionally being added as examples or fixtures.

## Review Checklist

Before sharing changes, confirm:

- The skill description still matches the actual behavior.
- The hard boundaries in `SKILL.md` are preserved.
- Script changes do not introduce deck-editing behavior.
- New examples or artifacts are clearly named and do not imply a corrected deck unless correction is an intentional, separate workflow.
