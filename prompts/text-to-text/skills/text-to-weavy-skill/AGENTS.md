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
| Prompt | `prompt` | `variable1`, `variable2`... |
| Concatenator | `prompt` | `prompt1`, `prompt2`... |
| Router | `out` | `in` |
| LLM | `text` | `prompt`, `system_prompt`, `image` |
| NB Pro / Flux | `result` | `prompt`, `image_1` |
| Kling | `video` | `prompt`, `image`, `end_image_url`, `negative_prompt`, `element_1`... |
| Kling Element | `result` | `frontal_image_url`, `reference_image_url1`...`3` |
| Array | `array` | `text` |
| List Selector | `option` | `options` |

### Common edge color/type combos

| Connection | src_color | tgt_color | src_type | tgt_type |
|-----------|-----------|-----------|----------|----------|
| File → Router | `Yambo_Blue` | `Yambo_Orange` | `any` | `any` |
| Router → LLM (image) | `Yambo_Orange` | `Yambo_Purple` | `any` | `image` |
| Router → AI Model (image) | `Yambo_Orange` | `Red` | `any` | `image` |
| Prompt → LLM (sys) | `Yambo_Green` | `Yambo_Purple` | `text` | `text` |
| Prompt → Prompt (variable) | `Yambo_Green` | `Yambo_Green` | `text` | `text` |
| Concat → LLM (prompt) | `Yambo_Green` | `Yambo_Purple` | `text` | `text` |
| LLM → Array | `Yambo_Purple` | `Yambo_Green` | `text` | `text` |
| LLM → AI Model (prompt) | `Yambo_Purple` | `Red` | `text` | `text` |
| Array → Selector | `Yambo_Green` | `Yambo_Green` | `array` | `array` |
| Selector → AI Model | `Yambo_Green` | `Red` | `text` | `text` |
| Kling Element → Kling | `#000000` | `Red` | `kling-element` | `kling-element` |

---

## PYTHON BOILERPLATE

```python
import json
import uuid

def uid():
    return str(uuid.uuid4())

NOW = "2026-01-01T00:00:00.000Z"
UPD = "2026-01-01T00:00:00.000Z"
```

---

## BUILDER: FILE UPLOAD ✅ Verified
`type: "import"` — 460 × 558 — No root `kind`

```python
def make_file_node(node_id, name, x, y):
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "import",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {"output": {"file": {"type": "any", "label": "File", "order": 0, "format": "uri", "description": "The uploaded file"}}},
            "name": name, "description": None, "color": "Yambo_Blue", "label": None, "menu": None, "params": None, "schema": None, "version": 3,
            "dark_color": "Yambo_Blue_Dark", "border_color": "Yambo_Blue_Stroke",
            "files": [], "cameraLocked": False, "selectedIndex": 0, "output": {}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 558
    }
```

---

## BUILDER: TEXT ✅ Verified
`type: "string"` — 460 × 268 — No root `kind` — Default name: `"Text"`

```python
def make_string_node(node_id, name, value, x, y):
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "string",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {"input": {}, "output": {"text": {"id": uid(), "type": "text", "order": 0, "format": "text", "description": "Text"}}},
            "name": name, "description": "", "color": "Yambo_Green", "label": None, "menu": None, "params": None, "schema": None, "version": 3,
            "result": {"string": ""}, "dark_color": "Yambo_Green_Dark", "border_color": "Yambo_Green_Stroke",
            "value": value, "output": {"type": "text", "text": "", "string": ""}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 268
    }
```

---

## BUILDER: PROMPT ✅ Verified
`type: "promptV3"` — 460 × 335 — No root `kind` — Supports `{{variableName}}` inline variables

```python
def make_prompt_node(node_id, name, prompt_text, x, y, variables=None):
    """
    variables: list of (var_name, label, ref_or_none)
    Example: [("variable1", "Variable 1", {"nodeId":"x","outputId":"prompt","string":""})]
    Use {{variable1}} in prompt_text where the value should appear.
    Pass None or [] for a prompt without variables.
    """
    input_handles = {} if variables else []
    input_nodes = []
    if variables:
        for i, (var_name, label, ref) in enumerate(variables):
            input_handles[var_name] = {
                "description": "", "format": "text", "id": uid(),
                "order": i, "required": False, "label": label, "type": "text"
            }
            input_nodes.append([var_name, ref])
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "promptV3",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {"input": input_handles, "output": {"prompt": {"type": "text", "order": 0, "format": "text", "description": "Text prompt"}}},
            "name": name, "description": None, "color": "Yambo_Green", "label": "prompt", "menu": None, "params": None, "schema": None, "version": 3,
            "prompt": prompt_text, "result": {"prompt": prompt_text},
            "dark_color": "Yambo_Green_Dark", "border_color": "Yambo_Green_Stroke",
            "inputNodes": input_nodes, "displayMode": "source-value",
            "output": {"type": "text", "prompt": prompt_text}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 335
    }
```

---

## BUILDER: CONCATENATOR ✅ Verified
`type: "prompt_concat"` — 460 × 368 (2 inputs) — No root `kind`

`additionalPrompt` = intro text BEFORE inputs. `inputNodes` order = concatenation order.

```python
def make_concat_node(node_id, name, input_refs, x, y, additional_prompt=""):
    input_handles = {}
    input_nodes = []
    for i, (hname, ref) in enumerate(input_refs):
        input_handles[hname] = {"type": "text", "label": f"text_{i+1}", "order": i, "format": "text", "description": "Text input"}
        input_nodes.append([hname, ref])
    total_height = 268 + len(input_refs) * 50
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "prompt_concat",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {"input": input_handles, "output": {"prompt": {"type": "text", "label": "combined_text", "format": "text", "description": "The combined text"}}},
            "name": name, "description": "Join multiple text inputs to one output.", "color": "Yambo_Green",
            "label": None, "menu": None, "params": None, "schema": None, "version": 3,
            "dark_color": "Yambo_Green_Dark", "inputNodes": input_nodes, "border_color": "Yambo_Green_Stroke",
            "additionalPrompt": additional_prompt, "result": {"additionalPrompt": additional_prompt},
            "output": {"type": "text", "prompt": ""}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": total_height
    }
```

---

## BUILDER: ROUTER ✅ Verified
`type: "router"` — 250 × 64 — No root `kind`

```python
def make_router_node(node_id, name, x, y):
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "router",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {
                "input": {"in": {"id": uid(), "type": "any", "label": "In", "order": 0, "description": "The input"}},
                "output": {"out": {"id": uid(), "type": "any", "label": "Out", "order": 0, "description": "The output"}}
            },
            "name": name, "description": None, "color": "Yambo_Orange", "label": None, "menu": None, "params": None, "schema": None, "version": 3,
            "dark_color": "Yambo_Orange_Dark", "border_color": "Yambo_Orange_Stroke", "output": {}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 250, "height": 64
    }
```

---

## BUILDER: LLM ✅ Verified
`type: "custommodelV2"` / `data.kind.type = "any_llm"` — 460 × 562 — **No root `kind`** — `isModel: true`

Up to 14 image inputs. `prompt`/`systemPrompt` in `data.kind` only when connected (omit when None).

```python
LLM_MODELS = [
    "anthropic/claude-sonnet-4-5","anthropic/claude-opus-4-6","anthropic/claude-opus-4-5",
    "anthropic/claude-3-haiku","google/gemini-2.0-flash-001","google/gemini-2.5-flash",
    "google/gemini-2.5-flash-lite","google/gemini-3-pro","openai/gpt-4o","openai/gpt-4.1",
    "openai/gpt-5-chat","meta-llama/llama-4-maverick","meta-llama/llama-4-scout"
]

def make_llm_node(node_id, name, model, prompt_ref, sys_ref, image_refs, x, y):
    """
    prompt_ref / sys_ref: text ref or None. Omitted from data.kind when None.
    image_refs: list of (label, ref_or_none). Always pass at least [("image", None)].
    """
    kind_data = {
        "type": "any_llm",
        "images": image_refs if image_refs else [["image", None]],
        "model": {"type": "value", "data": {"type": "string", "value": model}},
        "temperature": {"type": "value", "data": {"type": "float", "value": 0}},
        "thinking": {"type": "value", "data": {"type": "boolean", "value": False}}
    }
    if prompt_ref: kind_data["prompt"] = prompt_ref
    if sys_ref: kind_data["systemPrompt"] = sys_ref

    input_handles = {
        "prompt": {"type": "text", "order": 0, "format": "text", "required": True,
                   "description": "Describe your request from the model"},
        "system_prompt": {"type": "text", "order": 1, "format": "text", "required": False,
                          "description": "Describe the purpose of the model (e.g \"you are a prompt generator\")"}
    }
    if image_refs:
        for i, (label, _) in enumerate(image_refs):
            input_handles[label] = {"type": "image", "label": f"image {i+1}", "order": 2+i,
                                    "format": "uri", "required": False, "description": "Image to analyse"}

    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "custommodelV2",
        "visibility": None, "isModel": True,
        "data": {
            "handles": {"input": input_handles, "output": {"text": {"type": "text", "order": 0, "format": "text", "description": "The LLM response"}}},
            "name": name, "description": "Run any large language model.", "color": "Yambo_Purple",
            "label": None, "menu": None, "model": {"name": "any_llm"},
            "params": {"model": model, "temperature": 0},
            "schema": {
                "model": {"type": "enum", "order": 0, "title": "Model Name", "default": "google/gemini-3-pro",
                    "options": LLM_MODELS, "description": "Name of the model to use"},
                "thinking": {"type": "boolean", "order": 5, "title": "Thinking", "default": False, "required": False,
                    "description": "Enhanced reasoning capabilities for complex task (For supported models only)"},
                "temperature": {"max": 2, "min": 0, "type": "number", "title": "Temperature", "default": 0,
                    "description": "This setting influences the variety in the model's responses. Lower values lead to more predictable and typical responses, while higher values encourage more diverse and less common responses. At 0, the model always gives the same response for a given input."}
            },
            "version": 3, "dark_color": "Yambo_Purple_Dark", "border_color": "Yambo_Purple_Stroke",
            "kind": kind_data,
            "generations": [], "selectedIndex": 0, "cameraLocked": False,
            "result": [], "output": {}, "selectedOutput": 0
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 562
    }
```

---

## BUILDER: NANO BANANA PRO ✅ Verified
`fal-ai/nano-banana-pro/edit` — 460 × 560 — Wildcard — `isModel: true`

Seed = type `"seed"` (object). Resolutions: `1K/2K/4K`. No `output_format`. Inputs refs = `null` when not connected.

```python
def make_nb_pro_node(node_id, name, prompt_ref, image_1_ref, x, y, resolution="1K", aspect_ratio="auto"):
    inputs = [
        [{"id": "prompt", "title": "Prompt", "description": "The prompt for image editing.", "validTypes": ["text"], "required": True}, prompt_ref],
        [{"id": "image_1", "title": "image_1", "description": "The image you want to edit", "validTypes": ["image"], "required": False}, image_1_ref],
    ]
    input_handles = {
        "prompt": {"id": uid(), "type": "text", "label": "prompt", "order": 0, "format": "text", "required": True, "description": "Description of the edits you want to make"},
        "image_1": {"id": uid(), "type": "image", "label": "image_1", "order": 1, "format": "uri", "required": False, "description": "The image you want to edit"},
    }
    parameters = [
        [{"id": "seed", "title": "Seed", "description": "Seed value for random number generator. Uncheck for reproducible results.",
          "constraint": {"type": "seed"}, "defaultValue": {"type": "seed", "value": {"seed": 1, "isRandom": False}}},
         {"type": "value", "data": {"type": "seed", "value": {"seed": 0, "isRandom": True}}}],
        [{"id": "resolution", "title": "Resolution", "description": "The resolution of the image to generate.",
          "constraint": {"type": "enum", "options": ["1K","2K","4K"]}, "defaultValue": {"type": "string", "value": "1K"}},
         {"type": "value", "data": {"type": "string", "value": resolution}}],
        [{"id": "aspect_ratio", "title": "Aspect Ratio", "description": "The aspect ratio of the generated image.",
          "constraint": {"type": "enum", "options": ["auto","1:1","21:9","16:9","3:2","4:3","5:4","4:5","3:4","2:3","9:16"]},
          "defaultValue": {"type": "string", "value": "auto"}},
         {"type": "value", "data": {"type": "string", "value": aspect_ratio}}],
        [{"id": "enable_web_search", "title": "Enable Web Search", "description": "Enable web search for the image generation task.",
          "constraint": {"type": "boolean"}, "defaultValue": {"type": "boolean", "value": False}},
         {"type": "value", "data": {"type": "boolean", "value": False}}],
    ]
    outputs = [{"id": "result", "title": "result", "description": "Result image", "dataType": "image"}]
    kind_data = {
        "type": "wildcard",
        "model": {"type": "predefined", "name": "fal-ai/nano-banana-pro/edit", "version": "fal-ai/nano-banana-pro/edit",
                  "service": "fal_imported", "description": "Google's state-of-the-art image generation and editing model"},
        "inputs": inputs, "parameters": parameters, "outputs": outputs
    }
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "custommodelV2",
        "visibility": None, "isModel": True,
        "data": {
            "handles": {"input": input_handles, "output": {"result": {"id": uid(), "type": "image", "label": "result", "order": 0, "format": "uri", "description": "Result image"}}},
            "name": name, "description": "Google's state-of-the-art image generation and editing model", "color": "Red",
            "label": None,
            "menu": {"icon": "EmojiObjectsIcon", "isModel": True, "displayName": "Gemini 3 Pro (with Nano Banana)"},
            "model": {"name": "fal-ai/nano-banana-pro/edit", "service": "fal_imported", "version": "fal-ai/nano-banana-pro/edit"},
            "params": {"seed": {"seed": 0, "isRandom": True}, "prompt": "", "num_images": 1, "resolution": resolution, "aspect_ratio": aspect_ratio, "enable_web_search": False},
            "schema": {
                "seed": {"type": "seed", "title": "Seed", "required": False, "description": "Seed value for random number generator."},
                "prompt": {"type": "string", "title": "Prompt", "required": True, "description": "The prompt for image editing."},
                "resolution": {"type": "enum", "title": "Resolution", "default": "1K", "options": ["1K","2K","4K"], "required": False},
                "aspect_ratio": {"type": "enum", "title": "Aspect Ratio", "default": "auto", "options": ["auto","1:1","21:9","16:9","3:2","4:3","5:4","4:5","3:4","2:3","9:16"], "required": False},
                "enable_web_search": {"type": "boolean", "title": "Enable Web Search", "default": False, "required": False}
            },
            "version": 3, "kind": kind_data,
            "generations": [], "selectedIndex": 0, "cameraLocked": False,
            "result": [], "output": {}, "selectedOutput": 0
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 560
    }
```

---

## BUILDER: FLUX 2 PRO ✅ Verified
`fal-ai/flux-2-pro` — 460 × 560 — Wildcard — `isModel: true`

Same seed pattern as NB Pro. Uses `image_size` (type `fal_image_size`) instead of resolution/aspect_ratio.

```python
def make_flux_pro_node(node_id, name, prompt_ref, image_1_ref, x, y):
    inputs = [
        [{"id": "prompt", "title": "prompt", "description": "The prompt to generate an image from.", "validTypes": ["text"], "required": True}, prompt_ref],
        [{"id": "image_1", "title": "image_1", "description": "The image you want to edit", "validTypes": ["image"], "required": False}, image_1_ref],
    ]
    input_handles = {
        "prompt": {"id": uid(), "type": "text", "label": "prompt", "format": "text", "required": True, "description": "The prompt to generate an image from."},
        "image_1": {"id": uid(), "type": "image", "label": "image_1", "order": 1, "format": "uri", "required": False, "description": "The image you want to edit"},
    }
    parameters = [
        [{"id": "seed", "title": "Seed", "description": "Seed value for random number generator.",
          "constraint": {"type": "seed"}, "defaultValue": {"type": "seed", "value": {"seed": 1, "isRandom": False}}},
         {"type": "value", "data": {"type": "seed", "value": {"seed": 0, "isRandom": True}}}],
        [{"id": "image_size", "title": "Image Size", "description": "The size of the generated image.",
          "constraint": {"type": "image_size", "options": ["Default","auto","square_hd","square","portrait_4_3","portrait_16_9","landscape_4_3","landscape_16_9"]},
          "defaultValue": {"type": "image_size", "value": {"type": "built_in", "value": "match_input"}}},
         {"type": "value", "data": {"type": "image_size", "value": {"type": "built_in", "value": "match_input"}}}],
    ]
    outputs = [{"id": "result", "title": "result", "description": "Result image", "dataType": "image"}]
    kind_data = {
        "type": "wildcard",
        "model": {"type": "predefined", "name": "fal-ai/flux-2-pro", "version": "fal-ai/flux-2-pro",
                  "service": "fal_imported", "description": "Image generation and editing with FLUX.2 [pro] from Black Forest Labs."},
        "inputs": inputs, "parameters": parameters, "outputs": outputs
    }
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "custommodelV2",
        "visibility": "private", "isModel": True,
        "data": {
            "handles": {"input": input_handles, "output": {"result": {"id": uid(), "type": "image", "label": "result", "order": 0, "format": "uri", "description": "Result image"}}},
            "name": name, "description": "Image generation and editing with FLUX.2 [pro] from Black Forest Labs.", "color": "Red",
            "label": None,
            "menu": {"icon": "EmojiObjectsIcon", "isModel": True, "displayName": "Flux 2 Pro"},
            "model": {"name": "fal-ai/flux-2-pro", "service": "fal_imported", "version": "fal-ai/flux-2-pro"},
            "params": {"seed": {"seed": 0, "isRandom": True}, "prompt": "", "image_size": None, "output_format": "png", "safety_tolerance": "1", "enable_safety_checker": True},
            "schema": {
                "seed": {"type": "seed", "title": "Seed", "required": False},
                "image_size": {"type": "fal_image_size", "title": "Image Size", "default": None,
                    "options": ["Default","auto","square_hd","square","portrait_4_3","portrait_16_9","landscape_4_3","landscape_16_9"], "required": False}
            },
            "version": 3, "kind": kind_data,
            "generations": [], "selectedIndex": 0, "cameraLocked": False,
            "result": [], "output": {}, "selectedOutput": 0
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 560
    }
```

---

## BUILDER: KLING 3 ✅ Verified
`type: "custommodelV2"` / `data.kind.type = "kling"` — 460 × 560 — `isModel: true`

Refs named directly in `data.kind`: `prompt`, `image`, `endImageUrl`, `negativePrompt`, `elements[]`.

```python
def make_kling_node(node_id, name, prompt_ref, image_ref, end_image_ref, neg_prompt_ref, element_refs, x, y,
                    kling_model="3.0 Pro", duration=5, cfg_scale=0.5, aspect_ratio="16:9", generate_audio=False):
    kind_data = {
        "type": "kling",
        "model": {"type": "value", "data": {"type": "string", "value": kling_model}},
        "duration": {"type": "value", "data": {"type": "integer", "value": duration}},
        "cfgScale": {"type": "value", "data": {"type": "float", "value": cfg_scale}},
        "shotType": {"type": "value", "data": {"type": "string", "value": "customize"}},
        "aspectRatio": {"type": "value", "data": {"type": "string", "value": aspect_ratio}},
        "generateAudio": {"type": "value", "data": {"type": "boolean", "value": generate_audio}},
        "elements": element_refs if element_refs else []
    }
    if prompt_ref: kind_data["prompt"] = prompt_ref
    if image_ref: kind_data["image"] = image_ref
    if end_image_ref: kind_data["endImageUrl"] = end_image_ref
    if neg_prompt_ref: kind_data["negativePrompt"] = neg_prompt_ref

    input_handles = {
        "prompt": {"id": uid(), "type": "text", "label": "prompt", "order": 0, "format": "text", "required": True,
                   "description": "Text prompt for video generation."},
        "image": {"id": uid(), "type": "image", "label": "first_frame", "order": 1, "format": "text", "required": False,
                  "description": "The image to be used for the video"},
        "end_image_url": {"id": uid(), "type": "image", "label": "last_frame", "order": 2, "format": "text", "required": False,
                          "description": "The image to be used for the end of the video"},
        "negative_prompt": {"id": uid(), "type": "text", "label": "negative_prompt", "order": 3, "format": "text", "required": False},
    }
    for i, (label, _) in enumerate(element_refs or []):
        input_handles[label] = {"id": uid(), "type": "kling-element", "label": label, "order": 4+i, "format": "uri", "required": False}

    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "custommodelV2",
        "visibility": "private", "isModel": True,
        "data": {
            "handles": {"input": input_handles, "output": {"video": {"type": "video", "label": "video", "order": 0, "format": "uri", "description": "The video result"}}},
            "name": name, "description": "Kling 3.0 Pro: Top-tier image-to-video.", "color": "Red",
            "label": None,
            "menu": {"icon": "EmojiObjectsIcon", "isModel": True, "displayName": "Kling 3 Pro"},
            "model": {"name": "kling"},
            "params": {"model": kling_model, "duration": str(duration), "cfg_scale": cfg_scale, "shot_type": "customize", "aspect_ratio": aspect_ratio, "generate_audio": generate_audio},
            "schema": {
                "model": {"type": "enum", "order": 0, "title": "Model", "default": "Pro", "options": ["3.0 Pro","3.0 Standard"], "required": False},
                "duration": {"max": 15, "min": 3, "type": "integer", "title": "Duration", "default": 5, "required": False},
                "cfg_scale": {"max": 1, "min": 0, "type": "number", "title": "Cfg Scale", "default": 0.5, "required": False},
                "shot_type": {"type": "enum", "title": "Shot Type", "default": "customize", "options": ["customize"], "required": False},
                "aspect_ratio": {"type": "enum", "title": "Aspect Ratio (T2I only)", "default": "16:9", "options": ["16:9","9:16","1:1"], "required": False},
                "generate_audio": {"type": "boolean", "title": "Generate Audio", "default": False, "required": False}
            },
            "version": 3, "kind": kind_data,
            "generations": [], "selectedIndex": 0, "cameraLocked": False,
            "result": [], "output": {}, "selectedOutput": 0
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 560
    }
```

---

## BUILDER: KLING ELEMENT ✅ Verified
`type: "kling_element"` — 460 × 507 — Color `#000000` — `visibility: "public"`

```python
def make_kling_element_node(node_id, name, x, y):
    return {
        "id": node_id, "type": "kling_element",
        "data": {
            "version": 3, "color": "#000000",
            "description": "Provide structured element data for the Kling model",
            "type": "kling_element", "name": name,
            "handles": {
                "input": {
                    "frontal_image_url": {"id": "frontal_image_url", "type": "image", "label": "Frontal Image", "format": "uri", "order": 0, "required": True, "description": "Frontal image URL"},
                    "reference_image_url1": {"id": "reference_image_url1", "type": "image", "label": "Reference Image 1", "format": "uri", "order": 1, "required": True, "description": "Reference image URL"},
                    "reference_image_url2": {"id": "reference_image_url2", "type": "image", "label": "Reference Image 2", "format": "uri", "order": 2, "required": False, "description": "Reference image URL"},
                    "reference_image_url3": {"id": "reference_image_url3", "type": "image", "label": "Reference Image 3", "format": "uri", "order": 3, "required": False, "description": "Reference image URL"}
                },
                "output": {"result": {"id": "result", "type": "kling-element", "label": "Kling Element", "format": "uri", "order": 0, "required": False, "description": "Kling element data"}}
            }
        },
        "isModel": False, "owner": None, "visibility": "public", "locked": False,
        "position": {"x": x, "y": y},
        "createdAt": NOW, "selected": False, "width": 460, "height": 507
    }
```

---

## BUILDER: ARRAY ✅ Verified
`type: "array"` — 460 × 230 (static) / 460 × 278 (dynamic) — No root `kind`

```python
def make_array_node(node_id, name, delimiter, input_ref, x, y):
    """Dynamic array — splits incoming text by delimiter."""
    data = {
        "handles": {
            "input": {"text": {"id": uid(), "type": "text", "order": 0, "format": "text", "required": False, "description": "Text to split into array"}},
            "output": {"array": {"id": uid(), "type": "array", "order": 0, "format": "text", "description": "Array of text items"}}
        },
        "name": name, "description": "Array of elements", "color": "Yambo_Green",
        "label": None, "menu": None, "params": None, "schema": None, "version": 3,
        "array": [""], "result": [], "delimiter": delimiter,
        "dark_color": "Yambo_Green_Dark", "border_color": "Yambo_Green_Stroke",
        "output": {"type": "array", "array": []}
    }
    if input_ref:
        data["inputNode"] = input_ref
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "array",
        "visibility": None, "isModel": False, "data": data,
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 278
    }

def make_static_array_node(node_id, name, items, delimiter, x, y):
    """Static array — fixed list of values."""
    return {
        "id": node_id, "dragHandle": ".node-header", "owner": None, "type": "array",
        "visibility": None, "isModel": False,
        "data": {
            "handles": {
                "input": {"text": {"id": uid(), "type": "text", "order": 0, "format": "text", "required": False, "description": "Text to split into array"}},
                "output": {"array": {"id": uid(), "type": "array", "order": 0, "format": "text", "description": "Array of text items"}}
            },
            "name": name, "description": "Array of elements", "color": "Yambo_Green",
            "label": None, "menu": None, "params": None, "schema": None, "version": 3,
            "array": items, "result": items, "delimiter": delimiter,
            "dark_color": "Yambo_Green_Dark", "border_color": "Yambo_Green_Stroke",
            "output": {"type": "array", "array": items}
        },
        "createdAt": NOW, "updatedAt": UPD, "locked": False,
        "position": {"x": x, "y": y},
        "selected": False, "width": 460, "height": 230
    }
```

---

## BUILDER: LIST SELECTOR ✅ Verified
`type: "muxv2"` — 250 × 102 — No root `kind` — No `dragHandle` — `visibility: "public"`

`isIterator: true` triggers downstream for EACH element.

```python
def make_list_selector_node(node_id, name, options_ref, is_iterator, x, y):
    return {
        "id": node_id, "type": "muxv2",
        "data": {
            "version": 3, "description": "Select an option from a list", "type": "list_selector",
            "name": name,
            "handles": {
                "input": {"options": {"id": uid(), "type": "array", "label": "Options", "format": "array", "required": False, "order": 0, "description": "Array of options to choose from"}},
                "output": {"option": {"id": uid(), "type": "text", "label": "Text", "order": 0, "format": "text", "description": "The selected option", "required": False}}
            },
            "options": options_ref, "delimiter": ",", "list": [], "selected": 0,
            "schema": {"options": {"order": 0, "type": "array", "title": "Options", "exposed": True, "required": False, "description": "Array of options to choose from"}},
            "isIterator": is_iterator, "color": "Yambo_Green",
            "result": "", "output": {"type": "text", "option": ""}, "params": {"options": []}
        },
        "isModel": False, "owner": None, "visibility": "public", "locked": False,
        "position": {"x": x, "y": y},
        "createdAt": NOW,
        "selected": False, "width": 250, "height": 102
    }
```

---

## BUILDER: GROUP ✅ Verified
`type: "custom_group"` — Children: `parentId` = group ID, **relative** positions

```python
def make_group_node(group_id, name, x, y, width, height):
    return {
        "id": group_id, "type": "custom_group",
        "data": {
            "version": 3, "color": "rgba(227, 232, 236, 0.64)",
            "description": "Group of nodes", "type": "custom_group",
            "name": name,
            "handles": {"input": [], "output": []},
            "width": width, "height": height, "labelFontSize": 16
        },
        "position": {"x": x, "y": y},
        "locked": False, "selected": False,
        "width": width, "height": height
    }
# For each child: node["parentId"] = group_id
# Child positions are RELATIVE to group top-left
```

---

## COMPLETE SCRIPT TEMPLATE

```python
import json
import uuid

def uid():
    return str(uuid.uuid4())

NOW = "2026-01-01T00:00:00.000Z"
UPD = "2026-01-01T00:00:00.000Z"

# === Paste all make_* functions from this document ===

# === Declare node IDs ===
ID_FILE = uid()
ID_ROUTER = uid()
# ...

# === Build nodes ===
nodes = []
nodes.append(make_file_node(ID_FILE, "SOURCE IMAGE", 0, 0))
nodes.append(make_router_node(ID_ROUTER, "Router", 0, 640))
# ...

# === Build edges ===
edges = []
edges.append(make_edge(ID_FILE, ID_ROUTER, "file", "in", "Yambo_Blue", "Yambo_Orange", "any", "any"))
# ...

# === Export ===
template = {"nodes": nodes, "edges": edges}
with open("/mnt/user-data/outputs/workflow.json", "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)
print(f"✅ {len(nodes)} nodes, {len(edges)} edges")
```