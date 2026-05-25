#!/usr/bin/env python3
"""
Jatti LLM Model Fine-Tuning Pipeline
Comprehensive setup for training a custom model on Jatti code generation.
Supports both OpenAI API fine-tuning and Hugging Face transformers.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# STEP 1: DATA PREPARATION FOR FINE-TUNING
# ============================================================================

class DataPreparator:
    """Prepare training data in multiple formats for different models."""
    
    @staticmethod
    def prepare_openai_format(training_examples: List[Dict], output_file: str):
        """
        Format data for OpenAI fine-tuning API (Chat Completion format).
        Each example: {"messages": [{"role": "system/user/assistant", "content": "..."}]}
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, example in enumerate(training_examples):
                entry = {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are an expert Jatti programming language code generator.
Jatti is a Punjabi-inspired dynamic programming language.

Core Keywords:
- sun_we (program start), ja_we (program end)
- chilla_we (print), chal_oye (variable), ban (assign)
- kaam (function), wapas_kar (return)
- je (if), nahin_taan_je (elif), nahin_taan (else)
- har_ek (for), jadon_tak (while)
- roko_oye_roko (break), chalo_oye_chalo (continue)
- chal_koshish_karle (try), pakad (catch)

Data Types:
- Numbers: 5, 3.14, -10
- Strings: "hello", 'world'
- Lists: [1, 2, 3]
- Dicts: {"key": "value"}
- Booleans: sach (true), jhoot (false)
- Null: khaali

String Methods:
- vada_likha(text) - uppercase
- chhota_likha(text) - lowercase
- vand_karo(text, delim) - split
- badal_de(text, old, new) - replace
- dhundh_ja(text, substr) - find index
- shuru_hunda(text, prefix) - starts with
- khatam_hunda(text, suffix) - ends with
- saf_karo(text) - trim

Built-in Functions:
- kinna_lamba(obj) - length
- ganao(list) - sum
- sab_ton_vaddha(list) - max
- sab_ton_chhota(list) - min
- chal_sort_hoja(list) - sort
- chal_reverse_hoja(list) - reverse
- range_banao(n) - create range
- kism(obj) - type
- likh(file, content) - write file
- padh(file) - read file

Operators:
- Arithmetic: + - * / % ** (power)
- Comparison: vadha_hai (>) nikka_hai (<) barabar (==) barabar_nahi_hai (!=)
- Logical: ate (and) ya_te (or) nahi (not)

Rules:
1. All programs MUST start with 'sun_we' and end with 'ja_we'
2. Use 4-space indentation
3. Generate clean, idiomatic code
4. Comment with 'fuddu_chiz' where helpful"""
                        },
                        {
                            "role": "user",
                            "content": example["prompt"]
                        },
                        {
                            "role": "assistant",
                            "content": example["code"]
                        }
                    ]
                }
                f.write(json.dumps(entry) + '\n')
        
        logger.info(f"✅ OpenAI format: {output_file} ({len(training_examples)} examples)")
    
    @staticmethod
    def prepare_huggingface_format(training_examples: List[Dict], output_file: str):
        """
        Format data for Hugging Face fine-tuning (instruction-response format).
        Used with models like CodeLlama, CodeT5+, etc.
        """
        formatted = []
        for example in training_examples:
            formatted.append({
                "instruction": example["prompt"],
                "input": "",
                "output": example["code"],
                "category": example.get("category", "general")
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Hugging Face format: {output_file} ({len(formatted)} examples)")
    
    @staticmethod
    def prepare_lora_format(training_examples: List[Dict], output_file: str):
        """
        Format for LoRA (Low-Rank Adaptation) fine-tuning.
        More efficient fine-tuning on limited resources.
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in training_examples:
                entry = {
                    "prompt": example["prompt"],
                    "completion": f"\n{example['code']}",
                    "weight": 1.0
                }
                f.write(json.dumps(entry) + '\n')
        
        logger.info(f"✅ LoRA format: {output_file} ({len(training_examples)} examples)")

# ============================================================================
# STEP 2: OPENAI FINE-TUNING
# ============================================================================

class OpenAIFinetuner:
    """Fine-tune model using OpenAI API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        import openai
        openai.api_key = api_key
        self.client = openai
    
    def upload_training_file(self, file_path: str) -> str:
        """Upload training data file to OpenAI."""
        logger.info(f"Uploading training file: {file_path}")
        
        with open(file_path, 'rb') as f:
            response = self.client.File.create(
                file=f,
                purpose='fine-tune'
            )
        
        file_id = response['id']
        logger.info(f"✅ File uploaded. ID: {file_id}")
        return file_id
    
    def start_fine_tune(self, training_file_id: str, model: str = "gpt-3.5-turbo", 
                       epochs: int = 3, batch_size: int = 32) -> str:
        """Start fine-tuning job."""
        logger.info(f"Starting fine-tuning job...")
        logger.info(f"  Model: {model}")
        logger.info(f"  Training file: {training_file_id}")
        logger.info(f"  Epochs: {epochs}")
        logger.info(f"  Batch size: {batch_size}")
        
        response = self.client.FineTuningJob.create(
            training_file=training_file_id,
            model=model,
            hyperparameters={
                "n_epochs": epochs,
                "batch_size": batch_size,
            }
        )
        
        job_id = response['id']
        logger.info(f"✅ Fine-tuning job started. Job ID: {job_id}")
        return job_id
    
    def check_job_status(self, job_id: str):
        """Check status of fine-tuning job."""
        response = self.client.FineTuningJob.retrieve(job_id)
        
        status = response['status']
        logger.info(f"Job {job_id}: {status}")
        
        if response.get('result_files'):
            logger.info(f"Result file: {response['result_files']}")
        
        return status
    
    def list_jobs(self):
        """List all fine-tuning jobs."""
        response = self.client.FineTuningJob.list()
        
        for job in response['data']:
            logger.info(f"Job {job['id']}: {job['status']} (model: {job['model']})")

# ============================================================================
# STEP 3: HUGGING FACE FINE-TUNING
# ============================================================================

class HuggingFaceFinetuner:
    """Fine-tune CodeLlama or other models using Hugging Face transformers."""
    
    def __init__(self, model_name: str = "meta-llama/CodeLlama-7b-hf"):
        self.model_name = model_name
        logger.info(f"Initializing Hugging Face finetuner with model: {model_name}")
    
    def prepare_lora_config(self):
        """Configure LoRA parameters for efficient fine-tuning."""
        from peft import LoraConfig
        
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        logger.info("✅ LoRA config created")
        return lora_config
    
    def fine_tune(self, training_file: str, output_dir: str, 
                  epochs: int = 3, batch_size: int = 8, 
                  learning_rate: float = 2e-4, use_lora: bool = True):
        """
        Fine-tune model on Jatti code examples.
        
        Args:
            training_file: Path to training data (JSONL or JSON)
            output_dir: Directory to save fine-tuned model
            epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate
            use_lora: Use LoRA for efficient fine-tuning
        """
        try:
            import torch
            from transformers import (
                AutoTokenizer, AutoModelForCausalLM,
                TrainingArguments, Trainer, DataCollatorForLanguageModeling
            )
            from datasets import load_dataset
            from peft import get_peft_model
        except ImportError:
            logger.error("Missing dependencies. Install with:")
            logger.error("pip install torch transformers datasets peft")
            return
        
        logger.info(f"Starting fine-tuning on {self.model_name}")
        
        # Load model and tokenizer
        logger.info("Loading model and tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            load_in_8bit=True
        )
        
        # Apply LoRA if requested
        if use_lora:
            logger.info("Applying LoRA...")
            lora_config = self.prepare_lora_config()
            model = get_peft_model(model, lora_config)
            model.print_trainable_parameters()
        
        # Load dataset
        logger.info(f"Loading training data from {training_file}...")
        dataset = load_dataset('json', data_files=training_file)
        
        def preprocess(examples):
            texts = [f"{ex['instruction']}\n\n{ex['output']}" for ex in examples['instruction']]
            encodings = tokenizer(texts, max_length=512, truncation=True, padding=True)
            return encodings
        
        # Prepare training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            save_steps=100,
            save_total_limit=3,
            logging_steps=10,
            learning_rate=learning_rate,
            fp16=True,
            push_to_hub=False,
        )
        
        # Initialize trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset['train'],
            data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
        )
        
        # Train
        logger.info("🚀 Starting training...")
        trainer.train()
        
        # Save model
        logger.info(f"Saving fine-tuned model to {output_dir}")
        trainer.save_model(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        logger.info("✅ Fine-tuning complete!")
        return output_dir

# ============================================================================
# STEP 4: MODEL EVALUATION
# ============================================================================

class ModelEvaluator:
    """Evaluate fine-tuned model quality."""
    
    @staticmethod
    def evaluate_syntax(code: str) -> bool:
        """Check if generated code has valid Jatti syntax."""
        code = code.strip()
        
        checks = [
            code.startswith("sun_we"),
            code.endswith("ja_we"),
            code.count("sun_we") == code.count("ja_we"),
            "\n" in code,  # Multi-line
        ]
        
        return all(checks)
    
    @staticmethod
    def evaluate_completeness(prompt: str, code: str) -> float:
        """Score how well the code matches the prompt (rough estimate)."""
        prompt_lower = prompt.lower()
        code_lower = code.lower()
        
        # Check for key concepts from prompt appearing in code
        keywords = ["function", "loop", "print", "variable", "list", "dict", "file", "error"]
        matches = sum(1 for kw in keywords if kw in prompt_lower and kw in code_lower)
        
        return min(1.0, matches / max(1, len([kw for kw in keywords if kw in prompt_lower])))
    
    @staticmethod
    def evaluate_batch(test_cases: List[Dict]) -> Dict:
        """Evaluate multiple test cases."""
        results = {
            "valid_syntax": 0,
            "total": len(test_cases),
            "avg_completeness": 0,
            "scores": []
        }
        
        for test in test_cases:
            valid = ModelEvaluator.evaluate_syntax(test["code"])
            completeness = ModelEvaluator.evaluate_completeness(test["prompt"], test["code"])
            
            results["valid_syntax"] += valid
            results["scores"].append({
                "prompt": test["prompt"][:50],
                "valid": valid,
                "completeness": completeness
            })
        
        results["avg_completeness"] = sum(s["completeness"] for s in results["scores"]) / len(results["scores"]) if results["scores"] else 0
        results["syntax_rate"] = results["valid_syntax"] / results["total"] if results["total"] > 0 else 0
        
        return results

# ============================================================================
# MAIN: ORCHESTRATE FINE-TUNING WORKFLOW
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Jatti LLM Fine-Tuning Pipeline")
    parser.add_argument("--step", default="all", choices=["prepare", "openai", "huggingface", "evaluate", "all"],
                       help="Which step to run")
    parser.add_argument("--training-data", default="training_data.jsonl", help="Path to training data")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="OpenAI model to fine-tune")
    parser.add_argument("--hf-model", default="meta-llama/CodeLlama-7b-hf", help="Hugging Face model")
    parser.add_argument("--output-dir", default="./fine_tuned_model", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size")
    
    args = parser.parse_args()
    
    # Step 1: Data Preparation
    if args.step in ["prepare", "all"]:
        logger.info("=" * 60)
        logger.info("STEP 1: Data Preparation")
        logger.info("=" * 60)
        
        # Assume we have training examples (from previous extraction)
        training_examples = [
            {
                "prompt": "Write a program that prints hello world",
                "code": 'sun_we\n    chilla_we "Hello World"\nja_we',
                "category": "basics"
            }
            # ... more examples
        ]
        
        preparer = DataPreparator()
        preparer.prepare_openai_format(training_examples, "training_openai.jsonl")
        preparer.prepare_huggingface_format(training_examples, "training_huggingface.json")
        preparer.prepare_lora_format(training_examples, "training_lora.jsonl")
    
    # Step 2: OpenAI Fine-tuning
    if args.step in ["openai", "all"] and args.openai_key:
        logger.info("=" * 60)
        logger.info("STEP 2: OpenAI Fine-Tuning")
        logger.info("=" * 60)
        
        finetuner = OpenAIFinetuner(args.openai_key)
        file_id = finetuner.upload_training_file("training_openai.jsonl")
        job_id = finetuner.start_fine_tune(file_id, model=args.model, epochs=args.epochs)
        logger.info(f"Monitor progress with: python fine_tune.py --step openai --openai-key <key>")
    
    # Step 3: Hugging Face Fine-tuning
    if args.step in ["huggingface", "all"]:
        logger.info("=" * 60)
        logger.info("STEP 3: Hugging Face Fine-Tuning")
        logger.info("=" * 60)
        
        finetuner = HuggingFaceFinetuner(args.hf_model)
        finetuner.fine_tune(
            "training_huggingface.json",
            args.output_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            use_lora=True
        )
    
    # Step 4: Evaluate
    if args.step in ["evaluate", "all"]:
        logger.info("=" * 60)
        logger.info("STEP 4: Model Evaluation")
        logger.info("=" * 60)
        
        test_cases = [
            {
                "prompt": "Print hello world",
                "code": 'sun_we\n    chilla_we "Hello"\nja_we'
            }
        ]
        
        results = ModelEvaluator.evaluate_batch(test_cases)
        logger.info(f"Syntax validity: {results['syntax_rate']:.1%}")
        logger.info(f"Avg completeness: {results['avg_completeness']:.2f}")

if __name__ == "__main__":
    main()
