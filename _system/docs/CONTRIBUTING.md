# Contributing to Prompt Garden

Thank you for contributing to our prompt library! This guide will help you create high-quality, consistent prompts that integrate smoothly with our system.

## Table of Contents

- [Quick Start](#quick-start)
- [Contribution Workflow](#contribution-workflow)
- [Writing Guidelines](#writing-guidelines)
- [YAML Best Practices](#yaml-best-practices)
- [Code Review Process](#code-review-process)
- [Common Issues](#common-issues)

---

## Quick Start

### First Time Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt-garden
   ```

2. **Configure Git** (if not already done)
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

3. **Familiarize yourself** with:
   - [README.md](README.md) - Full documentation
   - `_system/templates/` - Available templates
   - Existing prompts in your category

### Every Time You Start Work

```bash
# 1. Switch to main branch
git checkout main

# 2. Pull latest changes
git pull origin main

# 3. Create a new feature branch
git checkout -b feature/your-prompt-name
```

---

## Contribution Workflow

### Step-by-Step Process

#### 1. Choose Your Prompt Type

Determine which category and role:

**Categories:**
- `text-to-image/` - Image generation prompts
- `text-to-text/` - Text generation prompts
- `text-to-code/` - Code generation prompts

**Roles:**
- `style` - Base aesthetic/style definition
- `scene` - Environment/setting description
- `subject` - Main subject/character
- `standalone` - Complete, self-contained prompt
- `template` - Reusable component with variables

#### 2. Select the Right Template

Copy from `_system/templates/`:

```bash
# For a style prompt
cp _system/templates/style-template.md text-to-image/styles/photography/my-style/_style.md

# For a scene prompt
cp _system/templates/scene-template.md text-to-image/styles/photography/my-style/scene-night-city.md

# For a standalone prompt
cp _system/templates/standalone-template.md text-to-text/marketing/email-campaign.md
```

#### 3. Name Your File Correctly

**Folder naming:**
- Use `lowercase-kebab-case`
- Be descriptive but concise
- Group related prompts in same folder

**File naming:**
- `_style.md` - For base style (one per style folder)
- `scene-{descriptor}.md` - For scenes
- `subject-{descriptor}.md` - For subjects
- `{descriptive-name}.md` - For standalone/templates

**Examples:**
```
✅ text-to-image/styles/photography/urban-bw/_style.md
✅ text-to-image/styles/photography/urban-bw/scene-rainy-street.md
✅ text-to-text/marketing/product-launch-email.md

❌ text-to-image/UrbanBW/style.md
❌ text-to-image/my_cool_prompt.md
❌ text-to-text/Email Template.md
```

#### 4. Fill in YAML Frontmatter

**Required fields** - must be completed:

```yaml
---
id: unique-kebab-case-id           # Must be unique across repo
title: Human Readable Title         # Clear and descriptive
type: text-to-image                 # text-to-image | text-to-text | text-to-code
category: photography               # Main category
description: What this generates    # Minimum 10 characters
prompt_role: style                  # style | scene | subject | standalone | template
tags:                               # Minimum 3 tags
  - photography
  - black-and-white
  - urban
version: 1.0                        # Start at 1.0
date_created: 2025-10-04           # Today's date (YYYY-MM-DD)
date_modified: 2025-10-04          # Same as created for new prompts
format: markdown                    # markdown | json
---
```

**Optional but recommended:**

```yaml
usage_notes: Ideal for social media posts, square cropping
sub_category: urban-photography
related_prompts:
  - id: urban-bw-scene-night
    relationship: companion
    combination_notes: "Use together for complete night scene"
compatible_models:
  - midjourney-v6
  - dall-e-3
author: your-name
```

#### 5. Write Your Prompt

**Structure your content:**

```markdown
## Prompt

[Your actual prompt text here]

## Usage Examples

[How to use this prompt, with examples]

## Variations

[Alternative versions or modifications]

## Notes

[Any additional context, tips, or warnings]
```

**Tips for good prompts:**
- Be specific and descriptive
- Include technical details (lighting, angles, mood)
- Avoid ambiguous language
- Test with target AI model if possible
- Document what works and what doesn't

#### 6. Link Related Prompts

If your prompt works with others, link them:

```yaml
related_prompts:
  - id: minimalist-scene-studio
    relationship: companion
    combination_notes: "Combine for clean product photography"
  - id: dramatic-lighting-style
    relationship: alternative
    combination_notes: "Alternative to soft lighting approach"
```

**Relationship types:**
- `companion` - Designed to work together
- `alternative` - Different approach for same goal
- `prerequisite` - Must be used before this prompt

#### 7. Validate Your Work

**Before committing, check:**

- [ ] All required YAML fields filled
- [ ] ID is unique (search repo for existing)
- [ ] Tags are relevant and descriptive (min 3)
- [ ] File follows naming convention
- [ ] No typos in YAML keys
- [ ] Dates in YYYY-MM-DD format
- [ ] Version follows semantic versioning (e.g., 1.0, 1.2)
- [ ] Prompt is clear and well-documented

**Optional: Validate YAML syntax**
- Use [yamllint.com](http://www.yamllint.com/)
- Or VS Code YAML extension

#### 8. Commit Your Changes

**Stage your files:**
```bash
git add .
```

**Commit with clear message:**
```bash
git commit -m "feat(photography): add urban-bw style with night scene"
```

**Commit message format:**
```
type(scope): description

Types:
  feat      - New prompt
  fix       - Fix to existing prompt
  docs      - Documentation changes
  refactor  - Reorganization
  style     - Formatting (not prompt style!)

Scope:
  photography, illustration, marketing, etc.

Examples:
  feat(photography): add minimalist product style
  fix(marketing): correct email template variables
  docs(readme): update YAML schema section
  refactor(illustration): reorganize anime styles
```

#### 9. Push to Remote

```bash
git push origin feature/your-prompt-name
```

If this is your first push on this branch:
```bash
git push -u origin feature/your-prompt-name
```

#### 10. Create Pull Request

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select your feature branch
4. Fill in PR template:

```markdown
## What does this PR do?

[Brief description of the prompt(s) you're adding]

## Type of change

- [ ] New prompt
- [ ] Prompt improvement/fix
- [ ] Documentation
- [ ] Refactoring

## Checklist

- [ ] All required YAML fields completed
- [ ] Followed naming conventions
- [ ] Tested prompt (if applicable)
- [ ] Linked related prompts
- [ ] No merge conflicts
```

5. Request review from a team member
6. Wait for approval and feedback

#### 11. Address Review Feedback

If reviewer requests changes:

1. Make updates in your local branch
2. Commit and push:
   ```bash
   git add .
   git commit -m "fix: address review feedback"
   git push
   ```
3. PR automatically updates

#### 12. Merge and Clean Up

After approval:

1. **Merge** (via GitHub interface)
   - Recommended: "Squash and merge"
2. **Delete** feature branch (GitHub prompts you)
3. **Locally, switch back to main:**
   ```bash
   git checkout main
   git pull origin main
   git branch -d feature/your-prompt-name
   ```

---

## Writing Guidelines

### Style Guide

**Do:**
- ✅ Be specific and detailed
- ✅ Use consistent terminology
- ✅ Include technical parameters
- ✅ Test prompts when possible
- ✅ Document variations
- ✅ Note model compatibility

**Don't:**
- ❌ Use vague or ambiguous language
- ❌ Include proprietary/confidential info
- ❌ Copy prompts without attribution
- ❌ Use offensive or controversial content
- ❌ Leave placeholder text (TODO, etc.)

### Prompt Quality Checklist

**A good prompt should:**

- [ ] Generate consistent results
- [ ] Be clearly documented
- [ ] Include usage examples
- [ ] Note any limitations
- [ ] Specify compatible models
- [ ] Link to related prompts (if applicable)
- [ ] Use proper grammar and spelling

### Examples

**❌ Bad prompt:**
```markdown
---
id: prompt1
title: Nice Photo
type: text-to-image
category: photo
description: makes nice photos
prompt_role: standalone
tags:
  - photo
version: 1
date_created: 2025-10-04
date_modified: 2025-10-04
format: markdown
---

## Prompt
A nice photo with good lighting
```

**✅ Good prompt:**
```markdown
---
id: minimalist-product-photography
title: Minimalist Product Photography Style
type: text-to-image
category: photography
sub_category: product
description: Clean, minimalist product photography with soft shadows and white background
usage_notes: Ideal for e-commerce, product catalogs, and professional presentations
prompt_role: style
tags:
  - photography
  - product
  - minimalist
  - commercial
  - clean
related_prompts:
  - id: studio-lighting-soft
    relationship: companion
    combination_notes: "Combine for professional studio look"
compatible_models:
  - midjourney-v6
  - dall-e-3
version: 1.0
date_created: 2025-10-04
date_modified: 2025-10-04
author: jane-doe
format: markdown
---

## Prompt

Professional product photography, minimalist composition, white background, soft studio lighting, subtle shadows, centered composition, high resolution, commercial quality, clean aesthetic, f/8 aperture, diffused light, no distractions

## Usage Examples

**Standalone:**
```
Professional product photography, minimalist composition, [product name], white background, soft studio lighting, subtle shadows, centered composition, high resolution
```

**With subject:**
```
[This style prompt] + wireless headphones floating, slight angle, detail visible
```

## Variations

- **Dark background**: Replace "white background" with "matte black background"
- **Colored backdrop**: Use "gradient [color] background" instead
- **Multiple products**: Add "arranged in clean grid, equal spacing"

## Notes

- Works best with products that have interesting shapes or textures
- Avoid cluttered or complex products
- Lighting should be soft and even
- Center-weighted composition performs better than rule-of-thirds
```

---

## YAML Best Practices

### ID Generation

**Format:** `category-subcategory-descriptor`

**Examples:**
```yaml
# Good IDs
id: urban-bw-scene-rainy-street
id: portrait-natural-subject-business-woman
id: marketing-email-product-launch
id: python-function-data-validation

# Bad IDs
id: prompt123
id: my_prompt
id: Photo Style
```

**Ensuring uniqueness:**
```bash
# Search before creating new ID
grep -r "id: your-proposed-id" .
```

### Date Formatting

**Always use ISO 8601 format:** `YYYY-MM-DD`

```yaml
# Correct
date_created: 2025-10-04
date_modified: 2025-10-04

# Incorrect
date_created: 10/4/2025
date_created: Oct 4, 2025
date_created: 2025-10-4
```

### Versioning

**Use semantic versioning:**

- `1.0` - Initial version
- `1.1` - Minor update (added examples, clarifications)
- `1.2.1` - Patch (typo fix, small tweak)
- `2.0` - Major rewrite or breaking change

**When to increment:**
```yaml
# Typo fix or formatting
1.0 → 1.0.1

# Added usage examples, minor improvements
1.0 → 1.1

# Significant prompt rewrite
1.5 → 2.0
```

### Tags

**Best practices:**
- Minimum 3 tags
- Use lowercase kebab-case
- Be specific but not overly granular
- Include both broad and specific tags

**Good tags:**
```yaml
tags:
  - photography          # Broad category
  - portrait            # Specific type
  - natural-light       # Technical detail
  - outdoor             # Environment
  - professional        # Quality level
```

**Avoid:**
```yaml
tags:
  - good
  - nice
  - prompt
  - image
```

---

## Code Review Process

### What Reviewers Check

**YAML Validation:**
- [ ] All required fields present
- [ ] ID is unique
- [ ] Dates in correct format
- [ ] Version follows semantic versioning
- [ ] Minimum 3 tags
- [ ] No YAML syntax errors

**Content Quality:**
- [ ] Prompt is clear and specific
- [ ] Examples provided
- [ ] Usage notes helpful
- [ ] No typos or grammatical errors
- [ ] Appropriate for category

**Structure:**
- [ ] File in correct location
- [ ] Naming convention followed
- [ ] Related prompts linked properly
- [ ] Format consistent with templates

### Reviewer Guidelines

**As a reviewer:**

1. **Be constructive** - Suggest improvements, don't just criticize
2. **Be specific** - Point to exact lines or sections
3. **Test if possible** - Try the prompt with AI model
4. **Check for duplicates** - Ensure similar prompts don't exist
5. **Approve quickly** - Don't block PRs unnecessarily

**Comment examples:**

✅ **Good feedback:**
```
The prompt looks great! Could you add an example of combining this with
the urban-bw style? Also, consider adding "midjourney-v6" to compatible_models
since this style works well there.
```

❌ **Poor feedback:**
```
This doesn't look right. Fix it.
```

---

## Common Issues

### Issue: Merge Conflicts

**Cause:** Someone else edited the same file

**Solution:**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Git will mark conflicts in your file
# 3. Open file, look for:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> main

# 4. Edit to keep correct version
# 5. Remove conflict markers
# 6. Commit resolution
git add .
git commit -m "fix: resolve merge conflict"
git push
```

### Issue: OneDrive Conflict Files

**Cause:** OneDrive synced while Git was operating

**File appears:** `prompt-name-OneDrive-Conflict-2025-10-04.md`

**Solution:**
```bash
# 1. Check Git version
git log -- path/to/prompt-name.md

# 2. Compare conflict file with Git version
# 3. Keep Git version (source of truth)
# 4. Delete OneDrive conflict file
rm path/to/prompt-name-OneDrive-Conflict-2025-10-04.md

# 5. If needed, commit
git add .
git commit -m "fix: remove OneDrive conflict file"
```

### Issue: YAML Syntax Error

**Symptoms:** File doesn't parse, Obsidian shows errors

**Common mistakes:**
```yaml
# ❌ Incorrect - missing quotes around colon
description: A prompt for: photography

# ✅ Correct
description: "A prompt for: photography"

# ❌ Incorrect - wrong indentation
tags:
- photography
  - portrait

# ✅ Correct
tags:
  - photography
  - portrait

# ❌ Incorrect - date format
date_created: 10/4/2025

# ✅ Correct
date_created: 2025-10-04
```

**Solution:** Validate at [yamllint.com](http://www.yamllint.com/)

### Issue: ID Already Exists

**Error message when committing:** (via script, if implemented)

**Solution:**
```bash
# 1. Search for existing ID
grep -r "id: your-id" .

# 2. Choose a more specific ID
# Instead of: urban-style
# Use: urban-bw-gritty-street

# 3. Update your YAML
id: urban-bw-gritty-street
```

### Issue: Can't Push to Main

**Error:** `You don't have permission to push to main`

**Cause:** Main branch is protected

**Solution:** You should be working on a feature branch!
```bash
# Check your current branch
git branch

# If on main, create feature branch
git checkout -b feature/my-prompt

# Now push to your branch
git push origin feature/my-prompt

# Then create PR on GitHub
```

---

## Questions?

- **Workflow questions**: Ask in team communication channel
- **Git help**: See [GitHub Docs](https://docs.github.com)
- **YAML help**: Check [YAML spec](https://yaml.org/spec/)
- **Bug reports**: Create GitHub issue

---

**Thank you for contributing! 🌱**
