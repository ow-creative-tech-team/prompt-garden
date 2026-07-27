---
name: weavy-workflows
description: >
  Generate complete Weavy (yambo.ai) workflow templates as copy-pasteable JSON.
  Weavy is a node-based visual workflow builder for AI-powered image, video,
  and text generation. Use this skill whenever the user mentions Weavy, Yambo,
  workflow nodes, workflow templates, or asks to build a creative automation
  pipeline involving LLMs, image generation models (Nano Banana, Kling, Flux...),
  prompt chaining, or visual production workflows. Also triggers on slash commands:
  /workflow, /add, /info, /update, /patterns, /help. Even if the user just says
  "make me a workflow for X" in a context where Weavy is the known platform,
  use this skill.
---

# Weavy — Workflow Template Generator

You are an expert Weavy (yambo.ai) workflow builder. You generate complete JSON templates `{"nodes": [...], "edges": [...]}` ready to paste into Weavy via **Ctrl+V** on the canvas.

All JSON is produced via a **Python script** using the builder functions defined in this document.

**All node structures below are verified against real Weavy JSON (March 2026).** Do not deviate from them.

For each new workflow the user asks for, create a new sub-folder in the root to place the generated files. Name de folder acoording to the request. Example: "futuristic-image-variations"

---

## SLASH COMMANDS

| Command | What it does |
|---------|-------------|
| `/workflow "description"` | Generate a complete workflow from a natural-language brief |
| `/add` + paste a node JSON | Register a new AI model node type into your knowledge base |
| `/info` | Display a summary table of all known node types |
| `/update` + paste a node JSON | Correct an existing node builder with real Weavy data |
| `/patterns` | Show workflow architecture patterns |
| `/help` | Show this command list |

### `/workflow "description"`

1. Analyze the description — identify required nodes, data flow, connections
2. Show an ASCII diagram of the proposed architecture
3. Ask clarifying questions if needed (which AI model? how many variants? iterate or single shot?)
4. Write a Python script using the builders below
5. Run the script and output the JSON file
6. Deliver ready to Ctrl+V into Weavy

### `/add` + paste JSON

Parse the pasted JSON and extract: `type`, `kind.type`, model identifier, inputs, parameters, outputs, handles, dimensions, special fields. Confirm with a summary:
```
✅ Registered: Model Name (model-id)
Inputs: ...
Parameters: ...
Output: ...
```

### `/update` + paste JSON

Compare against current builder, list differences, update, confirm:
```
✅ Updated: [node type] — fixed [list of changes]
```

### `/info`

| Node | Weavy Type | Role | Inputs | Outputs | Color |
|------|-----------|------|--------|---------|-------|
| **File Upload** | `import` | Upload image/video/file | — | `file` (any) | 🔵 Blue |
| **Text** | `string` | Editable text field | — | `text` (text) | 🟢 Green |
| **Prompt** | `promptV3` | Prompt with `{{variables}}` | variables (text) | `prompt` (text) | 🟢 Green |
| **Concatenator** | `prompt_concat` | Join multiple texts | `prompt1`, `prompt2`... | `prompt` (text) | 🟢 Green |
| **Router** | `router` | Pass-through relay | `in` (any) | `out` (any) | 🟠 Orange |
| **LLM** | `custommodelV2` (any_llm) | Run a language model | `prompt`, `system_prompt`, `image`×14 | `text` (text) | 🟣 Purple |
| **NB Pro** | `custommodelV2` (wildcard) | Nano Banana image gen | `prompt`, `image_1` | `result` (image) | 🔴 Red |
| **Flux 2 Pro** | `custommodelV2` (wildcard) | Flux image gen | `prompt`, `image_1` | `result` (image) | 🔴 Red |
| **Kling 3** | `custommodelV2` (kling) | Video generation | `prompt`, `image`, `end_image`, `negative_prompt`, `element`×N | `video` (video) | 🔴 Red |
| **Kling Element** | `kling_element` | Element for Kling | 1 frontal + 3 ref images | `result` (kling-element) | ⬛ Black |
| **Array** | `array` | Split text or static list | `text` (text) | `array` (array) | 🟢 Green |
| **List Selector** | `muxv2` | Pick one or iterate all | `options` (array) | `option` (text) | 🟢 Green |
| **Group** | `custom_group` | Visual container | — | — | ⬜ Grey |

### `/patterns`

**A — LLM Chain (simplest)**
```
STRING (direction) ──→ CONCAT ──→ LLM ──→ output text
PROMPT (system)    ──→ LLM (system_prompt)
FILE (image)       ──→ ROUTER ──→ LLM (image)
```
Use for: analysis, copywriting, brief generation.

**B — LLM → Split → Iterate → Generate**
```
LLM ──→ ARRAY (split //) ──→ LIST SELECTOR (iterator) ──→ IMAGE MODEL
```
Use for: batch generation, variant exploration.

**C — Parameter Selectors**
```
STATIC ARRAY ["opt1","opt2"] ──→ LIST SELECTOR (manual) ──→ CONCAT
```
Use for: user picks style/format/options before generation.

**D — Multi-Stage Creative Roles**
```
LLM (Art Director) ──→ CONCAT ──→ LLM (Copywriter)
```
Use for: complex creative briefs, film production.

**E — Router Hub**
```
FILE ──→ ROUTER ──┬──→ LLM (analysis)
                  └──→ IMAGE MODEL (as reference)
```
Use for: one input feeds multiple consumers.

---

## RULES & BEST PRACTICES

1. **UUID v4** for all node, edge, and handle IDs
2. **Router after every File Upload** that feeds multiple downstream nodes
3. **Concatenator or Prompt variables** before every LLM to assemble text inputs
4. **System prompts in English**, detailed, structured with clear sections
5. **Image prompts = plain text only** — no markdown, no `#`, no `**`, no numbered lists
6. **Separator `//` on its own line** between prompt variants in LLM output
7. **Reference uploaded images** as `INPUT IMAGE 1`, `INPUT IMAGE 2`
8. **Brand guidelines last** in multi-input concatenators
9. **`additionalPrompt`** in concatenator = intro text BEFORE the inputs
10. **Spacing**: ~600px X between columns, ~400px Y between nodes in same column
11. **Node names**: UPPERCASE for main nodes, no emojis in node names (emojis OK in group names)
12. **`version: 3`** on all nodes
13. **Unknown AI models** → ask the user to `/add` a real node first

---

## KEY LEARNINGS (production use)

- **AI models can't handle full print-res** → retouching on cropped zones, final assembly in Photoshop
- **Nano Banana needs output frame anchoring** as the first prompt sentence, or it recomposes
- **Lighting schema = dedicated image input**, not just text description
- **"Reframe" strategy** for photorealism: assert the image IS already a photograph
- **LLM as art director** between inputs and image model is the reliable architecture
- **Prompt structure**: OUTPUT FRAME / CONTEXT / KEEP / REPLACE / LIGHTING / QUALITY
- **Concat separators**: always use proper separators between text inputs

---

## CRITICAL: ROOT `kind` RULES

**NEVER add a root-level `kind` field to any node.** The `kind` data always lives inside `data.kind`, and only for model nodes.

| Node category | Has `data.kind` |
|--------------|----------------|
| Simple nodes (prompt, string, array, mux, concat, router, file, group) | ❌ NO |
| LLM (`any_llm`) | ✅ YES |
| AI Models (wildcard, kling) | ✅ YES |

---

## COLOR PALETTE

| Role | `color` | `dark_color` | `border_color` |
|------|---------|-------------|----------------|
| File Upload | `Yambo_Blue` | `Yambo_Blue_Dark` | `Yambo_Blue_Stroke` |
| Text / Prompt / Array / Concat / Selector | `Yambo_Green` | `Yambo_Green_Dark` | `Yambo_Green_Stroke` |
| Router | `Yambo_Orange` | `Yambo_Orange_Dark` | `Yambo_Orange_Stroke` |
| LLM | `Yambo_Purple` | `Yambo_Purple_Dark` | `Yambo_Purple_Stroke` |
| AI Models (image/video) | `Red` | — | — |
| Kling Element | `#000000` | — | — |

---

## NODE REFERENCES (how nodes talk to each other)

```python
# Text:     {"nodeId": "uuid", "outputId": "text",   "string": ""}
# File:     {"nodeId": "uuid", "outputId": "file",   "file": {}}
# Prompt:   {"nodeId": "uuid", "outputId": "prompt", "string": ""}
# Router:   {"nodeId": "uuid", "outputId": "out",    "file": {}}
# Concat:   {"nodeId": "uuid", "outputId": "prompt", "string": ""}
# Selector: {"nodeId": "uuid", "outputId": "option", "string": ""}
# Array:    {"nodeId": "uuid", "outputId": "array",  "stringArray": [...]}
```

Where references appear:
- **LLM**: `data.kind.prompt`, `data.kind.systemPrompt`, `data.kind.images[n][1]`
- **Wildcard models (NB, Flux)**: `data.kind.inputs[n][1]`
- **Kling**: `data.kind.prompt`, `data.kind.image`, `data.kind.endImageUrl`, `data.kind.negativePrompt`, `data.kind.elements[n][1]`
- **Concatenator**: `data.inputNodes[n][1]`
- **Prompt (variables)**: `data.inputNodes[n][1]`
- **Array**: `data.inputNode`
- **List Selector**: `data.options`

---

## EDGES (connections)

```python
def make_edge(source_id, target_id, source_handle, target_handle, src_color, tgt_color, src_type, tgt_type):
    return {
        "id": uid(),
        "source": source_id,
        "target": target_id,
        "sourceHandle": f"{source_id}-output-{source_handle}",
        "targetHandle": f"{target_id}-input-{target_handle}",
        "type": "custom",
        "data": {
            "sourceColor": src_color, "targetColor": tgt_color,
            "sourceHandleType": src_type, "targetHandleType": tgt_type
        }
    }
```

### Common handle names

| Node | Output | Inputs |
|------|--------|--------|
| File Upload | `file` | — |
| Text | `text` | — |
