# 🤖 Jatti LLM Integration Plan

## Overview
Integrate a fine-tuned language model into the Jatti ecosystem to enable **English-to-Jatti code generation** via VS Code extension and IDE support.

---

## Phase 1: Data Preparation

### 1.1 Training Dataset Collection
Create a structured dataset from existing Jatti documentation and examples:

**Sources:**
- BEGINNER_TUTORIAL.md → Extract code examples
- INTERMEDIATE_GUIDE.md → Advanced patterns
- ADVANCED_TOPICS.md → Complex use cases  
- LANGUAGE_SPECIFICATION.md → Language reference
- All .jatti test files

**Format:** JSON with `(english_description, jatti_code)` pairs

```json
{
  "prompt": "Write a program that prints hello world",
  "code": "sun_we\n    chilla_we \"Hello World\"\nja_we",
  "category": "basics"
}
```

### 1.2 Dataset Statistics
- Target: 200-500 code examples minimum
- Categories: basics, functions, loops, strings, collections, files, error-handling, recursion
- Quality: Manual review and validation

---

## Phase 2: Model Fine-Tuning

### 2.1 Base Model Selection

| Model | Pros | Cons | Recommended |
|-------|------|------|-------------|
| **GPT-4 with API** | Best quality, least training effort | Cost per call | ✅ For MVP |
| **CodeLlama** | Open-source, specialized for code | Requires GPU for training | For self-hosted |
| **GPT-3.5-turbo** | Cheaper, fast | Lower code quality | Alternative |

### 2.2 Fine-Tuning Approach

**Option A: OpenAI Fine-tuning API** (Recommended for MVP)
```python
# Use OpenAI's fine-tuning endpoint
# Requires JSONL format with prompt/completion pairs
# Lower cost than training from scratch
```

**Option B: Hugging Face + Transformer**
```python
# Use CodeLlama or CodeT5+
# Full control, but requires computational resources
# Good for long-term self-hosting
```

---

## Phase 3: Backend Service

### 3.1 Inference Server (Python Flask/FastAPI)

**Endpoints:**
```
POST /api/generate
{
  "prompt": "Create a function that adds two numbers",
  "context": "string",
  "max_tokens": 500
}

Response:
{
  "code": "kaam add(a, b)\n    wapas_kar a + b\nja_we",
  "confidence": 0.92,
  "tokens_used": 45
}
```

### 3.2 Configuration
- Model: CodeLlama-34B or GPT-4
- Temperature: 0.3 (deterministic)
- Max tokens: 1000
- Rate limiting: 10 req/min per user

---

## Phase 4: VS Code Extension Integration

### 4.1 New Commands

**Command: `Jatti: Generate Code from Prompt`**
- Keybinding: `Ctrl+Shift+G`
- Input: User enters English description
- Output: Generated Jatti code inserted into editor

**Command: `Jatti: Explain Code`** (Bonus)
- Converts Jatti code to English explanation

### 4.2 UI Components

**Input Panel:**
- Text input for natural language prompt
- Dropdown for code categories (optional)
- "Generate" button with spinner
- "Insert" / "Copy" / "Discard" options

**Output Panel:**
- Generated code with syntax highlighting
- Confidence score
- "Refine" button to regenerate
- "Save as Template" option

### 4.3 Extension Code Structure
```
jatti-vscode-extension-c/
├── src/
│   ├── extension.ts (main)
│   ├── llmClient.ts (API calls)
│   ├── codeGenerator.ts (prompt engineering)
│   └── uiPanel.ts (webview)
├── webview/
│   ├── generate.html
│   └── generate.css
└── resources/
    └── prompts.json
```

---

## Phase 5: Deployment

### 5.1 Local Setup
```bash
# Install Python dependencies
pip install flask transformers torch

# Run inference server
python llm_server.py --model codellama

# VS Code extension connects to localhost:5000
```

### 5.2 Cloud Deployment
```bash
# Option 1: AWS Lambda + API Gateway
# Option 2: Google Cloud Functions
# Option 3: Hugging Face Spaces
# Option 4: Custom Docker on DigitalOcean/Heroku
```

---

## Phase 6: Prompt Engineering

### 6.1 System Prompt Template
```
You are an expert Jatti programming language code generator.
Jatti is a Punjabi-inspired dynamic programming language with:
- Keywords: sun_we, ja_we, chilla_we, chal_oye, ban, kaam, wapas_kar, etc.
- Data types: numbers, strings (quoted), lists [], dicts {}, booleans (sach/jhoot)
- String methods: vada_likha(), chhota_likha(), vand_karo(), badal_de(), etc.
- Built-in functions: kinna_lamba(), ganao(), chal_sort_hoja(), range_banao(), etc.

Generate clean, idiomatic Jatti code. Always wrap in sun_we...ja_we blocks.
```

### 6.2 Few-Shot Examples
Include 3-5 examples in every prompt for context:
```
Example 1:
Prompt: "Print numbers 1 to 5"
Code: "sun_we\n    har_ek i range_banao(5)\n        chilla_we i\nja_we"

Example 2: ...
```

---

## Phase 7: Quality Assurance

### 7.1 Validation Pipeline
- Syntax verification against Jatti compiler
- Runtime testing on generated code
- Confidence score thresholding

### 7.2 Feedback Loop
- User ratings (thumbs up/down)
- Collect failed generations for retraining
- Version tagged datasets

---

## Timeline

| Phase | Duration | Effort |
|-------|----------|--------|
| Data Collection | 2-3 days | Medium |
| Model Fine-tuning | 1-2 weeks | High |
| Backend Service | 3-5 days | Medium |
| VS Code Integration | 5-7 days | High |
| Testing & Deployment | 3-5 days | Medium |
| **Total** | **3-4 weeks** | **High** |

---

## MVP Milestone (Quick Win)

**Done in 2-3 days:**
1. Use OpenAI GPT-4 API directly (no fine-tuning yet)
2. Add simple input dialog to extension
3. Send prompt + Jatti context to API
4. Insert generated code into editor

**Benefits:**
- Validate user experience immediately
- Collect real usage data
- Decide on fine-tuning based on results

---

## Resources Needed

- OpenAI API key ($20-100 credit)
- GPU for fine-tuning (Google Colab free, or AWS p3 instance ~$3/hr)
- Hugging Face account (free)
- VS Code extension development environment

---

## Next Steps

1. **Decision Point**: Which model to use (GPT-4 API vs CodeLlama)?
2. **Data Collection**: Extract and format training examples
3. **MVP Backend**: Create Flask server for inference
4. **Extension Integration**: Add LLM command and UI
5. **Testing**: Manual validation and user feedback

---

**Status**: 🟡 Planning Phase  
**Owner**: You  
**Last Updated**: May 25, 2026
