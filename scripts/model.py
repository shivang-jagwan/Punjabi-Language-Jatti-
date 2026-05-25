"""
Jatti LLM Model Inference Wrapper
Simple interface for loading and using fine-tuned models
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JattiModel:
    """Unified interface for Jatti LLM model inference."""
    
    def __init__(self, 
                 model_type: str = "openai",
                 model_name: str = None,
                 model_path: str = None,
                 api_key: str = None,
                 server_url: str = "http://localhost:5000"):
        """
        Initialize Jatti LLM model.
        
        Args:
            model_type: "openai" or "huggingface"
            model_name: Model identifier (e.g., "gpt-3.5-turbo", "meta-llama/CodeLlama-7b-hf")
            model_path: Path to fine-tuned model (for huggingface)
            api_key: OpenAI API key (auto-loads from env if not provided)
            server_url: Inference server URL (if using remote)
        """
        self.model_type = model_type
        self.model_name = model_name
        self.model_path = model_path
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.server_url = server_url
        self.session = None
        self._use_local = model_path is not None
        
        self._init_model()
    
    def _init_model(self):
        """Initialize model based on type."""
        if self.model_type == "openai":
            self._init_openai()
        elif self.model_type == "huggingface":
            self._init_huggingface()
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def _init_openai(self):
        """Initialize OpenAI API client."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Set environment variable or pass api_key")
        logger.info(f"✅ OpenAI initialized: {self.model_name}")
    
    def _init_huggingface(self):
        """Initialize Hugging Face model."""
        if self._use_local:
            try:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                logger.info(f"Loading Hugging Face model from {self.model_path}...")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
                logger.info("✅ Hugging Face model loaded")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                raise
        else:
            logger.info(f"Will use Hugging Face inference API")
    
    def _system_prompt(self) -> str:
        """Get Jatti language system prompt."""
        return """You are an expert Jatti language programmer. Jatti is a Punjabi programming language.

KEY SYNTAX RULES:
1. All code MUST be wrapped in: sun_we ... ja_we
2. Print: likho()
3. Read input: read()
4. Comments: # comment
5. Functions: function name(params) { ... }
6. Loops: for x in list { ... } or while (cond) { ... }
7. Conditionals: if (cond) { ... } else { ... }

KEYWORDS (27 total):
- Control: if, else, for, while, break, continue, return
- Declaration: function, let, const
- Values: true, false, null
- Special: sun_we, ja_we, import, export, class, new
- Built-ins: typeof, instanceof, delete
- Punctuation: {}, [], (), ;, ,, :, .

BUILT-IN FUNCTIONS:
- likho(value) - Print to screen
- read() - Read input
- write_file(name, content) - Write file
- read_file(name) - Read file
- len(list) - Get length
- type(value) - Get type

STRING METHODS:
- uppercase() - Convert to uppercase
- lowercase() - Convert to lowercase
- split(delimiter) - Split string
- contains(substring) - Check if contains
- concat(str) - Concatenate
- length() - Get length

PUNJABI ALIASES:
- chal_sort_hoja(list) - Sort list ascending
- chal_reverse_hoja(list) - Reverse list

YOUR TASK: Convert user's English description into valid Jatti code. 
- Always wrap code in sun_we...ja_we
- Use proper indentation
- Follow Jatti syntax exactly
- Generate working code examples"""
    
    def generate(self, 
                prompt: str, 
                context: str = "",
                max_tokens: int = 500,
                temperature: float = 0.7) -> str:
        """
        Generate Jatti code from English prompt.
        
        Args:
            prompt: English description of desired code
            context: Optional additional context
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0-1.0)
        
        Returns:
            Generated Jatti code
        """
        if self.model_type == "openai":
            return self._generate_openai(prompt, context, max_tokens, temperature)
        else:
            return self._generate_huggingface(prompt, context, max_tokens, temperature)
    
    def _generate_openai(self, prompt: str, context: str, max_tokens: int, 
                        temperature: float) -> str:
        """Generate using OpenAI API."""
        try:
            import openai
            openai.api_key = self.api_key
            
            user_message = prompt
            if context:
                user_message = f"{context}\n\n{prompt}"
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            code = response.choices[0].message.content
            logger.info(f"Generated code: {len(code)} chars")
            return code
        
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise
    
    def _generate_huggingface(self, prompt: str, context: str, max_tokens: int,
                            temperature: float) -> str:
        """Generate using Hugging Face model."""
        try:
            if self._use_local:
                return self._generate_local(prompt, context, max_tokens, temperature)
            else:
                return self._generate_hf_api(prompt, context, max_tokens, temperature)
        except Exception as e:
            logger.error(f"Hugging Face generation failed: {e}")
            raise
    
    def _generate_local(self, prompt: str, context: str, max_tokens: int,
                       temperature: float) -> str:
        """Generate using local Hugging Face model."""
        import torch
        
        user_message = prompt
        if context:
            user_message = f"{context}\n\n{prompt}"
        
        full_prompt = f"{self._system_prompt()}\n\nUser: {user_message}\n\nAssistant:"
        
        inputs = self.tokenizer(full_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs['input_ids'],
                max_length=len(inputs['input_ids'][0]) + max_tokens,
                temperature=temperature,
                top_p=0.95,
                do_sample=True
            )
        
        code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the generated part
        code = code.split("Assistant:")[-1].strip()
        return code
    
    def _generate_hf_api(self, prompt: str, context: str, max_tokens: int,
                        temperature: float) -> str:
        """Generate using Hugging Face API."""
        hf_token = os.getenv("HUGGINGFACE_API_KEY")
        if not hf_token:
            raise ValueError("HUGGINGFACE_API_KEY not set")
        
        user_message = prompt
        if context:
            user_message = f"{context}\n\n{prompt}"
        
        headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": [self._system_prompt(), user_message],
            "parameters": {
                "max_length": max_tokens,
                "temperature": temperature
            }
        }
        
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{self.model_name}",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"API error: {response.text}")
        
        result = response.json()
        return result[0].get("generated_text", "")
    
    def validate(self, code: str) -> Dict[str, any]:
        """
        Validate Jatti code.
        
        Args:
            code: Jatti code to validate
        
        Returns:
            Validation result with is_valid, errors, warnings
        """
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for sun_we...ja_we wrapper
        if "sun_we" not in code:
            result["errors"].append("Missing 'sun_we' at start")
            result["is_valid"] = False
        
        if "ja_we" not in code:
            result["errors"].append("Missing 'ja_we' at end")
            result["is_valid"] = False
        
        # Count braces
        open_braces = code.count("{")
        close_braces = code.count("}")
        if open_braces != close_braces:
            result["errors"].append(f"Brace mismatch: {open_braces} vs {close_braces}")
            result["is_valid"] = False
        
        # Check for valid keywords
        valid_keywords = {"if", "else", "for", "while", "function", "return", 
                         "true", "false", "let", "const", "sun_we", "ja_we"}
        
        return result
    
    def explain(self, code: str) -> str:
        """
        Explain what Jatti code does (OpenAI only).
        
        Args:
            code: Jatti code to explain
        
        Returns:
            English explanation
        """
        if self.model_type != "openai":
            raise NotImplementedError("Explanation only available for OpenAI models")
        
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are expert at explaining Jatti code"},
                    {"role": "user", "content": f"Explain this Jatti code:\n\n{code}"}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            explanation = response.choices[0].message.content
            return explanation
        
        except Exception as e:
            logger.error(f"Explanation failed: {e}")
            raise
    
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """
        Generate code for multiple prompts.
        
        Args:
            prompts: List of English prompts
            **kwargs: Additional arguments for generate()
        
        Returns:
            List of generated Jatti code
        """
        results = []
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"Generating [{i}/{len(prompts)}]...")
            code = self.generate(prompt, **kwargs)
            results.append(code)
        
        return results
    
    def benchmark(self, test_prompts: List[str]) -> Dict[str, any]:
        """
        Benchmark model on test prompts.
        
        Args:
            test_prompts: List of prompts to benchmark
        
        Returns:
            Benchmark results with success rate, avg tokens, etc.
        """
        results = {
            "total": len(test_prompts),
            "successful": 0,
            "valid_syntax": 0,
            "avg_length": 0,
            "generations": []
        }
        
        total_length = 0
        
        for prompt in test_prompts:
            try:
                code = self.generate(prompt)
                validation = self.validate(code)
                
                results["generations"].append({
                    "prompt": prompt,
                    "code": code,
                    "valid": validation["is_valid"]
                })
                
                results["successful"] += 1
                if validation["is_valid"]:
                    results["valid_syntax"] += 1
                
                total_length += len(code)
            
            except Exception as e:
                logger.error(f"Failed on prompt: {prompt[:50]}... ({e})")
        
        if results["successful"] > 0:
            results["avg_length"] = total_length // results["successful"]
            results["success_rate"] = results["successful"] / results["total"]
            results["syntax_rate"] = results["valid_syntax"] / results["successful"]
        
        return results

# Convenience functions for quick usage
def load_model(config_file: str = "jatti_llm_config.json") -> JattiModel:
    """Load model from configuration file."""
    if not Path(config_file).exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file) as f:
        config = json.load(f)
    
    model_type = config.get("model_type", "openai")
    model_config = config.get(model_type, {})
    
    return JattiModel(
        model_type=model_type,
        model_name=model_config.get("model"),
        model_path=config.get("inference", {}).get("model_path"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python model.py <prompt>")
        sys.exit(1)
    
    prompt = " ".join(sys.argv[1:])
    
    try:
        model = load_model()
        code = model.generate(prompt)
        print("\n" + "="*60)
        print("Generated Jatti Code:")
        print("="*60)
        print(code)
        print("="*60)
        
        validation = model.validate(code)
        print(f"\nValidation: {'✅ VALID' if validation['is_valid'] else '❌ INVALID'}")
        if validation["errors"]:
            for err in validation["errors"]:
                print(f"  - {err}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
