#!/usr/bin/env python3
"""
Jatti LLM Quick-Start Automation
One-command setup: extract data → fine-tune → test → deploy
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Optional
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JattiModelQS:
    """Quick-start orchestrator for Jatti LLM model building."""
    
    def __init__(self, repo_path: str, config_file: str = "jatti_llm_config.json"):
        self.repo_path = Path(repo_path)
        self.config_file = self.repo_path / config_file
        self.config = self.load_config()
        self.scripts_dir = self.repo_path / "scripts"
    
    def load_config(self) -> dict:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Default configuration."""
        return {
            "model_type": "openai",
            "openai": {
                "model": "gpt-3.5-turbo",
                "api_key": "${OPENAI_API_KEY}",
                "epochs": 3,
                "batch_size": 32
            },
            "huggingface": {
                "model": "meta-llama/CodeLlama-7b-hf",
                "epochs": 3,
                "batch_size": 8,
                "use_lora": True,
                "output_dir": "./jatti_codellama_ft"
            },
            "data": {
                "train_file": "training_data.jsonl",
                "test_size": 0.1,
                "seed": 42
            },
            "inference": {
                "port": 5000,
                "host": "localhost",
                "model_path": None
            }
        }
    
    def save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        logger.info(f"✅ Config saved to {self.config_file}")
    
    def step1_extract_data(self) -> bool:
        """Step 1: Extract training data from documentation."""
        logger.info("\n" + "="*60)
        logger.info("STEP 1: Extract Training Data")
        logger.info("="*60)
        
        cmd = [
            sys.executable,
            str(self.scripts_dir / "extract_training_data.py"),
            str(self.repo_path),
            str(self.repo_path / self.config["data"]["train_file"])
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(result.stdout)
            logger.info("✅ Data extraction complete")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Data extraction failed: {e.stderr}")
            return False
    
    def step2_fine_tune(self) -> bool:
        """Step 2: Fine-tune model."""
        logger.info("\n" + "="*60)
        logger.info("STEP 2: Fine-Tune Model")
        logger.info("="*60)
        
        model_type = self.config.get("model_type", "openai")
        
        if model_type == "openai":
            return self.step2_openai()
        elif model_type == "huggingface":
            return self.step2_huggingface()
        else:
            logger.error(f"Unknown model type: {model_type}")
            return False
    
    def step2_openai(self) -> bool:
        """Fine-tune with OpenAI API."""
        logger.info("Using OpenAI API for fine-tuning...")
        
        openai_config = self.config["openai"]
        api_key = os.getenv("OPENAI_API_KEY", openai_config["api_key"])
        
        if not api_key or api_key == "${OPENAI_API_KEY}":
            logger.error("❌ OPENAI_API_KEY not set. Set environment variable and try again.")
            logger.error("   export OPENAI_API_KEY=sk-...")
            return False
        
        cmd = [
            sys.executable,
            str(self.scripts_dir / "fine_tune.py"),
            "--step", "openai",
            "--model", openai_config["model"],
            "--openai-key", api_key,
            "--training-data", str(self.repo_path / self.config["data"]["train_file"])
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(result.stdout)
            logger.info("✅ OpenAI fine-tuning job submitted")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Fine-tuning failed: {e.stderr}")
            return False
    
    def step2_huggingface(self) -> bool:
        """Fine-tune with Hugging Face."""
        logger.info("Using Hugging Face for fine-tuning...")
        
        hf_config = self.config["huggingface"]
        
        cmd = [
            sys.executable,
            str(self.scripts_dir / "fine_tune.py"),
            "--step", "huggingface",
            "--hf-model", hf_config["model"],
            "--output-dir", hf_config["output_dir"],
            "--epochs", str(hf_config["epochs"]),
            "--batch-size", str(hf_config["batch_size"]),
            "--training-data", str(self.repo_path / self.config["data"]["train_file"])
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(result.stdout)
            logger.info("✅ Hugging Face fine-tuning complete")
            self.config["inference"]["model_path"] = hf_config["output_dir"]
            self.save_config()
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Fine-tuning failed: {e.stderr}")
            return False
    
    def step3_test_model(self) -> bool:
        """Step 3: Test fine-tuned model."""
        logger.info("\n" + "="*60)
        logger.info("STEP 3: Test Model")
        logger.info("="*60)
        
        model_type = self.config.get("model_type", "openai")
        model_path = self.config["inference"].get("model_path")
        
        cmd = [
            sys.executable,
            str(self.scripts_dir / "test_model.py"),
            "--model-type", model_type
        ]
        
        if model_path:
            cmd.extend(["--model-path", model_path])
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            logger.info(result.stdout)
            logger.info("✅ Model testing complete")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Model testing failed: {e.stderr}")
            return False
    
    def step4_start_server(self) -> bool:
        """Step 4: Start inference server."""
        logger.info("\n" + "="*60)
        logger.info("STEP 4: Start Inference Server")
        logger.info("="*60)
        
        model_type = self.config.get("model_type", "openai")
        model_path = self.config["inference"].get("model_path")
        port = self.config["inference"].get("port", 5000)
        host = self.config["inference"].get("host", "localhost")
        
        # Set environment variables
        env = os.environ.copy()
        env["LLM_PROVIDER"] = model_type
        env["MODEL_NAME"] = self.config[model_type]["model"]
        env["PORT"] = str(port)
        
        if model_path:
            env["MODEL_PATH"] = model_path
        
        if "OPENAI_API_KEY" not in env and model_type == "openai":
            env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
        
        cmd = [
            sys.executable,
            str(self.scripts_dir / "llm_server.py")
        ]
        
        logger.info(f"🚀 Starting inference server on {host}:{port}...")
        logger.info(f"   Provider: {model_type}")
        logger.info(f"   Health check: http://{host}:{port}/health")
        logger.info(f"   Generate: curl -X POST http://{host}:{port}/api/generate \\")
        logger.info(f"             -H 'Content-Type: application/json' \\")
        logger.info(f"             -d '{{\"prompt\": \"Write hello world in Jatti\"}}'")
        
        try:
            subprocess.run(cmd, env=env, check=False)
            return True
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
            return True
    
    def run_full_pipeline(self, skip_steps: list = None) -> bool:
        """Run complete pipeline: extract → fine-tune → test → serve."""
        skip_steps = skip_steps or []
        
        logger.info("\n" + "🚀" * 30)
        logger.info("JATTI LLM QUICK-START PIPELINE")
        logger.info("🚀" * 30)
        
        steps = [
            ("extract", self.step1_extract_data),
            ("finetune", self.step2_fine_tune),
            ("test", self.step3_test_model),
            ("serve", self.step4_start_server)
        ]
        
        for step_name, step_func in steps:
            if step_name in skip_steps:
                logger.info(f"⏭️  Skipping: {step_name}")
                continue
            
            success = step_func()
            if not success and step_name != "serve":
                logger.error(f"❌ Pipeline failed at step: {step_name}")
                return False
        
        logger.info("\n" + "✅" * 30)
        logger.info("PIPELINE COMPLETE!")
        logger.info("✅" * 30)
        return True

def main():
    parser = argparse.ArgumentParser(description="Jatti LLM Quick-Start")
    parser.add_argument("repo_path", help="Path to Jatti repository")
    parser.add_argument("--step", choices=["extract", "finetune", "test", "serve", "all"],
                       default="all", help="Which step to run")
    parser.add_argument("--config", default="jatti_llm_config.json", help="Config file")
    parser.add_argument("--skip", nargs="+", default=[], help="Steps to skip")
    parser.add_argument("--save-config", action="store_true", help="Save config and exit")
    
    args = parser.parse_args()
    
    qs = JattiModelQS(args.repo_path, args.config)
    
    if args.save_config:
        qs.save_config()
        logger.info("✅ Configuration file created/updated")
        return
    
    if args.step == "all":
        qs.run_full_pipeline(skip_steps=args.skip)
    else:
        step_map = {
            "extract": qs.step1_extract_data,
            "finetune": qs.step2_fine_tune,
            "test": qs.step3_test_model,
            "serve": qs.step4_start_server
        }
        step_map[args.step]()

if __name__ == "__main__":
    main()
