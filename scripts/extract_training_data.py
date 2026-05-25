#!/usr/bin/env python3
"""
Jatti LLM Training Data Extractor
Collects code examples and creates training dataset for fine-tuning LLM.
Output: training_data.jsonl (OpenAI fine-tuning format)
"""

import json
import re
from pathlib import Path
from typing import List, Dict

class JattiDataExtractor:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.examples = []
        
    def extract_from_markdown(self, file_path: str, category: str) -> List[Dict]:
        """Extract code blocks and associated descriptions from markdown files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern: Markdown heading followed by optional description, then ```jatti code block
        pattern = r'###?\s+(.+?)\n+(.+?)\n*```jatti\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        extracted = []
        for title, description, code in matches:
            code = code.strip()
            if code and 'sun_we' in code:  # Valid Jatti program
                example = {
                    "prompt": f"{title.strip()}. {description.strip()[:100]}",
                    "code": code,
                    "category": category,
                    "title": title.strip()
                }
                extracted.append(example)
                print(f"✓ {category}: {title.strip()[:50]}")
        
        return extracted
    
    def collect_examples(self) -> List[Dict]:
        """Collect examples from all documentation files."""
        files_to_process = [
            ("BEGINNER_TUTORIAL.md", "basics"),
            ("INTERMEDIATE_GUIDE.md", "intermediate"),
            ("ADVANCED_TOPICS.md", "advanced"),
            ("LANGUAGE_SPECIFICATION.md", "reference"),
        ]
        
        for file_name, category in files_to_process:
            file_path = self.repo_path / file_name
            if file_path.exists():
                print(f"\n📖 Processing {file_name}...")
                examples = self.extract_from_markdown(str(file_path), category)
                self.examples.extend(examples)
        
        return self.examples
    
    def manual_examples(self) -> List[Dict]:
        """Add high-quality manual examples to supplement extracted data."""
        manual = [
            {
                "prompt": "Write a program that prints 'Hello World'",
                "code": 'sun_we\n    chilla_we "Hello World"\nja_we',
                "category": "basics",
                "title": "Hello World"
            },
            {
                "prompt": "Create a function that adds two numbers and returns the result",
                "code": 'sun_we\n    kaam add(a, b)\n        wapas_kar a + b\n    \n    chilla_we add(5, 3)\nja_we',
                "category": "functions",
                "title": "Add Function"
            },
            {
                "prompt": "Loop through numbers 1 to 10 and print each one",
                "code": 'sun_we\n    har_ek i range_banao(1, 11)\n        chilla_we i\nja_we',
                "category": "loops",
                "title": "For Loop Example"
            },
            {
                "prompt": "Convert text to uppercase and print it",
                "code": 'sun_we\n    chal_oye text ban "hello jatti"\n    chilla_we vada_likha(text)\nja_we',
                "category": "strings",
                "title": "String Uppercase"
            },
            {
                "prompt": "Create a list of numbers, sort it, and print the result",
                "code": 'sun_we\n    chal_oye nums ban [3, 1, 4, 1, 5, 9, 2]\n    chal_oye sorted ban chal_sort_hoja(nums)\n    chilla_we sorted\nja_we',
                "category": "collections",
                "title": "Sort List"
            },
            {
                "prompt": "Check if a variable is greater than 10 and print accordingly",
                "code": 'sun_we\n    chal_oye x ban 15\n    je x vadha_hai 10\n        chilla_we "x is greater than 10"\n    nahin_taan\n        chilla_we "x is not greater than 10"\nja_we',
                "category": "conditionals",
                "title": "If-Else Condition"
            },
            {
                "prompt": "Calculate factorial of 5 using recursion",
                "code": 'sun_we\n    kaam factorial(n)\n        je n barabar 1\n            wapas_kar 1\n        nahin_taan\n            wapas_kar n * factorial(n - 1)\n    \n    chilla_we factorial(5)\nja_we',
                "category": "recursion",
                "title": "Factorial Recursion"
            },
            {
                "prompt": "Create a dictionary with person details and print their name",
                "code": 'sun_we\n    chal_oye person ban {"naam": "Singh", "age": 25, "city": "Punjab"}\n    chilla_we person["naam"]\nja_we',
                "category": "collections",
                "title": "Dictionary Access"
            },
            {
                "prompt": "Read a file and print its contents",
                "code": 'sun_we\n    chal_oye content ban padh("file.txt")\n    chilla_we content\nja_we',
                "category": "file_io",
                "title": "Read File"
            },
            {
                "prompt": "Write text to a file using likh function",
                "code": 'sun_we\n    likh("output.txt", "Hello from Jatti!")\n    chilla_we "File written successfully"\nja_we',
                "category": "file_io",
                "title": "Write File"
            },
            {
                "prompt": "Try to divide by zero and catch the error gracefully",
                "code": 'sun_we\n    chal_koshish_karle\n        chal_oye result ban 10 / 0\n    pakad err\n        chilla_we "Error caught: Cannot divide by zero"\nja_we',
                "category": "error_handling",
                "title": "Try-Catch Block"
            },
            {
                "prompt": "Split a string by comma and print each word",
                "code": 'sun_we\n    chal_oye text ban "apple,banana,mango"\n    chal_oye fruits ban vand_karo(text, ",")\n    har_ek fruit fruits\n        chilla_we fruit\nja_we',
                "category": "strings",
                "title": "Split String"
            },
            {
                "prompt": "Calculate power of 2 raised to 8",
                "code": 'sun_we\n    chal_oye result ban 2 ** 8\n    chilla_we result\nja_we',
                "category": "math",
                "title": "Power Operator"
            },
        ]
        
        print(f"\n📝 Added {len(manual)} manual examples")
        return manual
    
    def create_training_data(self, output_file: str):
        """Create OpenAI fine-tuning format (JSONL with prompt/completion)."""
        examples = self.collect_examples()
        examples.extend(self.manual_examples())
        
        # Remove duplicates by code
        seen_codes = set()
        unique_examples = []
        for ex in examples:
            if ex["code"] not in seen_codes:
                unique_examples.append(ex)
                seen_codes.add(ex["code"])
        
        # Convert to OpenAI format
        with open(output_file, 'w', encoding='utf-8') as f:
            for example in unique_examples:
                # Format: user prompt, assistant code
                entry = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert Jatti programming assistant. Generate clean, idiomatic Jatti code."
                        },
                        {
                            "role": "user",
                            "content": example["prompt"]
                        },
                        {
                            "role": "assistant",
                            "content": example["code"]
                        }
                    ],
                    "metadata": {
                        "category": example["category"],
                        "title": example["title"]
                    }
                }
                f.write(json.dumps(entry) + '\n')
        
        print(f"\n✅ Training data saved to {output_file}")
        print(f"📊 Total examples: {len(unique_examples)}")
        print(f"📈 Categories: {len(set(ex['category'] for ex in unique_examples))}")
        
        # Print statistics
        categories = {}
        for ex in unique_examples:
            cat = ex["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📋 Category Breakdown:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {cat}: {count} examples")
        
        return unique_examples

if __name__ == "__main__":
    import sys
    
    repo_path = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else "training_data.jsonl"
    
    extractor = JattiDataExtractor(repo_path)
    extractor.create_training_data(output_file)
    
    print(f"\n🚀 Ready for fine-tuning!")
    print(f"Next step: Upload {output_file} to OpenAI API")
