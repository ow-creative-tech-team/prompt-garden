# image-prompt-metadata

## Description
Validates and creates/fixes YAML frontmatter for text-to-image prompt files, ensuring compliance with Prompt Garden repository standards.

## Usage
```
/image-prompt-metadata [file-path]
```

If no file path provided, Claude will ask which file to validate.

## What This Command Does

This command performs comprehensive YAML metadata validation and correction:

1. **Reads the prompt file** - Analyzes both YAML frontmatter and prompt content
2. **Validates required fields** - Checks all mandatory YAML properties exist
3. **Verifies compliance** - Ensures fields match repo policy (dates, format, ID uniqueness)
4. **Infers missing metadata** - Generates appropriate values from prompt content
5. **Suggests improvements** - Recommends tags, compatible models, related prompts
6. **Updates the file** - Fixes or creates compliant YAML frontmatter

## Validation Checklist

**Required Fields:**
- ✅ `id` - Unique, kebab-case format (`category-subcategory-descriptor`)
- ✅ `title` - Human-readable, descriptive
- ✅ `type` - Must be `text-to-image`
- ✅ `category` - Main category (photography, illustration, 3d-render, digital-art)
- ✅ `description` - Minimum 10 characters, describes what this generates
- ✅ `prompt_role` - One of: `style`, `scene`, `subject`, `standalone`, `template`
- ✅ `tags` - Array with minimum 3 tags in kebab-case
- ✅ `version` - Semantic versioning (1.0, 1.1, 2.0, etc.)
- ✅ `date_created` - ISO 8601 format (YYYY-MM-DD)
- ✅ `date_modified` - ISO 8601 format (YYYY-MM-DD)
- ✅ `format` - Usually `markdown`

**Recommended Fields:**
- 🔹 `sub_category` - Finer categorization
- 🔹 `usage_notes` - Practical application guidance
- 🔹 `related_prompts` - Links to companion/alternative prompts
- 🔹 `compatible_models` - AI models tested/recommended
- 🔹 `author` - Creator identifier

## Validation Rules

1. **ID Uniqueness** - Run `grep -r "id: {proposed-id}" .` to ensure no conflicts
2. **Date Format** - Must be YYYY-MM-DD (ISO 8601)
3. **Type Match** - `type: text-to-image` for this command
4. **Role Validity** - `prompt_role` must be valid for text-to-image (style/scene/subject/standalone/template)
5. **Tag Format** - lowercase-kebab-case, minimum 3 tags
6. **Version Format** - Semantic versioning (major.minor or major.minor.patch)

## Workflow

1. **Read file** - Parse existing YAML and content
2. **Check required fields** - Identify what's missing or incorrect
3. **Analyze prompt content** - Infer appropriate metadata from the prompt text
4. **Verify ID uniqueness** - Grep search if ID exists or needs to be created
5. **Generate/fix YAML** - Create compliant frontmatter
6. **Show before/after** - Display changes to user for confirmation
7. **Update file** - Apply corrections with Edit tool
8. **Report** - Summarize what was fixed

## Example Interaction

**User:** `/image-prompt-metadata text-to-image/styles/photography/vintage-film/_style.md`

**Claude reads file and finds:**
```markdown
---
title: Vintage Film Look
type: text-to-image
tags:
  - vintage
---

## Prompt
Vintage film photography, grain texture, faded colors, 1970s aesthetic...
```

**Claude reports:**
> **YAML Validation Issues Found:**
>
> ❌ Missing: `id`
> ❌ Missing: `category`
> ❌ Missing: `description`
> ❌ Missing: `prompt_role`
> ❌ Missing: `version`
> ❌ Missing: `date_created`
> ❌ Missing: `date_modified`
> ❌ Missing: `format`
> ⚠️  Insufficient tags (has 1, needs minimum 3)
>
> **Proposed YAML:**
> ```yaml
> id: vintage-film-photography-style
> title: Vintage Film Look
> type: text-to-image
> category: photography
> sub_category: vintage
> description: Vintage film photography aesthetic with grain texture, faded colors, and 1970s-era characteristics
> usage_notes: Ideal for nostalgic imagery, retro aesthetics, and period-appropriate scenes
> prompt_role: style
> tags:
>   - vintage
>   - film-photography
>   - retro
>   - 1970s
>   - analog
> compatible_models:
>   - midjourney-v6
>   - stable-diffusion-xl
> version: 1.0
> date_created: 2025-10-04
> date_modified: 2025-10-04
> format: markdown
> ```
>
> **ID Uniqueness Check:** ✅ No conflicts found
>
> Apply these changes?

**User:** Yes

**Claude:**
> Updated [text-to-image/styles/photography/vintage-film/_style.md](text-to-image/styles/photography/vintage-film/_style.md)
>
> ✅ All required fields added
> ✅ Tags expanded to 5 relevant terms
> ✅ ID verified unique: `vintage-film-photography-style`
> ✅ Dates set to today (2025-10-04)
>
> **Next steps:**
> - Consider adding related_prompts if you have companion scenes/subjects
> - Test with compatible models and adjust recommendations
> - Commit: `git commit -m "fix(photography): add complete YAML to vintage-film style"`

## Inference Strategy

When generating missing metadata, Claude will:

1. **ID** - Derive from file path and content (`{category}-{subcategory}-{descriptor}`)
2. **Category** - Extract from folder structure
3. **Sub_category** - Infer from specific style/theme in prompt
4. **Description** - Summarize the prompt's purpose and output
5. **Tags** - Extract key terms from prompt content (medium, style, mood, technical terms)
6. **Prompt_role** - Determine from file name and structure:
   - `_style.md` → `style`
   - `scene-*.md` → `scene`
   - `subject-*.md` → `subject`
   - Standalone files → `standalone`
7. **Compatible_models** - Suggest based on prompt style and complexity
8. **Usage_notes** - Infer from prompt characteristics and style

## What This Command Does NOT Do

- ❌ Rewrite or improve the prompt content itself (use `/image-prompt-composer` for that)
- ❌ Create new files (only validates/fixes existing ones)
- ❌ Handle git operations (use repo curator workflow for commits)

## Related Commands

- `/image-prompt-composer` - Create/enhance text-to-image prompt text
- `/create-prompt` - Complete workflow including file creation and git commit
