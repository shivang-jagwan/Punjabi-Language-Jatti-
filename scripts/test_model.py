#!/usr/bin/env python3
"""
Jatti Model Testing & Evaluation
Test fine-tuned models on various prompts and evaluate results.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# TEST SUITE
# ============================================================================

TEST_PROMPTS = {
    "basics": [
        {
            "prompt": "Write a program that prints 'Hello World'",
            "keywords": ["sun_we", "ja_we", "chilla_we", "Hello World"]
        },
        {
            "prompt": "Create a variable named 'x' with value 5 and print it",
            "keywords": ["sun_we", "ja_we", "chal_oye", "ban", "x", "5", "chilla_we"]
        },
        {
            "prompt": "Print the sum of 10 and 15",
            "keywords": ["10", "15", "+", "chilla_we"]
        }
    ],
    "functions": [
        {
            "prompt": "Write a function that adds two numbers and returns the result",
            "keywords": ["kaam", "wapas_kar", "+"]
        },
        {
            "prompt": "Create a function named 'greet' that takes a name and prints a greeting",
            "keywords": ["kaam", "greet", "chilla_we"]
        },
        {
            "prompt": "Function that calculates factorial of a number recursively",
            "keywords": ["kaam", "factorial", "wapas_kar", "*"]
        }
    ],
    "loops": [
        {
            "prompt": "Loop from 1 to 10 and print each number",
            "keywords": ["har_ek", "range_banao", "chilla_we"]
        },
        {
            "prompt": "While loop that prints numbers from 1 to 5",
            "keywords": ["jadon_tak", "chal_oye", "ban", "chilla_we"]
        },
        {
            "prompt": "Loop through a list and print each item",
            "keywords": ["har_ek", "chilla_we"]
        }
    ],
    "strings": [
        {
            "prompt": "Convert a string to uppercase",
            "keywords": ["vada_likha"]
        },
        {
            "prompt": "Split a string by comma",
            "keywords": ["vand_karo"]
        },
        {
            "prompt": "Concatenate two strings",
            "keywords": ["+"]
        }
    ],
    "collections": [
        {
            "prompt": "Create a list with numbers 1 to 5 and print it",
            "keywords": ["[",  "]", "chilla_we"]
        },
        {
            "prompt": "Sort a list in ascending order",
            "keywords": ["chal_sort_hoja"]
        },
        {
            "prompt": "Create a dictionary with person details",
            "keywords": ["{", ":", "}", "\""]
        }
    ],
    "error_handling": [
        {
            "prompt": "Try to divide by zero and catch the error",
            "keywords": ["chal_koshish_karle", "pakad", "/"]
        },
        {
            "prompt": "Handle file read errors gracefully",
            "keywords": ["chal_koshish_karle", "pakad", "padh"]
        }
    ]
}

# ============================================================================
# VALIDATION
# ============================================================================

class CodeValidator:
    """Validate generated Jatti code."""
    
    @staticmethod
    def check_syntax(code: str) -> Tuple[bool, List[str]]:
        """Check if code has valid Jatti structure."""
        errors = []
        
        if not code.strip().startswith("sun_we"):
            errors.append("Code must start with 'sun_we'")
        
        if not code.strip().endswith("ja_we"):
            errors.append("Code must end with 'ja_we'")
        
        sun_count = code.count("sun_we")
        ja_count = code.count("ja_we")
        if sun_count != ja_count:
            errors.append(f"Unbalanced sun_we ({sun_count}) and ja_we ({ja_count})")
        
        # Check indentation (basic)
        lines = code.split('\n')
        for i, line in enumerate(lines[1:-1], start=1):
            if line.strip() and not line.startswith("    "):
                if not line.strip().startswith("fuddu_chiz"):
                    errors.append(f"Line {i}: Not properly indented")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def check_keywords(code: str, required_keywords: List[str]) -> Tuple[float, List[str]]:
        """Check if code contains expected keywords."""
        found = []
        for keyword in required_keywords:
            if keyword in code:
                found.append(keyword)
        
        score = len(found) / len(required_keywords) if required_keywords else 0
        missing = [kw for kw in required_keywords if kw not in code]
        
        return score, missing
    
    @staticmethod
    def check_complexity(code: str) -> float:
        """Estimate code complexity (lines, branches, functions)."""
        lines = len([l for l in code.split('\n') if l.strip()])
        branches = code.count("je") + code.count("nahin_taan_je") + code.count("nahin_taan")
        functions = code.count("kaam")
        loops = code.count("har_ek") + code.count("jadon_tak")
        
        complexity = (lines / 5) + (branches * 0.5) + (functions * 2) + (loops * 1.5)
        return min(10.0, complexity)

# ============================================================================
# TESTING
# ============================================================================

class ModelTester:
    """Test code generation models."""
    
    def __init__(self, model_type: str = "openai", model_path: str = None):
        self.model_type = model_type
        self.model_path = model_path
        self.results = []
    
    def generate_code(self, prompt: str) -> str:
        """Generate code using the model."""
        if self.model_type == "openai":
            return self._generate_openai(prompt)
        elif self.model_type == "huggingface":
            return self._generate_huggingface(prompt)
        elif self.model_type == "mock":
            return self._generate_mock(prompt)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def _generate_openai(self, prompt: str) -> str:
        """Generate using OpenAI API."""
        try:
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Generate Jatti code for: {prompt}"
                }]
            )
            return response.choices[0].message["content"]
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return ""
    
    def _generate_huggingface(self, prompt: str) -> str:
        """Generate using local Hugging Face model."""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                device_map="auto",
                torch_dtype=torch.float16
            )
            
            inputs = tokenizer.encode(
                f"Generate Jatti code for: {prompt}",
                return_tensors="pt"
            )
            
            outputs = model.generate(
                inputs,
                max_new_tokens=500,
                temperature=0.3,
                top_p=0.95
            )
            
            return tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            logger.error(f"Hugging Face error: {e}")
            return ""
    
    def _generate_mock(self, prompt: str) -> str:
        """Generate mock code for testing."""
        return 'sun_we\n    chilla_we "Generated code"\nja_we'
    
    def test_category(self, category: str) -> Dict:
        """Test all prompts in a category."""
        prompts = TEST_PROMPTS.get(category, [])
        results = {
            "category": category,
            "total": len(prompts),
            "passed": 0,
            "syntax_valid": 0,
            "keyword_match": 0.0,
            "avg_complexity": 0.0,
            "tests": []
        }
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing: {category.upper()}")
        logger.info(f"{'='*60}")
        
        for i, test in enumerate(prompts, 1):
            logger.info(f"\n[{i}/{len(prompts)}] {test['prompt'][:50]}...")
            
            code = self.generate_code(test["prompt"])
            if not code:
                logger.warning("  ⚠️  No code generated")
                continue
            
            # Validate
            syntax_valid, syntax_errors = CodeValidator.check_syntax(code)
            keyword_score, missing_keywords = CodeValidator.check_keywords(
                code, test["keywords"]
            )
            complexity = CodeValidator.check_complexity(code)
            
            # Determine pass/fail
            passed = syntax_valid and keyword_score > 0.5
            
            results["syntax_valid"] += syntax_valid
            results["keyword_match"] += keyword_score
            results["avg_complexity"] += complexity
            results["passed"] += passed
            
            results["tests"].append({
                "prompt": test["prompt"],
                "syntax_valid": syntax_valid,
                "keyword_score": keyword_score,
                "complexity": complexity,
                "passed": passed,
                "code": code[:200],
                "errors": syntax_errors
            })
            
            # Log result
            status = "✅ PASS" if passed else "❌ FAIL"
            logger.info(f"  {status} | Syntax: {syntax_valid} | Keywords: {keyword_score:.2f} | Complexity: {complexity:.1f}")
            
            if syntax_errors:
                for err in syntax_errors:
                    logger.info(f"    Error: {err}")
        
        # Calculate averages
        results["keyword_match"] /= len(prompts)
        results["avg_complexity"] /= len(prompts)
        results["pass_rate"] = results["passed"] / len(prompts) if len(prompts) > 0 else 0
        results["syntax_rate"] = results["syntax_valid"] / len(prompts) if len(prompts) > 0 else 0
        
        return results
    
    def test_all(self) -> Dict:
        """Test all categories."""
        all_results = {
            "model_type": self.model_type,
            "model_path": str(self.model_path),
            "categories": [],
            "overall_pass_rate": 0.0,
            "overall_syntax_rate": 0.0
        }
        
        for category in TEST_PROMPTS.keys():
            result = self.test_category(category)
            all_results["categories"].append(result)
        
        # Calculate overall stats
        total_passed = sum(r["passed"] for r in all_results["categories"])
        total_tests = sum(r["total"] for r in all_results["categories"])
        all_results["overall_pass_rate"] = total_passed / total_tests if total_tests > 0 else 0
        
        total_syntax = sum(r["syntax_valid"] for r in all_results["categories"])
        all_results["overall_syntax_rate"] = total_syntax / total_tests if total_tests > 0 else 0
        
        return all_results
    
    def report(self, results: Dict):
        """Generate test report."""
        logger.info(f"\n{'='*60}")
        logger.info("TEST REPORT")
        logger.info(f"{'='*60}")
        
        logger.info(f"Model: {results['model_type']}")
        logger.info(f"Path: {results['model_path']}")
        
        logger.info(f"\n📊 Overall Results:")
        logger.info(f"  Pass Rate: {results['overall_pass_rate']:.1%}")
        logger.info(f"  Syntax Valid: {results['overall_syntax_rate']:.1%}")
        
        logger.info(f"\n📈 Category Breakdown:")
        for cat_result in results["categories"]:
            logger.info(f"\n  {cat_result['category'].upper()}")
            logger.info(f"    Total Tests: {cat_result['total']}")
            logger.info(f"    Passed: {cat_result['passed']}/{cat_result['total']} ({cat_result['pass_rate']:.1%})")
            logger.info(f"    Syntax Valid: {cat_result['syntax_valid']}/{cat_result['total']} ({cat_result['syntax_rate']:.1%})")
            logger.info(f"    Keyword Match: {cat_result['keyword_match']:.2f}")
            logger.info(f"    Avg Complexity: {cat_result['avg_complexity']:.1f}")
        
        # Save report
        report_file = "jatti_model_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"\n✅ Report saved to {report_file}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Test Jatti LLM models")
    parser.add_argument("--model-type", default="mock", choices=["openai", "huggingface", "mock"],
                       help="Type of model to test")
    parser.add_argument("--model-path", help="Path to fine-tuned model (for huggingface)")
    parser.add_argument("--category", help="Test specific category (or test all)")
    parser.add_argument("--prompt", help="Test single prompt")
    
    args = parser.parse_args()
    
    tester = ModelTester(args.model_type, args.model_path)
    
    # Single prompt test
    if args.prompt:
        logger.info(f"Testing prompt: {args.prompt}")
        code = tester.generate_code(args.prompt)
        logger.info(f"Generated code:\n{code}")
        
        syntax_valid, errors = CodeValidator.check_syntax(code)
        logger.info(f"Syntax valid: {syntax_valid}")
        if errors:
            for err in errors:
                logger.info(f"  Error: {err}")
    
    # Category test
    elif args.category:
        result = tester.test_category(args.category)
        tester.report({"model_type": args.model_type, "model_path": str(args.model_path), 
                      "categories": [result], "overall_pass_rate": result["pass_rate"],
                      "overall_syntax_rate": result["syntax_rate"]})
    
    # Full test suite
    else:
        results = tester.test_all()
        tester.report(results)

if __name__ == "__main__":
    main()
