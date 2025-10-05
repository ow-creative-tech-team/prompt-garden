# image-prompt-composer

## Description
Helps users transform vague ideas or brief descriptions into structured, detailed text-to-image prompts following Prompt Garden conventions.

## Usage
```
/image-prompt-composer
```

## What This Command Does

This command enters a focused mode where Claude helps you craft a high-quality text-to-image prompt by:

1. **Understanding your vision** - Asks clarifying questions about style, subject, scene, mood, lighting, composition
2. **Determining prompt role** - Is this a style, scene, subject, or standalone prompt?
3. **Building structured description** - Transforms your ideas into technical, detailed prompt language
4. **Suggesting modular composition** - Recommends how to split into style/scene/subject if applicable
5. **Providing variations** - Offers alternative phrasings or parameter adjustments

## Workflow

1. Claude asks: What do you want to create? (describe your vision)
2. Claude clarifies: Style? Scene? Subject? Standalone?
3. Claude probes for technical details:
   - Lighting (natural, studio, dramatic, soft)
   - Composition (centered, rule-of-thirds, close-up, wide)
   - Mood/atmosphere (calm, energetic, mysterious)
   - Medium (photography, illustration, 3D, digital art)
   - Technical specs (camera settings, render style, art technique)
4. Claude drafts the structured prompt text
5. Claude suggests:
   - Variations to try

## Example Interaction

**User:** `/image-prompt-composer`

**Claude:**
> What image do you want to create? Describe your vision, even if it's rough or incomplete.

**User:**
> A moody portrait of someone in a coffee shop

**Claude:**
> Let me help you structure this. A few questions:
>
> 1. **Prompt role** - Is this a complete standalone prompt, or a subject/scene for a specific style?
> 2. **Style** - Photography style? Illustration? What aesthetic?
> 3. **Lighting** - Natural window light? Warm interior? Dramatic shadows?
> 4. **Composition** - Close portrait? Environmental shot showing the cafe?
> 5. **Mood** - Contemplative? Cozy? Melancholic? Busy?

**User:**
> Standalone, photography, natural window light, close portrait, contemplative mood

**Claude:**
> Here's your structured text-to-image prompt:
>
> ```
> Portrait photography, contemplative mood, natural window light, soft diffused lighting, coffee shop interior, shallow depth of field, bokeh background, warm color temperature, cinematic composition, subject in thoughtful pose, environmental portrait, f/2.8 aperture, 50mm lens perspective, professional photography, editorial style
> ```
>
> **Variations to consider:**
> - **More intimate:** Add "close-up, direct eye contact, emotional depth"
> - **Environmental context:** Add "visible cafe details, steam from coffee cup, ambient atmosphere"
> - **Different time:** "Golden hour light through window" or "rainy day soft gray light"
>
> **Suggested tags:** `photography`, `portrait`, `natural-light`, `editorial`, `coffee-shop`, `contemplative`
>
> **Compatible models:** Midjourney v6, DALL-E 3, Stable Diffusion XL
>
> Ready to save this as a prompt file with YAML metadata?

## Notes

- **Focus on description, not YAML** - This command crafts the prompt text; use `/image-prompt-metadata` to handle YAML
- **Technical language** - Translates casual descriptions into precise technical terms AI models understand
- **Modular thinking** - Suggests when to split into style + scene + subject for reusability
- **No file operations** - This command only helps write the prompt text, not save files (unless user explicitly asks)

## Related Commands

- `/image-prompt-metadata` - Validate/create YAML frontmatter for existing prompts
- `/create-prompt` - Complete workflow: compose + metadata + file creation + git commit
