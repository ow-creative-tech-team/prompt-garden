# Folder Structure Guide

This document explains the organization of the Prompt Garden repository.

## Complete Structure

```
prompt-garden/
│
├── _system/                           # Infrastructure & documentation
│   ├── schemas/
│   │   └── prompt-schema.json        # YAML validation schema
│   ├── templates/
│   │   ├── style-template.md         # Base style template
│   │   ├── scene-template.md         # Scene template
│   │   ├── subject-template.md       # Subject template
│   │   ├── standalone-template.md    # Standalone prompt template
│   │   └── template-component.md     # Reusable component template
│   └── docs/
│       └── folder-structure.md       # This file
│
├── text-to-image/                     # Image generation prompts
│   ├── styles/
│   │   ├── photography/              # Photography styles
│   │   │   ├── urban-bw/            # Example: Urban B&W style
│   │   │   │   ├── _style.md        # Base style definition
│   │   │   │   ├── scene-*.md       # Scene variants
│   │   │   │   └── subject-*.md     # Subject variants
│   │   │   ├── portrait-natural/
│   │   │   └── product-studio/
│   │   ├── illustration/             # Illustration styles
│   │   ├── 3d-render/               # 3D rendering styles
│   │   └── digital-art/             # Digital art styles
│   ├── subjects/                     # Standalone subjects (not style-specific)
│   └── templates/                    # Reusable image prompt components
│
├── text-to-text/                      # Text generation prompts
│   ├── creative/                     # Creative writing
│   ├── technical/                    # Technical documentation
│   ├── marketing/                    # Marketing copy
│   └── templates/                    # Reusable text templates
│
├── text-to-code/                      # Code generation prompts
│   ├── functions/                    # Function generation
│   ├── scripts/                      # Script generation
│   ├── snippets/                     # Code snippet generation
│   └── templates/                    # Code templates
│
├── .gitignore                        # Git ignore rules
├── README.md                         # Main documentation
└── CONTRIBUTING.md                   # Contribution guidelines
```

## Design Principles

### 1. Three-Tier Category System

**Tier 1: Type** (`text-to-image`, `text-to-text`, `text-to-code`)
- Top-level categorization by AI model type
- Matches most common AI tool categories

**Tier 2: Category** (`styles`, `subjects`, `creative`, `technical`, etc.)
- Second-level organization by purpose or style type
- Allows for flexible grouping

**Tier 3: Specific Style/Topic** (`photography/urban-bw`, `marketing`, etc.)
- Actual prompt collections
- Contains the working files

### 2. Special Folders

**`_system/`**
- Prefixed with underscore to indicate "not content"
- Contains infrastructure, not prompts
- Three subfolders:
  - `schemas/` - Validation rules
  - `templates/` - Starting templates
  - `docs/` - Additional documentation

**`templates/` (in each category)**
- Reusable components for that category
- Different from `_system/templates/` (infrastructure)
- Contains actual working template prompts

### 3. Style Folder Organization

For `text-to-image/styles/`, each specific style gets its own folder:

```
photography/urban-bw/
├── _style.md              # Base style (the aesthetic foundation)
├── scene-night-rain.md    # Scene: rainy night street
├── scene-day-market.md    # Scene: daytime market
└── subject-pedestrian.md  # Subject: walking person
```

**Why this structure?**
- `_style.md` defines the core look (B&W, gritty, contrast, etc.)
- Scene files add environment context
- Subject files add the main focus
- All can be mixed and matched

### 4. Standalone vs. Modular

**Standalone prompts** go in category root or subjects:
```
text-to-text/marketing/email-product-launch.md
text-to-image/subjects/business-person.md
```

**Modular prompts** stay grouped in style folders:
```
text-to-image/styles/photography/urban-bw/[style+scenes+subjects]
```

## Navigation Patterns

### Finding a Prompt

**By type:**
```
Need image prompt → text-to-image/
Need text prompt  → text-to-text/
Need code prompt  → text-to-code/
```

**By purpose:**
```
Photography style     → text-to-image/styles/photography/
Marketing copy        → text-to-text/marketing/
Python function       → text-to-code/functions/
```

**By modularity:**
```
Want to mix & match   → text-to-image/styles/[category]/[style]/
Want complete prompt  → [category]/[type]/*.md
Reusable component    → [category]/templates/
```

### Creating New Content

**New style:**
```bash
# 1. Create style folder
mkdir -p text-to-image/styles/photography/my-new-style

# 2. Copy base template
cp _system/templates/style-template.md \
   text-to-image/styles/photography/my-new-style/_style.md

# 3. Add scenes/subjects as needed
cp _system/templates/scene-template.md \
   text-to-image/styles/photography/my-new-style/scene-example.md
```

**New standalone prompt:**
```bash
# Copy appropriate template
cp _system/templates/standalone-template.md \
   text-to-text/marketing/my-prompt.md
```

## Folder Naming Rules

### Conventions

- **Case**: `lowercase-kebab-case`
- **Clarity**: Descriptive but concise
- **Consistency**: Match category naming patterns

### Examples

**✅ Good:**
```
urban-bw/
portrait-natural/
product-studio/
email-campaigns/
python-functions/
```

**❌ Bad:**
```
Urban_BW/              # Mixed case
PortraitNatural/       # CamelCase
my folder/             # Spaces
stuff/                 # Not descriptive
```

## File Naming Rules

### By Prompt Role

| Role | Naming Pattern | Example |
|------|----------------|---------|
| Style | `_style.md` | `_style.md` |
| Scene | `scene-{descriptor}.md` | `scene-rainy-night.md` |
| Subject | `subject-{descriptor}.md` | `subject-business-woman.md` |
| Standalone | `{descriptive-name}.md` | `product-hero-shot.md` |
| Template | `template-{component}.md` | `template-lighting.md` |

### Special Prefixes

- `_style.md` - Reserved for base style definition
- `scene-` - Scene/environment prompts
- `subject-` - Subject/character prompts
- `template-` - Reusable components

## Scaling Considerations

### When to Create New Folders

**Create subfolder when:**
- You have 5+ related prompts in same category
- Clear thematic grouping exists
- Prompts are meant to work together

**Keep flat when:**
- Only 1-4 prompts in category
- Prompts are independent
- Over-organization would hurt discoverability

### Example Growth Pattern

**Initial state:**
```
text-to-image/styles/photography/
├── urban-bw/
└── portrait-natural/
```

**After growth:**
```
text-to-image/styles/photography/
├── urban/
│   ├── urban-bw/
│   ├── urban-color/
│   └── urban-neon/
├── portrait/
│   ├── portrait-natural/
│   ├── portrait-studio/
│   └── portrait-environmental/
└── product/
    ├── product-studio/
    ├── product-lifestyle/
    └── product-flat-lay/
```

**When to add depth:**
- 5+ styles in same sub-category
- Clear organizational benefit
- Team consensus

## Cross-Category Linking

Prompts can reference across categories using `related_prompts`:

```yaml
# In text-to-image/styles/photography/product-studio/_style.md
related_prompts:
  - id: product-description-concise
    relationship: companion
    combination_notes: "Use with generated image for product listing"
```

This links an image style with a text-to-text product description prompt.

## Archive Strategy

**Don't delete old prompts.** Instead:

```
text-to-image/styles/photography/
├── urban-bw/
└── _archive/
    └── urban-bw-old-version/
```

**When to archive:**
- Prompt replaced by better version
- No longer relevant but has historical value
- Deprecated but still referenced

**Archive process:**
1. Move folder/file to `_archive/`
2. Add note in old prompt: `This prompt is archived. See: [new-prompt-id]`
3. Update version in new prompt to indicate major change

---

## Quick Reference

**Infrastructure:**
- Templates: `_system/templates/`
- Schemas: `_system/schemas/`
- Docs: `_system/docs/`

**Prompt Categories:**
- Images: `text-to-image/`
- Text: `text-to-text/`
- Code: `text-to-code/`

**Key Files:**
- Main docs: `README.md`
- Contributing: `CONTRIBUTING.md`
- This guide: `_system/docs/folder-structure.md`

---

**Questions?** See [README.md](../../README.md) or create a GitHub issue.
