# 🤖 Jatti LLM Model Building Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements-llm.txt
```

### 2. Prepare Training Data
```bash
python scripts/extract_training_data.py \
  "c:\Users\Mr.Singh\Desktop\jatti-lang-final\Punjabi-Language-Jatti-" \
  training_data.jsonl
```

Output: `training_data.jsonl` with 100+ code examples

### 3. Choose Your Path

#### **Option A: Use OpenAI API (Fastest, Recommended for MVP)**
```bash
export OPENAI_API_KEY=sk-...

python scripts/fine_tune.py \
  --step openai \
  --model gpt-3.5-turbo \
  --openai-key $OPENAI_API_KEY
```

**Cost:** $5-50 depending on data size  
**Time:** 30 mins - 2 hours  
**Quality:** Excellent (GPT-3.5 level)

#### **Option B: Local Fine-tuning with CodeLlama (Free, DIY)**
```bash
python scripts/fine_tune.py \
  --step huggingface \
  --hf-model meta-llama/CodeLlama-7b-hf \
  --output-dir ./jatti-codellama-7b \
  --epochs 3 \
  --batch-size 8
```

**Cost:** Free (but needs GPU)  
**Time:** 2-8 hours on RTX 3090 / 20+ hours on CPU  
**Quality:** Good (comparable to GPT-3.5)

---

## Detailed Workflow

### Step 1: Data Collection & Preparation

```bash
# Extract all examples from documentation
python scripts/extract_training_data.py \
  "/path/to/jatti-repo" \
  my_training_data.jsonl
```

This creates a dataset with:
- ✅ 100+ real code examples
- ✅ Multiple categories (basics, functions, loops, strings, etc.)
- ✅ High-quality manual examples
- ✅ Proper formatting for each framework

**Output formats:**
- `training_openai.jsonl` - OpenAI Chat format
- `training_huggingface.json` - Hugging Face format
- `training_lora.jsonl` - LoRA adapter format

### Step 2: Model Selection

| Approach | Model | Pros | Cons |
|----------|-------|------|------|
| **OpenAI API** | GPT-3.5-turbo | Easiest, best quality, minimal setup | Costs money |
| **CodeLlama** | 7B / 13B / 34B | Free, self-hosted, specialized for code | Needs GPU |
| **GPT-2 Fine-tune** | Small GPT-2 | Fast, runs on CPU | Lower quality |
| **Phi** | Microsoft Phi | Lightweight, efficient | Newer, less proven |

**Recommendation:** Start with **GPT-3.5-turbo OpenAI API** for MVP, then transition to **CodeLlama** for long-term self-hosted solution.

### Step 3: Fine-Tuning (Choose One)

#### **Method 1: OpenAI API**

```python
import openai

# 1. Upload training file
with open('training_openai.jsonl', 'rb') as f:
    response = openai.File.create(file=f, purpose='fine-tune')
    file_id = response['id']

# 2. Start fine-tuning job
job = openai.FineTuningJob.create(
    training_file=file_id,
    model="gpt-3.5-turbo",
    hyperparameters={"n_epochs": 3, "batch_size": 32}
)

# 3. Monitor progress
status = openai.FineTuningJob.retrieve(job.id)
print(f"Status: {status.status}")

# 4. Once complete, use fine-tuned model
response = openai.ChatCompletion.create(
    model=status.fine_tuned_model,
    messages=[{"role": "user", "content": "Write hello world in Jatti"}]
)
```

#### **Method 2: Local Hugging Face Fine-tuning**

```python
from scripts.fine_tune import HuggingFaceFinetuner

finetuner = HuggingFaceFinetuner("meta-llama/CodeLlama-7b-hf")
finetuner.fine_tune(
    training_file="training_huggingface.json",
    output_dir="./jatti-codellama",
    epochs=3,
    batch_size=8,
    use_lora=True  # Efficient fine-tuning
)
```

### Step 4: Model Testing

```bash
python scripts/test_model.py \
  --model-path ./jatti-codellama \
  --test-prompts test_prompts.txt
```

### Step 5: Deployment

#### Deploy Inference Server
```bash
# Set environment variables
export MODEL_TYPE=huggingface  # or 'openai'
export MODEL_PATH=./jatti-codellama
export API_PORT=5000

python scripts/llm_server.py
```

#### Test Inference
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a program that adds two numbers"}'
```

---

## Performance Benchmarks

### Expected Quality After Fine-Tuning

| Metric | CodeLlama-7B | GPT-3.5-turbo | Target |
|--------|-------------|---------------|--------|
| Valid Syntax % | 85% | 95% | 90%+ |
| Code Completeness | 0.72 | 0.92 | 0.85+ |
| Jatti-Specific Accuracy | 78% | 98% | 90%+ |
| Avg Generation Time | 2s (GPU) / 30s (CPU) | 1s (API) | <2s |

### Hardware Requirements

**Minimum (CPU only):**
- 8GB RAM
- Training time: 20+ hours per epoch

**Recommended (Single GPU):**
- RTX 3060 (12GB) - 4-6 hours
- RTX 3090 (24GB) - 1-2 hours
- A100 (40GB) - 30 mins

**Cloud Options:**
- Google Colab (free T4, limited time)
- Lambda Labs (~$0.45/hour A100)
- AWS p3 instances (~$3/hour p3.2xlarge)

---

## Optimization Strategies

### 1. LoRA Fine-Tuning (Recommended)
- **70% less GPU memory** compared to full fine-tuning
- **Train in 1-2 hours** instead of 8 hours
- Nearly identical results

### 2. Quantization
- **8-bit quantization** reduces model size by 75%
- Run large models on smaller GPUs

### 3. Data Augmentation
```python
# Generate variations of prompts
augmented_data = augment_prompts(training_data)
# More diverse training = better generalization
```

### 4. Progressive Unfreezing
- Start with frozen base model
- Gradually unfreeze layers during training
- Prevents catastrophic forgetting

---

## Evaluation & Validation

### Syntax Checking
```python
def is_valid_jatti(code: str) -> bool:
    return (
        code.strip().startswith("sun_we") and
        code.strip().endswith("ja_we") and
        code.count("sun_we") == code.count("ja_we")
    )
```

### Semantic Testing (Manual)
1. Test each category: basics, functions, strings, collections, etc.
2. Verify code actually runs
3. Check output correctness

### Test Prompts
```
1. "Print hello world"
2. "Create a function that adds two numbers"
3. "Loop through 1 to 10 and print each"
4. "Create a list and sort it"
5. "Write a program with error handling"
6. "Calculate fibonacci recursively"
7. "Read a file and print its contents"
8. "Create a dictionary with person info"
```

---

## Troubleshooting

### Problem: Out of Memory (OOM)
```python
# Solution 1: Reduce batch size
batch_size = 4  # instead of 8

# Solution 2: Use gradient accumulation
gradient_accumulation_steps = 4

# Solution 3: Enable 8-bit quantization
load_in_8bit=True

# Solution 4: Use LoRA instead of full fine-tuning
use_lora=True
```

### Problem: Poor Performance
```python
# Solution 1: More training data (200+ examples)
# Solution 2: Increase epochs (5-10)
# Solution 3: Lower learning rate (1e-5)
# Solution 4: Different model (try CodeLlama-13B)
```

### Problem: Model Forgets English
```python
# Solution: Add English examples to training data
# Mix Jatti examples with general code examples
# Fine-tune with lower learning rate (prevents drift)
```

---

## Next Steps

1. **Week 1:** Collect data, prepare dataset
2. **Week 2:** Fine-tune OpenAI model (MVP)
3. **Week 3:** Set up inference server + testing
4. **Week 4:** Optional - Train CodeLlama locally for self-hosting
5. **Week 5:** Integration with VS Code extension

---

## Resources

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [CodeLlama Models](https://huggingface.co/meta-llama)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Hugging Face Fine-tuning Guide](https://huggingface.co/docs/transformers/training)

---

## Support

For issues:
1. Check error logs
2. Verify API keys are set correctly
3. Check system resources (GPU/RAM)
4. Review training data quality
5. Try different model/parameters

**Estimated Total Time: 2-4 weeks end-to-end** 🚀
