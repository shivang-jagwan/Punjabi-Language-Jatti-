"""
Jatti LLM Data Augmentation Utilities
Generate variations and synthetic examples to expand training dataset
"""

import json
import random
import re
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import itertools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JattiDataAugmentor:
    """Generate augmented training data for Jatti models."""
    
    # Substitution templates
    VARIABLE_NAMES = [
        "x", "y", "z", "n", "count", "sum", "total", "result", "value",
        "item", "element", "data", "input", "output", "temp", "i", "j", "k",
        "name", "age", "city", "person", "user", "student", "number", "text"
    ]
    
    FUNCTION_NAMES = [
        "calculate", "process", "compute", "handle", "check", "validate",
        "transform", "convert", "extract", "filter", "map", "reduce",
        "add_values", "multiply_values", "is_valid", "get_sum"
    ]
    
    LIST_NAMES = [
        "items", "values", "numbers", "strings", "data", "results", "elements",
        "collection", "list", "array", "sequence", "records", "entries"
    ]
    
    STRING_PATTERNS = [
        "Hello {}", "Welcome {}", "The value is {}", "Result: {}",
        "Processing: {}", "Success: {}", "Error: {}", "Data: {}",
        "{} items found", "Your {} is ready", "Total {}"
    ]
    
    MATHEMATICAL_OPERATIONS = [
        ("+", "addition"),
        ("-", "subtraction"),
        ("*", "multiplication"),
        ("/", "division"),
        ("%", "modulo"),
        ("**", "power")
    ]
    
    LOOP_TYPES = [
        "for i in range($min, $max)",
        "for item in items",
        "for element in list",
        "while count < $limit",
        "while i > 0"
    ]
    
    CONDITIONAL_PATTERNS = [
        "if (x > $threshold)",
        "if (value == $target)",
        "if (name != \"\")",
        "if (count >= $minimum)",
        "if (age < $age_limit)"
    ]
    
    def __init__(self):
        """Initialize augmentor."""
        self.augmented_count = 0
    
    def augment_examples(self, examples: List[Dict], augmentation_factor: int = 3) -> List[Dict]:
        """
        Augment training examples with multiple variations.
        
        Args:
            examples: Original training examples
            augmentation_factor: How many variations to create per example
        
        Returns:
            Original + augmented examples
        """
        augmented = examples.copy()
        
        for example in examples:
            for _ in range(augmentation_factor):
                new_example = self._create_variation(example)
                if new_example:
                    augmented.append(new_example)
                    self.augmented_count += 1
        
        logger.info(f"✅ Generated {self.augmented_count} augmented examples from {len(examples)} originals")
        return augmented
    
    def _create_variation(self, example: Dict) -> Optional[Dict]:
        """Create a random variation of an example."""
        variation_type = random.choice([
            "rename_variables",
            "paraphrase_prompt",
            "change_values",
            "add_comments",
            "restructure"
        ])
        
        try:
            if variation_type == "rename_variables":
                return self._rename_variables(example)
            elif variation_type == "paraphrase_prompt":
                return self._paraphrase_prompt(example)
            elif variation_type == "change_values":
                return self._change_values(example)
            elif variation_type == "add_comments":
                return self._add_comments(example)
            else:
                return self._restructure_code(example)
        except Exception as e:
            logger.debug(f"Failed variation: {e}")
            return None
    
    def _rename_variables(self, example: Dict) -> Dict:
        """Create variation by renaming variables."""
        new_example = example.copy()
        code = new_example.get("completion", "")
        
        # Extract variable names used in code
        var_pattern = r'\b([a-z_][a-z0-9_]*)\b'
        used_vars = list(set(re.findall(var_pattern, code.lower())))
        
        # Create mapping to new names
        mapping = {}
        for var in used_vars[:5]:  # Limit to 5 variables
            if var not in ["sun_we", "ja_we", "function", "return", "if", "else", "for", "while"]:
                mapping[var] = random.choice(self.VARIABLE_NAMES)
        
        # Apply mapping
        for old_name, new_name in mapping.items():
            code = re.sub(rf'\b{old_name}\b', new_name, code)
        
        new_example["completion"] = code
        new_example["_augmentation"] = "rename_variables"
        return new_example
    
    def _paraphrase_prompt(self, example: Dict) -> Dict:
        """Create variation by rephrasing the prompt."""
        new_example = example.copy()
        prompt = new_example.get("prompt", "")
        
        paraphrases = {
            "Write": "Create",
            "program": "application",
            "prints": "outputs",
            "that": "which",
            "calculate": "compute",
            "check": "verify",
            "find": "search for",
            "using": "with",
            "a ": "the "
        }
        
        new_prompt = prompt
        for old, new in paraphrases.items():
            new_prompt = new_prompt.replace(old, new)
        
        if new_prompt != prompt:
            new_example["prompt"] = new_prompt
            new_example["_augmentation"] = "paraphrase"
            return new_example
        
        return None
    
    def _change_values(self, example: Dict) -> Dict:
        """Create variation by changing numeric/string values."""
        new_example = example.copy()
        code = new_example.get("completion", "")
        
        # Change numbers
        numbers = re.findall(r'\b(\d+)\b', code)
        if numbers:
            old_num = random.choice(numbers)
            new_num = str(random.randint(1, 100))
            code = code.replace(old_num, new_num, 1)
        
        # Change strings in quotes
        strings = re.findall(r'"([^"]*)"', code)
        if strings:
            old_str = random.choice(strings)
            new_str = random.choice(["data", "value", "text", "result", "output"])
            code = code.replace(f'"{old_str}"', f'"{new_str}"', 1)
        
        new_example["completion"] = code
        new_example["_augmentation"] = "value_change"
        return new_example
    
    def _add_comments(self, example: Dict) -> Dict:
        """Create variation by adding comments."""
        new_example = example.copy()
        code = new_example.get("completion", "")
        
        # Simple comment insertion
        lines = code.split('\n')
        if len(lines) > 1:
            insert_idx = random.randint(1, len(lines) - 1)
            comment = f"  # Processing step {insert_idx}"
            lines.insert(insert_idx, comment)
            code = '\n'.join(lines)
            new_example["completion"] = code
            new_example["_augmentation"] = "add_comments"
            return new_example
        
        return None
    
    def _restructure_code(self, example: Dict) -> Dict:
        """Create variation by restructuring while maintaining functionality."""
        new_example = example.copy()
        code = new_example.get("completion", "")
        
        # Add indentation variation (if needed)
        # Change loop style if applicable
        variations = [
            lambda x: x.replace(" = ", " ="),  # Remove space
            lambda x: x.replace("  ", "\t"),   # Tabs instead of spaces (when safe)
            lambda x: x.replace("{", "{\n  ") if "{" in x else x  # Format braces
        ]
        
        try:
            transform = random.choice(variations)
            new_code = transform(code)
            if new_code != code:
                new_example["completion"] = new_code
                new_example["_augmentation"] = "restructure"
                return new_example
        except:
            pass
        
        return None
    
    def generate_synthetic_examples(self, count: int = 50) -> List[Dict]:
        """
        Generate synthetic training examples.
        
        Args:
            count: Number of examples to generate
        
        Returns:
            List of synthetic examples
        """
        examples = []
        templates = self._get_code_templates()
        
        for i in range(count):
            template = random.choice(templates)
            example = self._instantiate_template(template)
            examples.append(example)
        
        logger.info(f"✅ Generated {count} synthetic examples")
        return examples
    
    def _get_code_templates(self) -> List[Tuple[str, str]]:
        """Get code generation templates (prompt, code_template)."""
        return [
            # Basic I/O
            ("Print a message to console", 
             "sun_we\n  likho(\"{msg}\")\nja_we"),
            
            # Variables
            ("Define a variable and print it",
             "sun_we\n  {var} = {value}\n  likho({var})\nja_we"),
            
            # Arithmetic
            ("Calculate {op_name} of two numbers",
             "sun_we\n  result = {num1} {op} {num2}\n  likho(result)\nja_we"),
            
            # Loops
            ("Loop through and print numbers",
             "sun_we\n  for {var} in [1, 2, 3, 4, 5] {{\n    likho({var})\n  }}\nja_we"),
            
            # Functions
            ("Create a function that adds two values",
             "sun_we\n  function add({n1}, {n2}) {{\n    return {n1} + {n2}\n  }}\n  likho(add(5, 3))\nja_we"),
            
            # Conditionals
            ("Check if a number is greater than threshold",
             "sun_we\n  n = {num}\n  if (n > {threshold}) {{\n    likho(\"Greater\")\n  }}\nja_we"),
            
            # Lists
            ("Create a list and access an element",
             "sun_we\n  {list_name} = [1, 2, 3, 4, 5]\n  likho({list_name}[{idx}])\nja_we"),
            
            # String operations
            ("Convert string to uppercase",
             "sun_we\n  text = \"{text}\"\n  likho(text.uppercase())\nja_we"),
            
            # Power operation
            ("Calculate power using ** operator",
             "sun_we\n  result = {base} ** {exp}\n  likho(result)\nja_we"),
            
            # Nested structures
            ("Loop with conditional inside",
             "sun_we\n  for {var} in [1, 2, 3, 4, 5] {{\n    if ({var} > 2) {{\n      likho({var})\n    }}\n  }}\nja_we"),
        ]
    
    def _instantiate_template(self, template: Tuple[str, str]) -> Dict:
        """Fill in a template with random values."""
        prompt_template, code_template = template
        
        # Generate random values
        values = {
            "msg": random.choice(["Hello", "Welcome", "Success", "Complete"]),
            "var": random.choice(self.VARIABLE_NAMES),
            "value": random.randint(1, 100),
            "op_name": random.choice(["sum", "product", "difference", "quotient"]),
            "op": random.choice(["+", "-", "*", "/"]),
            "num1": random.randint(1, 50),
            "num2": random.randint(1, 50),
            "threshold": random.randint(1, 20),
            "num": random.randint(1, 50),
            "idx": random.randint(0, 4),
            "list_name": random.choice(self.LIST_NAMES),
            "text": random.choice(["Jatti", "Code", "Language", "Punjabi"]),
            "base": random.randint(2, 5),
            "exp": random.randint(2, 4),
            "n1": random.choice(self.VARIABLE_NAMES),
            "n2": random.choice(self.VARIABLE_NAMES),
        }
        
        # Format templates
        prompt = prompt_template.format(**values)
        code = code_template.format(**values)
        
        return {
            "prompt": prompt,
            "completion": code,
            "_synthetic": True
        }
    
    def apply_mixup(self, examples: List[Dict], mix_count: int = 10) -> List[Dict]:
        """
        Mix prompts and completions from different examples.
        
        Args:
            examples: Original examples
            mix_count: Number of mix combinations to create
        
        Returns:
            List with added mix variations
        """
        mixed = []
        
        for _ in range(mix_count):
            # Pick two random examples
            ex1 = random.choice(examples)
            ex2 = random.choice(examples)
            
            # Sometimes mix prompt+completion from same, sometimes cross
            if random.random() < 0.5:
                # Use prompt from one, completion from similar category
                mixed_example = {
                    "prompt": ex1.get("prompt"),
                    "completion": ex2.get("completion"),
                    "_augmentation": "mixup"
                }
            else:
                mixed_example = {
                    "prompt": ex2.get("prompt"),
                    "completion": ex1.get("completion"),
                    "_augmentation": "mixup"
                }
            
            mixed.append(mixed_example)
        
        logger.info(f"✅ Generated {mix_count} mixed examples")
        return mixed
    
    def apply_backtranslation(self, examples: List[Dict], model_fn=None) -> List[Dict]:
        """
        Apply back-translation: code -> explanation -> code.
        
        Args:
            examples: Original examples
            model_fn: Optional function to convert code to explanation
        
        Returns:
            List with added back-translation variations
        """
        backtranslated = []
        
        for example in examples:
            code = example.get("completion", "")
            
            # Simple rule-based explanation
            if model_fn:
                explanation = model_fn(code)
            else:
                explanation = self._simple_explain(code)
            
            # Regenerate prompt from explanation
            new_prompt = f"Write Jatti code that: {explanation}"
            
            backtranslated_example = {
                "prompt": new_prompt,
                "completion": code,
                "_augmentation": "backtranslation"
            }
            
            backtranslated.append(backtranslated_example)
        
        logger.info(f"✅ Generated {len(backtranslated)} back-translated examples")
        return backtranslated
    
    def _simple_explain(self, code: str) -> str:
        """Simple rule-based code explanation."""
        explanations = []
        
        if "likho(" in code:
            explanations.append("prints output")
        if "function" in code:
            explanations.append("defines a function")
        if "for" in code or "while" in code:
            explanations.append("uses a loop")
        if "if" in code:
            explanations.append("has conditional logic")
        if "**" in code:
            explanations.append("uses power operation")
        if ".uppercase()" in code or ".split(" in code:
            explanations.append("manipulates strings")
        
        return " and ".join(explanations) if explanations else "performs operations"
    
    def save_augmented_data(self, examples: List[Dict], output_file: str):
        """Save augmented examples to file."""
        with open(output_file, 'w') as f:
            for example in examples:
                # Remove augmentation metadata before saving
                clean_example = {k: v for k, v in example.items() 
                               if not k.startswith("_")}
                f.write(json.dumps(clean_example) + "\n")
        
        logger.info(f"✅ Saved {len(examples)} examples to {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Jatti Data Augmentation")
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--output", required=True, help="Output JSONL file")
    parser.add_argument("--factor", type=int, default=3, help="Augmentation factor")
    parser.add_argument("--synthetic", type=int, default=0, help="Number of synthetic examples")
    parser.add_argument("--mixup", type=int, default=0, help="Number of mix variations")
    parser.add_argument("--backtranslate", action="store_true", help="Apply back-translation")
    
    args = parser.parse_args()
    
    # Load original data
    examples = []
    with open(args.input) as f:
        for line in f:
            examples.append(json.loads(line))
    
    logger.info(f"Loaded {len(examples)} original examples")
    
    augmentor = JattiDataAugmentor()
    
    # Apply augmentations
    augmented = augmentor.augment_examples(examples, args.factor)
    
    if args.synthetic:
        augmented.extend(augmentor.generate_synthetic_examples(args.synthetic))
    
    if args.mixup:
        augmented.extend(augmentor.apply_mixup(examples, args.mixup))
    
    if args.backtranslate:
        augmented.extend(augmentor.apply_backtranslation(examples))
    
    augmentor.save_augmented_data(augmented, args.output)
    print(f"\n✅ Total examples: {len(augmented)}")
    print(f"   Original: {len(examples)}")
    print(f"   Augmented: {len(augmented) - len(examples)}")

if __name__ == "__main__":
    main()
