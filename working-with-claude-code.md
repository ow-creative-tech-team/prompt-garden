# Working with Claude Code in Prompt Garden

This guide explains how Claude Code is configured to work as your **Prompt Garden Curator** - a specialized AI assistant for managing, creating, and maintaining the Prompt Garden repository.

---

## Overview

Claude Code in this project is configured with:
- **Custom Output Style** - Prompt Garden Curator persona
- **Specialized Agents** - Task-specific automation for metadata validation and prompt composition
- **Slash Commands** - Quick-access workflows for common operations
- **Permissions** - Safety guardrails for repository operations

This setup transforms Claude Code from a general-purpose coding assistant into a **librarian and curator** focused on structure, metadata, version control, and repository health.

---

## Configuration Files

The `.claude/` directory contains all customization:

```
.claude/
├── output-styles/
│   └── prompt-garden-curator.md    # Main Claude persona/behavior
├── agents/
│   ├── image-prompt-metadata.md    # YAML validation agent
│   └── image-prompt-composer.md    # Prompt crafting agent
├── commands/
│   ├── image-prompt-metadata.md    # /image-prompt-metadata command
│   └── image-prompt-composer.md    # /image-prompt-composer command
└── settings.local.json              # Project-specific settings
```

---

## Output Style: Prompt Garden Curator

**Location:** [.claude/output-styles/prompt-garden-curator.md](.claude/output-styles/prompt-garden-curator.md)

**Active by default** via `settings.local.json`:
```json
{
  "outputStyle": "prompt-garden-curator"
}
```

### What It Does

This output style defines Claude's **role, behavior, and expertise** when working in this repository:

**Primary responsibilities:**
1. **YAML Frontmatter Validation** - Ensures complete, accurate metadata
2. **File Organization** - Maintains naming conventions (`lowercase-kebab-case`)
3. **Git Version Control** - Creates semantic commits, uses feature branches
4. **Cross-Reference Linking** - Connects related prompts via `related_prompts` field
5. **ID Uniqueness** - Always verifies IDs globally before creating prompts

**Behavioral guidelines:**
- Be **precise and systematic** - verify completeness before confirming "done"
- Be **concise** - focus on structure/metadata, not prompt content (unless asked)
- **Never commit to main** - always use feature branches
- **Always check ID uniqueness** with `grep -r "id: proposed-id" .`
- **Explicitly state** git branch, commit message, and next steps

### How to Use

Simply interact naturally with Claude Code - the curator persona is always active:

```
You: "Create a new urban photography style prompt"

Claude: I'll help create that. First, let me check for existing urban
        photography prompts and verify the ID will be unique...

        [Creates feature branch, validates YAML, suggests related prompts]
```

Claude will proactively:
- Check for templates to copy
- Validate YAML completeness
- Verify ID uniqueness with grep
- Create feature branches (never commit to main)
- Suggest semantic commit messages
- Link related prompts when appropriate

---

## Specialized Agents

Agents are **autonomous sub-tasks** that Claude can launch for complex, multi-step operations. They have access to specific tools and expertise.

### 1. Image Prompt Metadata Agent

**Location:** [.claude/agents/image-prompt-metadata.md](.claude/agents/image-prompt-metadata.md)
**Purpose:** Validates and fixes YAML frontmatter for text-to-image prompt files

**When Claude uses it:**
- Automatically when you ask to validate/fix metadata
- When creating new text-to-image prompts
- When editing existing prompts with incomplete YAML

**What it does:**
1. Reads prompt file and parses YAML frontmatter
2. Validates all required fields against schema
3. Infers missing metadata from file path and content
4. Verifies ID uniqueness with `grep -r "id: ..." .`
5. Updates file with compliant YAML
6. Reports before/after changes clearly

**Example workflow:**
```
You: "Fix the YAML metadata in my vintage-film style prompt"

Claude: [Launches image-prompt-metadata agent]

Agent:
  ❌ Missing: id, category, description, prompt_role, version, dates
  ⚠️  Insufficient tags (has 1, needs 3)

  Proposed YAML:
  id: vintage-film-photography-style
  title: Vintage Film Look
  type: text-to-image
  category: photography
  ...

  ID Uniqueness Check: ✅ No conflicts found

  Apply these changes?
```

**Tools available:** Read, Edit, Grep, Glob, Bash

### 2. Image Prompt Composer Agent

**Location:** [.claude/agents/image-prompt-composer.md](.claude/agents/image-prompt-composer.md)
**Purpose:** Transforms vague ideas into structured, technical text-to-image prompts

**When Claude uses it:**
- When you want help crafting a new image prompt
- When refining existing prompt text
- When you provide rough ideas that need structuring

**What it does:**
1. Asks clarifying questions (style? lighting? composition? mood?)
2. Determines appropriate prompt role (style/scene/subject/standalone)
3. Translates casual descriptions into precise technical language
4. Suggests modular composition strategies
5. Provides variations and alternative phrasings

**Example workflow:**
```
You: "Help me write a prompt for moody portraits in coffee shops"

Claude: [Launches image-prompt-composer agent]

Agent:
  Let me clarify a few things:
  1. Prompt role - Is this a complete standalone or a style/scene/subject?
  2. Lighting - Natural window light? Warm interior? Dramatic?
  3. Composition - Close portrait? Environmental shot showing cafe?

  [After your answers]

  Here's your structured prompt:
  "Portrait photography, contemplative mood, natural window light,
   soft diffused lighting, coffee shop interior, shallow depth of field,
   bokeh background, warm color temperature, cinematic composition..."

  Variations to consider:
  - More intimate: Add "close-up, direct eye contact"
  - Environmental: Add "visible cafe details, steam from coffee cup"

  Tags: photography, portrait, natural-light, editorial, coffee-shop
  Compatible models: Midjourney v6, DALL-E 3, Stable Diffusion XL
```

**Tools available:** Read, Grep, Glob (focuses on composition, not file operations)

---

## Slash Commands

Commands provide **quick access** to agent workflows without needing to manually describe tasks.

### /image-prompt-metadata [file-path]

**Location:** [.claude/commands/image-prompt-metadata.md](.claude/commands/image-prompt-metadata.md)

**Usage:**
```
/image-prompt-metadata prompts/text-to-image/styles/photography/vintage-film/_style.md
```

Or simply:
```
/image-prompt-metadata
```
(Claude will ask which file)

**What it does:**
Launches the metadata validation agent on a specific file. Same functionality as the agent, but with direct file target.

**Use when:**
- You want to validate/fix YAML on a specific existing file
- You've just created a prompt and need metadata added
- You're unsure if a prompt file meets repo standards

### /image-prompt-composer

**Location:** [.claude/commands/image-prompt-composer.md](.claude/commands/image-prompt-composer.md)

**Usage:**
```
/image-prompt-composer
```

**What it does:**
Enters a focused mode where Claude helps craft text-to-image prompt text through guided questions.

**Use when:**
- You have a rough idea but need help structuring it
- You want to create a new prompt from scratch
- You need variations or alternative phrasings
- You're unsure how to translate casual descriptions into technical language

---

## Repository-Specific Settings

**Location:** [.claude/settings.local.json](.claude/settings.local.json)

```json
{
  "permissions": {
    "allow": [
      "Bash(tree:*)",    // Allow tree command without asking
      "Bash(test:*)"     // Allow test command without asking
    ],
    "deny": [],
    "ask": []
  },
  "outputStyle": "prompt-garden-curator"
}
```

**What this means:**
- Claude can run `tree` and `test` bash commands without asking permission
- All other bash commands require approval (safety measure)
- The "prompt-garden-curator" output style is active by default

---

## Common Use Cases

### 1. Creating a New Modular Style Prompt

**Workflow:**
```
You: "Create a new black-and-white urban photography style with night
      street scenes and pedestrian subjects"

Claude:
1. Checks for similar existing prompts
2. Determines this needs modular composition (style + scene + subject)
3. Verifies ID uniqueness for all components
4. Creates feature branch: feature/urban-bw-photography
5. Copies templates from _system/templates/
6. Fills complete YAML frontmatter
7. Links related prompts via related_prompts field
8. Commits with: "feat(photography): add urban-bw modular style system"
9. Suggests creating PR
```

**Claude handles:**
- ✅ Feature branch creation
- ✅ Template copying
- ✅ Complete YAML generation (all required fields)
- ✅ ID uniqueness validation (grep search)
- ✅ Proper file naming (`_style.md`, `scene-*.md`, `subject-*.md`)
- ✅ Cross-reference linking
- ✅ Semantic commit message
- ✅ Folder structure adherence

### 2. Validating Existing Prompt Metadata

**Workflow:**
```
You: "Check if my vintage-film style prompt has correct metadata"

Claude: [Reads file, validates YAML]

Issues found:
❌ Missing: id, category, version, dates
⚠️  Only 1 tag (needs minimum 3)
⚠️  Description too short (6 chars, needs 10+)

Proposed fixes:
id: vintage-film-photography-style (verified unique ✅)
category: photography
sub_category: vintage
version: 1.0
date_created: 2025-10-05
date_modified: 2025-10-05
tags: [vintage, film-photography, retro, analog, 1970s]
description: Vintage film photography aesthetic with grain texture...

Apply these changes? [Yes/No]
```

**Claude handles:**
- ✅ Complete YAML validation
- ✅ Inference of missing fields from content/path
- ✅ ID uniqueness check (grep)
- ✅ Tag suggestions (minimum 3, relevant, kebab-case)
- ✅ Date formatting (YYYY-MM-DD)
- ✅ Clear before/after presentation

### 3. Editing an Existing Prompt

**Workflow:**
```
You: "Update the urban-bw night street scene to include rain effects"

Claude:
1. Reads existing file
2. Notes current version: 1.0
3. Updates prompt content
4. Increments version to 1.1 (minor update)
5. Updates date_modified to today
6. Preserves ID (never changes existing IDs)
7. Creates feature branch: feature/urban-bw-rain-update
8. Commits: "feat(photography): add rain effects to urban-bw night scene"
```

**Claude handles:**
- ✅ Reading existing file first
- ✅ Semantic versioning (1.0 → 1.1 for enhancement)
- ✅ Updating date_modified
- ✅ Preserving ID (critical for cross-references)
- ✅ Feature branch workflow
- ✅ Descriptive commit message

### 4. Organizing and Cleaning Up Repository

**Workflow:**
```
You: "Find all prompts missing proper YAML and fix them"

Claude:
1. Searches repo: grep -r "^---" prompts/ to find all frontmatter
2. Identifies files with incomplete YAML
3. Creates todo list of files to fix
4. For each file:
   - Validates YAML
   - Infers missing metadata
   - Verifies ID uniqueness
   - Updates file
5. Creates feature branch: feature/yaml-cleanup
6. Commits: "fix(repo): complete YAML frontmatter for 15 prompts"
7. Provides summary report
```

**Claude handles:**
- ✅ Systematic file discovery (Glob/Grep)
- ✅ Batch validation
- ✅ Metadata inference
- ✅ ID conflict detection
- ✅ Single logical commit for related changes
- ✅ Comprehensive reporting

### 5. Creating Properly Labeled Git Commits

**Claude automatically creates semantic commits:**

**Format:**
```
type(scope): description

Types:
- feat: New prompt or feature
- fix: Correct YAML, typo, or bug
- docs: Documentation updates
- refactor: Reorganization without content change
- style: Formatting (not prompt style, but code style)

Scope:
- Category name (photography, illustration, marketing, etc.)

Examples:
✅ feat(photography): add urban-bw style with night scene
✅ fix(marketing): correct email template YAML dates
✅ docs(readme): update YAML schema documentation
✅ refactor(illustration): reorganize fantasy folder structure
```

**What Claude does automatically:**
1. Determines appropriate type based on changes
2. Extracts scope from category/folder
3. Writes concise description focusing on "why" not "what"
4. Ensures one logical change per commit
5. Never commits to main (always feature branch)

**Example commits Claude creates:**
```bash
# Creating new prompt
git commit -m "feat(photography): add film-noir lighting style"

# Fixing metadata
git commit -m "fix(illustration): add missing YAML fields to fantasy-landscape"

# Updating content
git commit -m "feat(marketing): enhance product-email tone with urgency"

# Cleanup
git commit -m "fix(repo): resolve OneDrive conflict files in styles/"

# Documentation
git commit -m "docs(templates): add usage examples to style-template"
```

### 6. Linking Related Prompts

**Workflow:**
```
You: "Link my urban-bw style with the night-street scene"

Claude:
1. Reads both files
2. Adds to _style.md:
   related_prompts:
     - id: urban-bw-scene-night-street
       relationship: companion
       combination_notes: "Combine for classic urban night photography"
3. Adds to scene-night-street.md:
   related_prompts:
     - id: urban-bw-photography-style
       relationship: companion
       combination_notes: "Works with this style for cohesive aesthetic"
4. Updates date_modified and version on both
5. Commits: "feat(photography): link urban-bw style with night-street scene"
```

**Claude handles:**
- ✅ Bidirectional linking
- ✅ Appropriate relationship type (companion/alternative/prerequisite)
- ✅ Combination notes for guidance
- ✅ Version and date updates
- ✅ Single commit for related changes

### 7. Handling OneDrive Conflicts

**Workflow:**
```
You: "I see some OneDrive conflict files in the repo"

Claude:
1. Searches for conflict files: ls -la | grep "OneDrive-Conflict"
2. For each conflict:
   - Checks Git version: git log -- path/to/original.md
   - Reads both conflict and original
   - Determines Git is source of truth
   - Deletes OneDrive conflict file
3. Commits: "fix(repo): resolve OneDrive conflicts, keep Git versions"
```

**Claude handles:**
- ✅ Finding conflict files
- ✅ Verifying Git history
- ✅ Choosing correct version (Git wins)
- ✅ Cleanup commit

---

## Working with Claude: Best Practices

### Do's

✅ **Ask Claude to validate before committing**
```
"Check if this prompt has proper YAML before I commit"
```

✅ **Request complete workflows**
```
"Create a new portrait style prompt with complete metadata and git commit"
```

✅ **Let Claude handle repository mechanics**
```
"Organize these three prompts and link them appropriately"
```

✅ **Use slash commands for focused tasks**
```
/image-prompt-metadata prompts/text-to-image/styles/vintage/_style.md
```

✅ **Ask for batch operations**
```
"Find all prompts missing tags and add appropriate ones"
```

### Don'ts

❌ **Don't manually write YAML** - Let Claude validate/generate
❌ **Don't commit to main** - Claude will use feature branches
❌ **Don't worry about ID uniqueness** - Claude checks with grep
❌ **Don't write vague commit messages** - Claude uses semantic commits
❌ **Don't skip cross-referencing** - Claude suggests related_prompts

---

## How Claude Helps Maintain Repository Health

### 1. Prevents Common Mistakes

**ID conflicts:**
- Always runs `grep -r "id: proposed-id" .` before creating
- Suggests alternatives if conflict found

**Incomplete metadata:**
- Validates all required fields
- Infers missing fields from content/path
- Enforces minimum 3 tags

**Naming violations:**
- Enforces `lowercase-kebab-case` for files/folders
- Validates file role prefixes (`_style.md`, `scene-*.md`)
- Checks YAML ID format

**Git mishaps:**
- Never commits to main
- Always uses feature branches
- Creates semantic commit messages
- One logical change per commit

### 2. Maintains Consistency

**YAML structure:**
- All prompts have identical required fields
- Dates in YYYY-MM-DD format
- Tags in kebab-case
- Semantic versioning

**File organization:**
- Prompts in correct category folders
- Templates copied from `_system/templates/`
- Related prompts properly linked

**Version control:**
- Conventional commit format
- Descriptive commit messages
- Feature branch workflow
- PR-ready branches

### 3. Enables Discovery

**Cross-references:**
- Links related prompts via `related_prompts`
- Suggests companions/alternatives/prerequisites
- Enables prompt graph navigation

**Rich metadata:**
- Comprehensive tags for search
- Usage notes for guidance
- Compatible models listed
- Categories and sub-categories

**Documentation:**
- Descriptions explain purpose
- Combination notes guide usage
- File structure reflects modularity

---

## Advanced Usage

### Custom Agent Invocation

You can explicitly request agent use:

```
You: "Use the metadata agent to validate all files in the photography folder"

Claude: [Launches image-prompt-metadata agent with batch scope]
```

### Multi-step Workflows

Claude can chain operations:

```
You: "Create a new sci-fi illustration style, compose the prompt text,
      add complete YAML, link it with existing space-station scene,
      and commit everything"

Claude:
1. [Launches image-prompt-composer agent] → crafts prompt text
2. [Launches image-prompt-metadata agent] → generates YAML
3. Searches for related space-station scene
4. Links prompts bidirectionally
5. Creates feature branch
6. Commits with semantic message
7. Reports complete workflow
```

### Repository Analysis

```
You: "Show me all prompts that are missing related_prompts links"

Claude:
1. Searches all YAML files: grep -r "related_prompts:" prompts/
2. Identifies files without the field
3. Suggests likely companions based on categories
4. Offers to add links
```

---

## Troubleshooting

### "Claude didn't use a feature branch"

This shouldn't happen with the curator output style active. If it does:
1. Check `.claude/settings.local.json` has `"outputStyle": "prompt-garden-curator"`
2. Explicitly remind: "Always use feature branches, never commit to main"

### "Claude created invalid YAML"

The metadata agent should prevent this. If it happens:
1. Use `/image-prompt-metadata` to validate
2. Report the issue so the agent prompt can be improved

### "Claude didn't check ID uniqueness"

This is a critical step. If skipped:
1. Manually run: `grep -r "id: your-id" .`
2. Remind Claude: "Always verify ID uniqueness with grep"

### "I need to work on main branch temporarily"

Tell Claude explicitly:
```
"I need to commit directly to main this time (I know this breaks the rule)"
```

Claude will warn but comply if you confirm.

---

## Summary

**Claude Code in Prompt Garden is your specialized curator:**

- **Output Style** defines its role and behavior
- **Agents** handle complex metadata and composition tasks
- **Commands** provide quick access to workflows
- **Settings** enable safe, productive operations

**Claude automatically:**
- Validates YAML completeness
- Checks ID uniqueness
- Creates feature branches
- Writes semantic commits
- Links related prompts
- Maintains naming conventions
- Infers missing metadata

**You focus on:**
- Creative prompt content
- Repository goals
- What prompts to create/edit

**Claude handles:**
- Repository mechanics
- Metadata accuracy
- Git workflow
- Organizational consistency

---

## Quick Reference

**Create new prompt:**
```
"Create a [type] prompt for [description]"
```

**Validate metadata:**
```
/image-prompt-metadata path/to/file.md
```

**Compose prompt text:**
```
/image-prompt-composer
```

**Fix batch issues:**
```
"Find all prompts with [issue] and fix them"
```

**Link prompts:**
```
"Link [prompt-a] with [prompt-b] as companions"
```

**Clean up repo:**
```
"Check for YAML issues and OneDrive conflicts"
```

**Commit changes:**
```
"Commit this with a proper semantic message"
```

---

**Claude Code + Prompt Garden = Well-organized, version-controlled, discoverable prompt library** 🌱
