# Feedback Summary: `feedback-1st-iteration`

This document consolidates the reviewer feedback across all files in the `feedback-1st-iteration` folder.

## Overall Summary

The overall feedback is that the translation prompts are already fairly strong, but they still need improvement in three main areas:

- making the output sound more native and less literal
- adapting language more precisely to the target market or region
- improving the handling of technical financial terminology

Across the reviews, the most common issue is that some translations are understandable and acceptable, but do not always sound like something a native professional would naturally write in that market. Several reviewers also noted that terminology should be more localized rather than broadly neutral.

Portuguese received the strongest feedback overall, while Italian had the most concern around technical precision.

## Key Cross-Language Themes

### 1. Reduce literal or AI-sounding phrasing

This is the most repeated theme across the folder.

- French feedback says the structure and terminology are good, but several expressions still feel too "AI-generated," too poetic, too literal, or not natural in business French.
- Spanish feedback says many expressions are acceptable, but not always the most natural option a native writer would choose.
- Portuguese feedback suggests only small refinements, but still recommends explicitly instructing the model to avoid literal translation.
- Italian feedback says the translation has improved, but some phrases still feel uncertain, especially in technical business contexts.

### 2. Use region-specific language, not overly generic language

Localization needs to be more specific in some languages.

- Spanish feedback strongly recommends creating two separate prompts: one for Spain and one for Latin American Spanish.
- The reviewer notes that although neutral Spanish can work for financial content, terminology still differs enough by region to justify separate prompt versions.
- Portuguese feedback recommends explicitly requesting European Portuguese rather than a generic Portuguese output.

### 3. Strengthen technical and industry terminology

Several reviewers focused on terminology precision, especially for financial content.

- Chinese feedback highlights that terms like "asset managers" and "alternative managers" must be translated in a way that reflects institutions rather than individuals.
- Italian feedback says highly technical terms should ideally be reviewed by a subject-matter expert because the reviewer could not fully confirm their correctness.
- French feedback is generally positive on terminology, but still suggests that some contextual choices should be more idiomatic and business-appropriate.

### 4. Keep a formal, executive-level tone

Most reviewers agreed that the intended tone is appropriate, but prompts should continue reinforcing:

- formal corporate language
- professional business style
- natural sentence flow for executive readers

## Language-by-Language Summary

## Chinese

**Estimated accuracy:** 70% to 80%

### Main feedback

- The translation is reasonably strong but needs better handling of business terminology.
- Terms referring to business entities should be translated as institutions, not people.
- Political wording should be softened or made more neutral in certain contexts.

### Specific points

- "asset managers" should be translated as `资产管理机构` or `资管机构`, depending on context.
- "alternative managers" should be translated as `另类资产管理机构`.
- Reviewer recommends avoiding or toning down politically sensitive phrasing such as references to the "liberal democratic world order."

### Takeaway

The Chinese prompt should place more emphasis on:

- institutional business terminology
- consistency in finance-specific labels
- avoiding politically sensitive or overly explicit political framing

## French

**Accuracy of original prompt:** 85%  
**Accuracy of new prompt:** 90%

### Main feedback

- The structure is solid.
- The terminology is mostly good.
- The biggest issue is that some phrases still sound unnatural in French.

### Specific points

The reviewer marked expressions that were:

- too poetic
- not natural
- not used in everyday professional French
- not adapted to the context
- occasionally invalid or awkward word choices

Examples of concern include phrasing that sounds overly literary, excessively literal, or not spontaneous enough for native French business writing.

### Takeaway

The French prompt should continue to emphasize:

- natural business French
- avoidance of literal translation
- rejection of overly embellished or "AI-sounding" phrasing

## Italian

**Accuracy of original prompt:** 40%  
**Estimated revised accuracy:** 65% to 70%

### Main feedback

- The translation has improved significantly from the original prompt.
- However, there is still uncertainty around very technical terms.
- The reviewer could not fully validate whether the most specialized finance terminology is correct.

### Specific points

- The reviewer explicitly recommends that very technical terminology should be checked by a consultant or subject-matter expert.
- The translation reads better than before, but accuracy is still not fully reliable in highly technical sections.

### Takeaway

The Italian prompt likely needs the most work in terms of:

- technical finance terminology
- domain-specific reliability
- reducing ambiguity in specialized wording

## Spanish

**Estimated accuracy:** around 90%

### Main feedback

- The translation quality is already strong.
- The main issue is localization strategy rather than basic correctness.
- The reviewer does not recommend a single neutral Spanish prompt for all markets.

### Specific points

- A separate prompt should be created for Spain Spanish.
- A separate prompt should also be created for LATAM Spanish.
- For Spain, the prompt should explicitly request terminology specific to Spain.
- For LATAM, the reviewer suggests using a more general form adapted to that broader audience.

The reviewer also marked:

- acceptable wording that works but is not ideal
- preferred alternatives that sound more native
- clearly incorrect or misspelled wording

### Takeaway

The Spanish prompt should be split by region and should place more emphasis on:

- Spain-specific language for Spain
- LATAM-appropriate language for Latin America
- selecting the most natural financial/business terminology rather than merely acceptable wording

## Portuguese

**Estimated accuracy:** approximately 95%

### Main feedback

- The translation output was very good overall.
- Only very minor changes were needed.
- Most edits were for grammatical consistency rather than substantive translation problems.

### Suggested prompt direction

The reviewer suggested wording along these lines:

> Please translate the text into European Portuguese, avoiding literal translations and respecting Portuguese spelling and punctuation rules. Maintain a formal and professional tone appropriate for a corporate context.

### Supporting review notes

The separate Portuguese review document also reinforces that the translation:

- maintained a formal and executive tone
- sounded natural in European Portuguese
- handled terminology well overall
- required no major human-review flags

### Takeaway

Portuguese is the strongest-performing language in this set. The prompt only needs light refinement to make the regional preference and style requirements explicit.

## Recommended Prompt Improvements

Based on all files in the folder, the main prompt improvements should be:

- explicitly instruct the model to avoid literal translation
- prioritize native, market-specific phrasing over generic correctness
- specify regional variants where needed, especially for Spanish and Portuguese
- reinforce correct financial and institutional terminology
- preserve a formal and professional tone suitable for executive readers
- reduce poetic, embellished, or unnatural wording
- consider expert review for highly technical finance translations, especially in Italian
- include safeguards for politically sensitive phrasing in Chinese where relevant

## Final Takeaway

The current translation prompts are already usable, but they should evolve from being mostly accurate to being market-native and domain-precise. The next iteration should focus less on general fluency and more on regional localization, business authenticity, and technical terminology control.
