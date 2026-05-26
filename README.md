# 🌱 Prompt Garden

A version-controlled, modular prompt library for text-to-image, text-to-text, and text-to-code generation. This repository serves as the single source of truth for our team's prompt collection.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Creating Prompts](#creating-prompts)
- [Naming Conventions](#naming-conventions)
- [YAML Schema](#yaml-schema)
- [Modular Prompt System](#modular-prompt-system)
- [Workflow](#workflow)
- [Tools & Interfaces](#tools--interfaces)
- [Version Control Best Practices](#version-control-best-practices)

---

## Overview

This repository is simultaneously:
- **GitHub Repository**: Version-controlled source of truth
- **OneDrive Shared Folder**: Team file sync and access
- **Obsidian Vault**: Visual browsing and linking

All prompts are stored as either `.md` (Markdown) or `.json` files with YAML frontmatter for metadata.

Codex skill packages under `prompts/text-to-text/skills/` are a special case. They use a `SKILL.md` file with Codex skill frontmatter, plus optional `AGENTS.md`, `agents/`, `references/`, and `scripts/` files. The standard prompt YAML schema applies to prompt files, not to skill package support files.

---

## Repository Structure

```
prompt-garden/
├── prompts/                   # All prompts organized by type
│   ├── text-to-image/
│   │   ├── styles/
│   │   │   ├── photography/        # Photography styles
│   │   │   │   ├── urban-bw/       # Example: Urban Black & White
│   │   │   │   │   ├── _style.md   # Base style definition
│   │   │   │   │   ├── scene-*.md  # Scene variants
│   │   │   │   │   └── subject-*.md # Subject variants
│   │   │   │   ├── portrait-natural/
│   │   │   │   └── product-studio/
│   │   │   ├── illustration/       # Illustration styles
│   │   │   ├── 3d-render/         # 3D render styles
│   │   │   └── digital-art/       # Digital art styles
│   │   ├── subjects/              # Standalone subjects
│   │   └── templates/             # Reusable components
│   │
│   ├── text-to-text/
│   │   ├── brand-voice/           # Brand voice prompts and guidance
│   │   │   └── agents/            # Brand voice reviewer prompts
│   │   │       ├── email-reviewer-prompt.md
│   │   │       ├── presentation-reviewer-prompt.md
│   │   │       ├── publication-reviewer-prompt.md
│   │   │       ├── social-media-reviewer-prompt.md
│   │   │       └── tone-of-voice-reviewer-prompt.md
│   │   ├── creative/              # Creative writing prompts
│   │   ├── marketing/             # Marketing copy prompts
│   │   ├── skills/                # Codex skill packages
│   │   │   └── powerpoint/
│   │   │       └── powerpoint-proofing/
│   │   │           ├── SKILL.md          # Skill definition and workflow
│   │   │           ├── AGENTS.md         # Directory-level agent guide
│   │   │           ├── agents/           # Skill agent metadata
│   │   │           ├── references/       # Skill-specific rule references
│   │   │           └── scripts/          # Skill helper scripts
│   │   ├── technical/             # Technical writing prompts
│   │   ├── templates/             # Reusable templates
│   │   └── translation/           # Translation prompt systems
│   │       └── translation-prompts-v1/
│   │           ├── translators/        # Agent-style language translators
│   │           ├── translators-lenAI/  # Standalone LenAI translator prompts
│   │           ├── evaluator/          # Translation quality evaluator
│   │           └── prompt-enhancer/    # Translation prompt improvement agent
│   │
│   └── text-to-code/
│       ├── functions/             # Function generation prompts
│       ├── scripts/               # Script generation prompts
│       ├── snippets/              # Code snippet prompts
│       └── templates/             # Code templates
│
└── _system/
    ├── schemas/               # YAML validation schemas
    ├── templates/             # Prompt templates
    └── docs/                  # Additional documentation
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd prompt-garden
```

### 2. Set Up Your Environment

**Primary Tools:**
- **VS Code + Claude Code**: For creating and editing prompts
- **Obsidian**: For browsing and exploring prompts
- **Finder (macOS)**: For file operations and organization

### 3. Pull Before Making Changes

**Always** pull the latest changes before starting work:

```bash
git pull origin main
```

---

## Creating Prompts

### Quick Start

1. **Choose the right template** from `_system/templates/`:
   - `style-template.md` - For base style definitions
   - `scene-template.md` - For scene/environment prompts
   - `subject-template.md` - For subject/character prompts
   - `standalone-template.md` - For complete standalone prompts
   - `template-component.md` - For reusable components

2. **Copy the template** to the appropriate folder
3. **Rename** following naming conventions (see below)
4. **Fill in the YAML frontmatter** with all required fields
5. **Write your prompt** in the content section
6. **Save and commit** following the workflow guidelines

### Example: Creating a Photography Style

```bash
# 1. Navigate to the category
cd prompts/text-to-image/styles/photography

# 2. Create a new style folder
mkdir minimalist-product

# 3. Copy the style template
cp ../../../../_system/templates/style-template.md minimalist-product/_style.md

# 4. Edit in VS Code
code minimalist-product/_style.md
```

---

## Naming Conventions

### Folders
- **Format**: `lowercase-kebab-case`
- **Examples**: `urban-bw`, `portrait-natural`, `minimalist-product`

### Files
- **Format**: `{type}-{descriptor}.{ext}`
- **Extension**: `.md` or `.json`

#### File Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `_style` | Base style definition | `_style.md` |
| `scene-` | Scene/environment prompt | `scene-urban-night.md` |
| `subject-` | Subject/character prompt | `subject-business-woman.md` |
| `template-` | Reusable component | `template-lighting.md` |
| (none) | Standalone prompt | `product-hero-shot.md` |

### Examples

✅ **Good:**
- `prompts/text-to-image/styles/photography/urban-bw/_style.md`
- `prompts/text-to-image/styles/photography/urban-bw/scene-night-street.md`
- `prompts/text-to-text/marketing/social-media-hook.md`

❌ **Bad:**
- `Urban_BW/Style.md` (wrong case, wrong name)
- `scene_nightStreet.md` (mixed case styles)
- `My Amazing Prompt.md` (spaces, not descriptive)

---

## YAML Schema

Most prompt files use the standard Prompt Garden YAML schema below.

Brand voice reviewer prompts under `prompts/text-to-text/brand-voice/agents/` use the standard Prompt Garden YAML schema. They are prompt files, not Codex skill package agent metadata.

Translation agents under `prompts/text-to-text/translation/translation-prompts-v1/translators/`, `evaluator/`, and `prompt-enhancer/` may instead use agent-style frontmatter:

```yaml
---
name: french-business-translator
description: |
  Use this agent when translating English business content into French.
model: inherit
color: blue
---
```

Standalone LenAI translator prompts under `translators-lenAI/` are plain Markdown system prompts and may omit YAML frontmatter.

### Standard Prompt Required Fields

```yaml
---
id: unique-identifier-kebab-case
title: Human Readable Title
type: text-to-image | text-to-text | text-to-code
format: markdown | json
version: 1.0
category: photography | illustration | creative | technical | etc.
sub_category: deeper-categorization
prompt_role: style | scene | subject | template | standalone
description: Short description of what this prompt generates
usage_notes: Best use cases and tips for this prompt
tags: #tag1; #tag 2;
date_created: 2025-10-04
date_modified: 2025-10-04
related_prompts:
  - id: related-prompt-id
    relationship: companion | alternative | prerequisite
    combination_notes: How to combine these prompts
recomended_models: #nanobanana #GPT-Image #FluxKontext
author: your-git-hub-user
---
```


### Standard Prompt Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier in kebab-case (used for linking) |
| `title` | string | Human-readable title |
| `type` | enum | Primary type: text-to-image, text-to-text, text-to-code |
| `category` | string | Main category (e.g., photography, illustration) |
| `sub_category` | string | Optional deeper categorization |
| `description` | string | What this prompt generates (min 10 chars) |
| `usage_notes` | string | Best practices and use cases |
| `prompt_role` | enum | Role in composition: style, scene, subject, template, standalone |
| `tags` | array | Minimum 3 tags for searchability |
| `related_prompts` | array | Links to related prompts with relationship type |
| `recomended_models` | array | AI models this works with |
| `version` | string | Semantic version (e.g., 1.0, 1.2.1) |
| `date_created` | date | Creation date (YYYY-MM-DD) |
| `date_modified` | date | Last modified date (YYYY-MM-DD) |
| `author` | string | Optional creator name |
| `format` | enum | markdown or json |

---

## Modular Prompt System

### Concept

Prompts can be **combined** to create complex outputs. The system uses three main roles:

1. **Style** (`_style.md`): Defines the aesthetic/rendering style
2. **Subject** (`subject-*.md`): Defines what is in the image
3. **Scene** (`scene-*.md`): Defines the environment/setting

### Linking Prompts

Use the `related_prompts` field to create relationships:

```yaml
related_prompts:
  - id: urban-bw-scene-street
    relationship: companion
    combination_notes: "Combine for complete urban scene"
  - id: portrait-natural-subject-woman
    relationship: alternative
    combination_notes: "Alternative subject for this style"
```

### Relationship Types

- **companion**: Designed to work together
- **alternative**: Different option for similar use case
- **prerequisite**: Required before using this prompt

### Example: Modular Photography Prompt

**File Structure:**
```
prompts/text-to-image/styles/photography/urban-bw/
├── _style.md              # Base B&W photography style
├── scene-night-street.md  # Urban nighttime scene
└── subject-pedestrian.md  # Walking person subject
```

**Combination:**
```
[_style.md prompt] + [subject-pedestrian.md prompt] + [scene-night-street.md prompt]
= "High contrast black and white photography, sharp grain, dramatic shadows +
   solitary pedestrian in winter coat, walking with purpose +
   wet city street at night, neon reflections, empty sidewalk"
```

---

## Workflow

### Branch Strategy

- **`main`**: Protected branch, requires PR + 1 review
- **`develop`**: Integration branch (optional for complex changes)
- **Feature branches**: `feature/your-prompt-name`

### Standard Workflow

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/urban-bw-style
   ```

3. **Create your prompt(s)**
   - Copy appropriate template
   - Fill in YAML frontmatter
   - Write prompt content
   - Save file

4. **Test and validate**
   - Check YAML syntax
   - Verify all required fields
   - Test prompt if possible

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat(photography): add urban-bw style with scene variants"
   ```

6. **Push to remote**
   ```bash
   git push origin feature/urban-bw-style
   ```

7. **Create Pull Request**
   - Go to GitHub
   - Create PR from your branch to `main`
   - Request review from team member
   - Address feedback if needed

8. **Merge after approval**
   - Squash and merge (recommended)
   - Delete feature branch

### Commit Message Convention

Format: `type(scope): description`

**Types:**
- `feat`: New prompt or feature
- `fix`: Fix to existing prompt
- `docs`: Documentation changes
- `refactor`: Reorganization or renaming
- `style`: Formatting changes (not prompt style)

**Examples:**
```bash
feat(photography): add urban-bw style
fix(illustration): correct color values in anime style
docs(readme): update naming conventions
refactor(text-to-image): reorganize photography styles
```

---

## Tools & Interfaces

### VS Code + Claude Code Extension
**Primary editing interface**

- Create and edit prompts
- Use Claude Code for writing assistance
- Integrated Git workflow
- YAML syntax highlighting

**Recommended Extensions:**
- Claude Code
- YAML
- Markdown All in One
- GitLens

### Obsidian
**Browsing and exploration**

- Visual graph view of linked prompts
- Quick navigation between related prompts
- Tag-based filtering
- Note: `.obsidian/workspace.json` is gitignored (personal settings)

### Finder
**File operations**

- Copy/move prompts between folders
- Quick file management
- Drag-and-drop organization

---

## Version Control Best Practices

### Avoiding Conflicts

With 5 team members + OneDrive + Git, follow these rules:

1. **Always pull before editing**
   ```bash
   git pull origin main
   ```

2. **Work on separate prompts** when possible
   - Coordinate with team in your communication channel
   - Avoid editing the same file simultaneously

3. **Commit frequently**
   - Small, focused commits are better
   - Makes conflict resolution easier

4. **Push regularly**
   - Don't let changes sit for days
   - Reduces merge conflict likelihood

### OneDrive + Git Coexistence

⚠️ **Important**: OneDrive can create sync conflicts. To prevent issues:

1. **Git is the source of truth**
   - Always use Git commands for version control
   - Don't rely on OneDrive version history

2. **Before major changes**
   ```bash
   git status  # Check for any uncommitted changes
   git pull    # Get latest from team
   ```

3. **If OneDrive creates conflict files**
   - Files like `prompt-name-OneDrive-Conflict.md` appear
   - Resolve by comparing with Git version
   - Delete conflict file after resolving
   - Commit clean version

4. **OneDrive pause** (if needed)
   - Pause OneDrive sync during complex Git operations
   - Resume after committing and pushing

### Handling Merge Conflicts

If you encounter conflicts:

1. **Identify the conflict**
   ```bash
   git status  # Shows conflicted files
   ```

2. **Open conflicted file** in VS Code
   - Look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
   - Choose which version to keep (or combine them)

3. **Resolve and commit**
   ```bash
   git add resolved-file.md
   git commit -m "fix: resolve conflict in urban-bw style"
   git push
   ```

### Git Safety Checklist

Before committing:
- [ ] Pulled latest changes
- [ ] Tested prompt (if applicable)
- [ ] All YAML fields filled correctly
- [ ] No OS-specific files included (`.DS_Store`, etc.)
- [ ] Meaningful commit message

Before pushing:
- [ ] Commits are clean and focused
- [ ] No sensitive information in prompts
- [ ] Files follow naming conventions

---

## Quick Reference

### File Templates Location
```
_system/templates/
├── style-template.md
├── scene-template.md
├── subject-template.md
├── standalone-template.md
└── template-component.md
```

### Schema Validation
```
_system/schemas/prompt-schema.json
```

### Common Git Commands
```bash
# Daily workflow
git pull origin main                    # Start of day
git checkout -b feature/my-prompt       # New feature
git add .                               # Stage changes
git commit -m "feat(type): description" # Commit
git push origin feature/my-prompt       # Push to remote

# Checking status
git status                              # See what's changed
git log --oneline -5                    # Recent commits
git diff                                # See uncommitted changes

# Branch management
git branch                              # List branches
git branch -d feature/old-branch        # Delete local branch
git checkout main                       # Switch to main
```

---

## Getting Help

**Questions about:**
- **Git/GitHub**: Check [GitHub Docs](https://docs.github.com)
- **YAML syntax**: Validate at [yamllint.com](http://www.yamllint.com/)
- **Prompt writing**: Ask in team communication channel
- **This repo structure**: Create an issue in GitHub

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

---

**Happy Prompting! 🌱**
