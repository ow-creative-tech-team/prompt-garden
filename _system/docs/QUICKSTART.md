# 🚀 Prompt Garden - Quick Start Guide

> Condensed reference for creating and committing prompts to the repository

---

## 📁 Repository Structure

```
prompt-garden/
├── text-to-image/          # Image generation prompts
│   ├── styles/             # Organized by style categories
│   │   └── [category]/[style-name]/
│   │       ├── _style.md
│   │       ├── scene-*.md
│   │       └── subject-*.md
│   ├── subjects/           # Standalone subjects
│   └── templates/          # Reusable components
│
├── text-to-text/           # Text generation prompts
│   ├── creative/
│   ├── technical/
│   ├── marketing/
│   │   └── [use-case]/
│   │       ├── _tone.md
│   │       ├── format-*.md
│   │       └── topic-*.md
│   └── templates/
│
├── text-to-code/           # Code generation prompts
│   ├── functions/
│   ├── scripts/
│   ├── snippets/
│   │   └── [feature]/
│   │       ├── _pattern.md
│   │       ├── context-*.md
│   │       └── purpose-*.md
│   └── templates/
│
└── _system/
    ├── schemas/            # YAML validation
    └── templates/          # Prompt templates
```

---

## 📝 Naming Conventions

### Folders
- **Format**: `lowercase-kebab-case`
- **Examples**: `urban-bw`, `linkedin-professional`, `async-api-handler`

### File Prefixes by Type

#### Text-to-Image

| Prefix | Purpose | Example |
|--------|---------|---------|
| `_style` | Base style (HOW it looks) | `_style.md` |
| `scene-` | Environment/setting (WHERE) | `scene-urban-night.md` |
| `subject-` | Main subject (WHAT) | `subject-pedestrian.md` |

#### Text-to-Text

| Prefix | Purpose | Example |
|--------|---------|---------|
| `_tone` | Voice/writing style (HOW it sounds) | `_tone.md` |
| `format-` | Output structure (CONTAINER) | `format-linkedin-post.md` |
| `topic-` | Subject matter (WHAT about) | `topic-ai-ethics.md` |

#### Text-to-Code

| Prefix | Purpose | Example |
|--------|---------|---------|
| `_pattern` | Coding paradigm (HOW to code) | `_pattern.md` |
| `context-` | Tech stack/environment (WHERE) | `context-nextjs-api.md` |
| `purpose-` | Functionality (WHAT it does) | `purpose-auth-jwt.md` |

#### Universal

| Prefix | Purpose | Example |
|--------|---------|---------|
| `template-` | Reusable component | `template-lighting.md` |
| (none) | Standalone prompt | `hero-shot.md` |

---

## 📋 Available Templates

### Text-to-Image
- `_system/templates/style-template.md` → `_style.md`
- `_system/templates/scene-template.md` → `scene-*.md`
- `_system/templates/subject-template.md` → `subject-*.md`

### Text-to-Text
- `_system/templates/text-to-text/tone-template.md` → `_tone.md`
- `_system/templates/text-to-text/format-template.md` → `format-*.md`
- `_system/templates/text-to-text/topic-template.md` → `topic-*.md`

### Text-to-Code
- `_system/templates/text-to-code/pattern-template.md` → `_pattern.md`
- `_system/templates/text-to-code/context-template.md` → `context-*.md`
- `_system/templates/text-to-code/purpose-template.md` → `purpose-*.md`

### Universal
- `_system/templates/standalone-template.md` → `[name].md`
- `_system/templates/template-component.md` → `template-*.md`

---

## 📄 YAML Schema Reference

### Required Fields (All Types)

```yaml
---
id: unique-identifier-kebab-case
title: Human Readable Title
type: text-to-image | text-to-text | text-to-code
category: [main-category]
description: Short description (min 10 chars)
prompt_role: [see role table below]
tags:
  - tag1
  - tag2
  - tag3  # minimum 3 tags
version: 1.0
date_created: 2025-10-04
date_modified: 2025-10-04
format: markdown
---
```

### Prompt Role Values by Type

| Type | Available Roles |
|------|-----------------|
| **text-to-image** | `style`, `scene`, `subject` |
| **text-to-text** | `tone`, `format`, `topic` |
| **text-to-code** | `pattern`, `context`, `purpose` |
| **All types** | `template`, `standalone` |

### Optional Fields

```yaml
sub_category: deeper-categorization
usage_notes: Best use cases and tips
related_prompts:
  - id: related-prompt-id
    relationship: companion | alternative | prerequisite
    combination_notes: How to combine
compatible_models:
  - model-name-1
  - model-name-2
author: your-name
```

---

## ✅ Type-Specific YAML Examples

### Text-to-Image Example

```yaml
---
id: urban-bw-photography
title: Urban Black & White Photography
type: text-to-image
category: photography
description: High contrast black and white urban photography style
prompt_role: style
tags:
  - black-and-white
  - urban
  - high-contrast
version: 1.0
date_created: 2025-10-04
date_modified: 2025-10-04
format: markdown
---
```

### Text-to-Text Example

```yaml
---
id: professional-linkedin-tone
title: Professional LinkedIn Tone
type: text-to-text
category: marketing
description: Professional yet conversational tone for LinkedIn posts
prompt_role: tone
tags:
  - professional
  - linkedin
  - conversational
version: 1.0
date_created: 2025-10-04
date_modified: 2025-10-04
format: markdown
---
```

### Text-to-Code Example

```yaml
---
id: async-error-handling-pattern
title: Async/Await Error Handling Pattern
type: text-to-code
category: functions
description: Async/await pattern with comprehensive error handling
prompt_role: pattern
tags:
  - async
  - error-handling
  - typescript
version: 1.0
date_created: 2025-10-04
date_modified: 2025-10-04
format: markdown
---
```

---

## ✓ Validation Instructions

### 1. YAML Syntax Validation

**Online Validator:**
- Visit: [yamllint.com](http://www.yamllint.com/)
- Copy your YAML frontmatter (between `---` markers)
- Paste and validate

**VS Code:**
- Install "YAML" extension
- Red underlines indicate syntax errors
- Hover for error details

### 2. Schema Validation

**Required Field Checklist:**
- [ ] `id` is in kebab-case (lowercase, hyphens only)
- [ ] `type` is one of: `text-to-image`, `text-to-text`, `text-to-code`
- [ ] `prompt_role` matches your type (see table above)
- [ ] `tags` has minimum 3 items
- [ ] `version` follows semantic versioning (e.g., `1.0`, `1.2.1`)
- [ ] `date_created` and `date_modified` are in `YYYY-MM-DD` format
- [ ] `description` is at least 10 characters

**Schema Location:**
```
_system/schemas/prompt-schema.json
```

---

## 🔄 Git Commit Workflow

### Step-by-Step Process

```bash
# 1. ALWAYS pull first
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-prompt-name

# 3. Create your prompt file(s)
# - Copy appropriate template
# - Fill YAML frontmatter
# - Write prompt content
# - Validate YAML (see above)

# 4. Stage changes
git add .

# 5. Commit with conventional message
git commit -m "feat(category): description"

# 6. Push to remote
git push origin feature/your-prompt-name

# 7. Create Pull Request on GitHub
# - Go to repository
# - Click "Compare & pull request"
# - Request review from team member
# - Merge after approval
```

### Commit Message Format

**Format:** `type(scope): description`

**Types:**
- `feat` - New prompt or feature
- `fix` - Fix to existing prompt
- `docs` - Documentation changes
- `refactor` - Reorganization or renaming

**Examples:**
```bash
feat(photography): add urban-bw style with variants
feat(marketing): add linkedin professional tone
feat(functions): add async error handling pattern
fix(illustration): correct color values
docs(readme): update naming conventions
```

---

## 🎯 Modular Combination Examples

### Text-to-Image
```
[Style] + [Subject] + [Scene]
= urban-bw/_style.md + subject-pedestrian.md + scene-night-street.md
```

### Text-to-Text
```
[Tone] + [Format] + [Topic]
= _tone.md + format-linkedin-post.md + topic-ai-ethics.md
```

### Text-to-Code
```
[Pattern] + [Context] + [Purpose]
= _pattern.md + context-nextjs-api.md + purpose-auth-jwt.md
```

---

## 📚 Quick Commands Reference

```bash
# Daily workflow
git pull origin main                    # Start of session
git checkout -b feature/my-prompt       # New feature branch
git add .                               # Stage all changes
git commit -m "feat(type): description" # Commit
git push origin feature/my-prompt       # Push to remote

# Status checks
git status                              # What's changed
git diff                                # See changes
git log --oneline -5                    # Recent commits

# Branch management
git branch                              # List branches
git checkout main                       # Switch to main
git branch -d feature/old-branch        # Delete local branch
```

---

## 🆘 Quick Help

**YAML Errors?** → [yamllint.com](http://www.yamllint.com/)
**Git Issues?** → [GitHub Docs](https://docs.github.com)
**Full Documentation?** → See [README.md](README.md)

---

**Happy Prompting! 🌱**
