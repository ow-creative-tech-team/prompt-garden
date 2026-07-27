# Weavy Workflow Generator

Describe a creative workflow in plain language. Get a complete JSON template you paste directly into [Weavy](https://yambo.ai). That's it.

No coding, no manual node wiring. You tell the AI what you want to build, it gives you a workflow ready to run.

## What it does

You talk to an LLM (Claude, GPT, Gemini...) that understands every node type in Weavy - file uploads, prompts, LLMs, image generators, video models, routers, arrays, iterators. You describe a workflow like you'd explain it to a colleague, and it generates the full JSON structure: nodes, connections, system prompts, parameters, everything.

The AI knows the exact structure of these models out of the box:

- **Nano Banana Pro** - image generation & editing
- **Flux 2 Pro** - photorealistic image generation
- **Kling 3** - video generation with first/last frame, negative prompt, and elements
- **Any LLM** - Claude, GPT, Gemini, Llama (as Art Director, Copywriter, Analyst, whatever role you need)

And you can teach it new ones (see `/add` below).

## Install

Everything lives in one file: `SKILL.md`.

### Claude Projects (recommended)

1. Open [claude.ai](https://claude.ai) -> **Projects** -> create a new project (or open one)
2. Go to the project's **Knowledge** section
3. Upload `SKILL.md`
4. Start chatting in that project

Every conversation in the project will have access to the skill. You can keep iterating on workflows across sessions.

### Claude - single conversation

1. Open a new chat on [claude.ai](https://claude.ai)
2. Attach `SKILL.md` to your first message
3. Say what you want to build

This works fine but you'll need to re-attach the file each new conversation.

### ChatGPT

1. Go to **Explore GPTs** -> **Create**
2. In the **Instructions** field, paste the full contents of `SKILL.md`
3. Save and use your custom GPT

Or just attach `SKILL.md` as a file in any conversation.

### Gemini / Other LLMs

Upload `SKILL.md` as an attachment or paste its contents into the system prompt / custom instructions of your platform.

### Code execution

The AI writes a Python script to generate the JSON. If your LLM can execute code (Claude with artifacts, ChatGPT with Code Interpreter), it runs the script and gives you the JSON directly. If not, it gives you the script - save it as `workflow.py` and run `python workflow.py` on your machine. You'll need Python 3, nothing else.

## Commands

Once the skill is loaded, you can use these commands in the chat:

### `/workflow "your description"`

The main one. Describe what you want and the AI builds it.

```
/workflow "take a product photo, analyze it with an Art Director LLM,
generate 5 creative variants, render each with Nano Banana Pro"
```

The AI will:
1. Show you an ASCII diagram of the architecture
2. Ask clarifying questions if needed
3. Generate the JSON
4. Give you a file to download or copy

Then go to Weavy, click on the canvas, and **Ctrl+V** (Cmd+V on Mac). Your workflow appears, fully wired.

### `/add`

Teach the AI a new model it doesn't know yet. Weavy has dozens of AI models and the skill only ships with Nano Banana Pro, Flux 2 Pro, and Kling 3. If you need another one:

1. In Weavy, drop the model node on your canvas
2. Select it -> **Ctrl+C**
3. In your chat, type `/add` and paste what you copied

The AI parses the structure and can now use that model in future workflows.

### `/update`

Fix a node that doesn't paste correctly. Models sometimes get updated on Weavy's side:

1. In Weavy, copy a **working** node of that type -> **Ctrl+C**
2. In your chat, type `/update` and paste

The AI compares, finds the differences, and corrects itself.

### `/info`

Shows a quick reference table of all node types the AI knows: what they do, their inputs and outputs.

### `/patterns`

Shows the 5 standard workflow architectures:
- **LLM Chain** - text in, text out
- **LLM -> Split -> Iterate -> Generate** - one LLM writes N prompts, each triggers an image/video generation
- **Parameter Selectors** - let the user pick options (style, format) before generation
- **Multi-Stage Creative Roles** - Art Director -> Copywriter -> etc. in sequence
- **Router Hub** - one source image distributed to multiple consumers

### `/help`

Shows the command list.

## Tips for good results

**Name your creative roles.** Instead of "use an LLM to write prompts", say "add an Art Director that writes the visual brief" or "a DOP that designs the lighting setup". The AI writes much better system prompts when it has a role to embody.

**Be specific about quantities.** "Generate 12 variants" is better than "generate some variants". The AI will set up the right split/iterate pattern.

**Mention your image model.** "Render with Nano Banana Pro" or "generate video with Kling 3" tells the AI exactly which builder to use.

**Think in columns.** Weavy workflows flow left to right. Inputs on the left, processing in the middle, output on the right. The AI follows this convention.

**Start with a mood reference.** Upload a mood board or reference image as the first File Upload node. It anchors the creative direction for every LLM in the chain.

## Example

```
/workflow "Generative casting sheet with 12 persons. A DOP handles the lighting
setup from a mood reference, a Casting Director generates 12 diverse profiles
from the user brief, and an Art Director synthesizes everything into 12 portrait
prompts for Nano Banana Pro."
```

This generates a 20-node workflow:
- File Upload (mood reference) -> Router
- Text node (casting brief)
- Casting Director LLM -> 12 character profiles
- DOP LLM -> lighting setup
- Art Director LLM -> 12 NB Pro prompts separated by //
- Array splitter -> Iterator (12x) -> Nano Banana Pro

One paste into Weavy. Fill in your mood image and brief. Hit run. 12 portraits.

## What's inside SKILL.md

You don't need to read it - the AI does. But if you're curious:

- All slash command definitions
- 13 verified node builders (Python): File Upload, Text, Prompt (with inline variables), Concatenator, Router, LLM, Nano Banana Pro, Flux 2 Pro, Kling 3, Kling Element, Array, List Selector, Group
- Edge/connection builder with handle names and color conventions
- Node reference format (how nodes pass data to each other)
- Structural rules (which nodes have `kind` fields, which don't - getting this wrong breaks paste)
- Workflow patterns and best practices
- Learnings from production use

Every node structure was verified by copying real nodes from Weavy and comparing field by field. Updated March 2026.

## Troubleshooting

**The JSON doesn't paste into Weavy**
Copy the raw JSON content (the `{"nodes":[...],"edges":[...]}` object), not the Python script. Click somewhere on the canvas first, then Ctrl+V.

**A node shows an error after pasting**
The model structure may have changed on Weavy's side. Copy a working node from Weavy, then use `/update` to sync.

**The AI doesn't know a specific model**
Use `/add` with a real Weavy node. The AI can't guess proprietary model structures.

**I get a Python script instead of a JSON file**
Your LLM doesn't have code execution. Save the script as `workflow.py` and run `python workflow.py` - it outputs the JSON file.

**The workflow is too simple / missing nodes**
Be more specific in your brief. Name the roles, the models, the number of variants. The more context you give, the more complete the result.

Built at [Combo](https://combocombo.ai). Shared because that's always been the way.
