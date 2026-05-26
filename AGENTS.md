# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository Purpose

**Prompt Garden** is a version-controlled, modular prompt library that serves three simultaneous purposes:
1. **GitHub repository** - Version control and collaboration
2. **OneDrive folder** - Team synchronization
3. **Obsidian vault** - Browsing and exploration

The library organizes prompts across three AI generation types:
- **text-to-image** - Styles, scenes, subjects (modular composition)
- **text-to-text** - Tone, format, topic
- **text-to-code** - Pattern, context, purpose

## Architecture & Design Patterns

### Modular Composition System

The core architecture uses a **compositional pattern** where prompts combine to create complete outputs:

```
Style + Scene + Subject = Complete Image Prompt
Tone + Format + Topic = Complete Text Prompt
Pattern + Context + Purpose = Complete Code Prompt
```

**File organization pattern:**
```
prompts/text-to-image/styles/{category}/{specific-style}/
├── _style.md              # Base aesthetic (ONE per style folder)
├── scene-*.md             # Multiple environment variants
└── subject-*.md           # Multiple subject variants
```

The `_style.md` prefix is **reserved** and critical - it marks the foundational style definition that other prompts build upon.

### YAML Frontmatter Schema

**Every** prompt file requires YAML frontmatter with strict field requirements:

**Required fields:**
- `id` - Unique across entire repo (format: `category-subcategory-descriptor`)
- `title` - Human-readable name
- `type` - Must be: `text-to-image`, `text-to-text`, or `text-to-code`
- `category` - Primary categorization
- `description` - Minimum 10 characters
- `prompt_role` - Must be: `style`, `scene`, `subject`, `standalone`, or `template`
- `tags` - Array, minimum 3 tags
- `version` - Semantic versioning (start at 1.0)
- `date_created` - ISO 8601 format (YYYY-MM-DD)
- `date_modified` - ISO 8601 format (YYYY-MM-DD)
- `format` - Usually `markdown`

**Recommended fields:**
- `related_prompts` - Links to complementary prompts with relationship type (`companion`, `alternative`, `prerequisite`)
- `compatible_models` - AI models tested with this prompt
- `usage_notes` - Practical application guidance
- `sub_category` - Finer categorization
- `author` - Creator identifier

### Cross-Reference Linking

Prompts link via `related_prompts` field in YAML:

```yaml
related_prompts:
  - id: urban-bw-scene-night-street
    relationship: companion  # companion | alternative | prerequisite
    combination_notes: "Combine for classic film noir aesthetic"
```

This creates a **graph structure** of interconnected prompts across categories.

## Naming Conventions (Critical)

**Folders:** `lowercase-kebab-case`
- Example: `urban-bw`, `portrait-natural`, `product-studio`

**Files by role:**
- `_style.md` - Base style (ONE per style folder, underscore prefix is mandatory)
- `scene-{descriptor}.md` - Scene variants (e.g., `scene-night-street.md`)
- `subject-{descriptor}.md` - Subject variants (e.g., `subject-pedestrian.md`)
- `{descriptive-name}.md` - Standalone/template prompts

**YAML IDs:** `category-subcategory-descriptor`
- Example: `urban-bw-photography-style`, `marketing-email-product-launch`
- Must be globally unique - search before creating: `grep -r "id: your-id" .`

## Git Workflow

**Branch Protection:** Main branch requires PRs. Never commit directly to main.

**Standard workflow:**
```bash
git checkout main
git pull origin main
git checkout -b feature/your-prompt-name
# [create/edit prompts]
git add .
git commit -m "type(scope): description"
git push origin feature/your-prompt-name
# [create PR on GitHub]
```

**Commit message format:**
```
type(scope): description

Types: feat, fix, docs, refactor, style
Scope: photography, illustration, marketing, etc.

Examples:
  feat(photography): add urban-bw style with night scene
  fix(marketing): correct email template variables
  docs(readme): update YAML schema section
```

## Working with OneDrive Conflicts

**Critical:** Git is the source of truth, not OneDrive.

If OneDrive creates conflict files (`*-OneDrive-Conflict-*.md`):
1. Check Git version: `git log -- path/to/file.md`
2. Keep Git version
3. Delete OneDrive conflict file
4. Commit removal if necessary

## Common Operations

### Creating a New Modular Style

```bash
# 1. Create style folder
mkdir -p prompts/text-to-image/styles/photography/my-style

# 2. Copy base template
cp _system/templates/style-template.md prompts/text-to-image/styles/photography/my-style/_style.md

# 3. Add scene/subject variants as needed
cp _system/templates/scene-template.md prompts/text-to-image/styles/photography/my-style/scene-example.md
```

### Creating a Standalone Prompt

```bash
cp _system/templates/standalone-template.md prompts/text-to-text/marketing/my-prompt.md
```

### Validating YAML

Before committing, verify:
- All required fields present
- ID is unique (grep search)
- Dates in YYYY-MM-DD format
- Minimum 3 tags
- No YAML syntax errors (use yamllint.com if unsure)

## Infrastructure Folders

**`_system/`** - Contains infrastructure, NOT prompts:
- `_system/templates/` - Starting templates for new prompts (COPY these)
- `_system/schemas/` - Validation schemas
- `_system/docs/` - Additional documentation

**`{category}/templates/`** - Contains actual reusable prompt components (different from `_system/templates/`)

## File Discovery Strategy

When searching for prompts or understanding structure:

1. **By type:** Navigate to `prompts/text-to-image/`, `prompts/text-to-text/`, or `prompts/text-to-code/`
2. **By purpose:** Navigate to category (e.g., `prompts/text-to-image/styles/photography/`, `prompts/text-to-text/marketing/`)
3. **By modularity:** Look for `_style.md` files for base styles, then find companion scenes/subjects

**Use grep for ID searches:**
```bash
grep -r "id: specific-id" .
```

## Key Principles

1. **Modularity** - Prefer composable prompts over monolithic ones
2. **YAML consistency** - Frontmatter is not optional; it enables search and relationships
3. **Git-first** - Git is source of truth, OneDrive is sync mechanism
4. **Feature branches** - Always work on feature branches, never on main
5. **Unique IDs** - IDs must be globally unique across entire repository
6. **kebab-case** - All folders, files, IDs, tags use lowercase-kebab-case

## Tools & Interfaces

- **VS Code + Codex** - Primary editing
- **Obsidian** - Browsing prompts (treats repo as vault)
- **GitHub** - Version control and PR reviews
- **OneDrive** - Background sync (passive, not authoritative)
