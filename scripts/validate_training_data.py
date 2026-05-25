#!/usr/bin/env python3
"""
Jatti Training Data Validator and Corrector
Validates training data against actual Jatti compiler keywords
"""

import json
import re
from pathlib import Path

# Correct Jatti Keywords (from compiler.c source)
CORRECT_KEYWORDS = {
    "sun_we": "program start",
    "ja_we": "program end",
    "chilla_we": "print/output",
    "chal_oye": "variable declaration",
    "ban": "assignment operator (is/equals)",
    "kaam": "function definition",
    "wapas_kar": "return statement",
    "je": "if",
    "nahin_taan_je": "else if",
    "nahin_taan": "else",
    "har_ek": "for loop",
    "jadon_tak": "while loop",
    "range_banao": "range function",
    "roko_oye_roko": "break",
    "chalo_oye_chalo": "continue",
    "fuddu_chiz": "comment",
}

# WRONG keywords that might appear in training data
WRONG_KEYWORDS = {
    "likho": "WRONG - should be 'chilla_we'",
    "function": "WRONG - should be 'kaam'",
    "return": "WRONG - should be 'wapas_kar'",
    "if": "WRONG - should be 'je'",
    "else": "WRONG - should be 'nahin_taan'",
    "for": "WRONG - should be 'har_ek'",
    "while": "WRONG - should be 'jadon_tak'",
    "let": "WRONG - should be 'chal_oye'",
    "const": "WRONG - should be 'chal_oye'",
    "break": "WRONG - should be 'roko_oye_roko'",
    "continue": "WRONG - should be 'chalo_oye_chalo'",
    "range": "WRONG - should be 'range_banao'",
}

def validate_code(code):
    """Validate a Jatti code snippet."""
    errors = []
    warnings = []
    
    # Check for sun_we and ja_we
    if "sun_we" not in code:
        errors.append("Missing 'sun_we' at start")
    if "ja_we" not in code:
        errors.append("Missing 'ja_we' at end")
    
    # Check for wrong keywords
    for wrong_kw, hint in WRONG_KEYWORDS.items():
        if re.search(r'\b' + wrong_kw + r'\b', code):
            errors.append(f"Found '{wrong_kw}': {hint}")
    
    # Check structure
    if "sun_we" in code and "ja_we" in code:
        start_idx = code.index("sun_we")
        end_idx = code.index("ja_we")
        if start_idx >= end_idx:
            errors.append("'ja_we' must come after 'sun_we'")
    
    return errors, warnings

def correct_code(code):
    """Auto-correct common mistakes in Jatti code."""
    corrected = code
    
    # Fix common keyword mistakes
    corrections = {
        r'\blikho\(': 'chilla_we ',
        r'\bfunction\s+': 'kaam ',
        r'\breturn\s+': 'wapas_kar ',
        r'\bif\s+': 'je ',
        r'\belse\s+if\s+': 'nahin_taan_je ',
        r'\belse\s*\n': 'nahin_taan\n',
        r'\bfor\s+': 'har_ek ',
        r'\bwhile\s+': 'jadon_tak ',
        r'\blet\s+': 'chal_oye ',
        r'\bconst\s+': 'chal_oye ',
        r'\bbreak\s*\n': 'roko_oye_roko\n',
        r'\bcontinue\s*\n': 'chalo_oye_chalo\n',
        r'\brange\(': 'range_banao(',
    }
    
    for pattern, replacement in corrections.items():
        corrected = re.sub(pattern, replacement, corrected)
    
    # Fix print syntax: chilla_we "text" instead of chilla_we("text")
    corrected = re.sub(r'chilla_we\s*\(\s*', 'chilla_we ', corrected)
    corrected = re.sub(r'chilla_we\s+(["\'].*?["\'])\s*\)', r'chilla_we \1', corrected)
    
    # Fix function call syntax - remove parentheses from definition
    corrected = re.sub(r'kaam\s+(\w+)\s*\(\s*', r'kaam \1(', corrected)
    
    return corrected

def load_training_data(filepath):
    """Load training data from JSONL file."""
    examples = []
    with open(filepath) as f:
        for i, line in enumerate(f, 1):
            try:
                examples.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"❌ Line {i}: JSON decode error - {e}")
    return examples

def validate_training_data(filepath):
    """Validate all training examples."""
    print(f"\n📋 Validating: {filepath}\n")
    
    examples = load_training_data(filepath)
    stats = {
        "total": len(examples),
        "valid": 0,
        "invalid": 0,
        "errors": []
    }
    
    for i, example in enumerate(examples, 1):
        prompt = example.get("prompt", "")
        code = example.get("completion", "")
        
        errors, warnings = validate_code(code)
        
        if errors:
            stats["invalid"] += 1
            stats["errors"].append({
                "line": i,
                "prompt": prompt[:50],
                "errors": errors
            })
            print(f"❌ Example {i}: {prompt[:40]}...")
            for err in errors:
                print(f"   └─ {err}")
        else:
            stats["valid"] += 1
            print(f"✅ Example {i}: VALID")
    
    print(f"\n📊 Summary:")
    print(f"   Total: {stats['total']}")
    print(f"   ✅ Valid: {stats['valid']}")
    print(f"   ❌ Invalid: {stats['invalid']}")
    print(f"   Success Rate: {stats['valid']/stats['total']*100:.1f}%")
    
    return stats

def correct_training_data(input_file, output_file):
    """Correct and save training data."""
    print(f"\n🔧 Correcting: {input_file}\n")
    
    examples = load_training_data(input_file)
    corrected_count = 0
    
    corrected_examples = []
    for i, example in enumerate(examples, 1):
        original_code = example.get("completion", "")
        corrected_code = correct_code(original_code)
        
        if original_code != corrected_code:
            corrected_count += 1
            print(f"🔄 Example {i}: CORRECTED")
            example["completion"] = corrected_code
        
        corrected_examples.append(example)
    
    # Save corrected data
    with open(output_file, 'w') as f:
        for example in corrected_examples:
            f.write(json.dumps(example) + '\n')
    
    print(f"\n✅ Corrected {corrected_count} examples")
    print(f"📁 Saved to: {output_file}")
    
    return corrected_examples

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Jatti Training Data Validator\n")
        print("Usage:")
        print("  python validate_training_data.py <input_file> [--correct]")
        print("\nExamples:")
        print("  python validate_training_data.py training_data_examples.jsonl")
        print("  python validate_training_data.py training_data_examples.jsonl --correct")
        sys.exit(1)
    
    input_file = sys.argv[1]
    should_correct = "--correct" in sys.argv
    
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    # Validate
    stats = validate_training_data(input_file)
    
    # Correct if requested
    if should_correct and stats["invalid"] > 0:
        output_file = input_file.replace(".jsonl", "_corrected.jsonl")
        correct_training_data(input_file, output_file)
        print(f"\n✨ Now validating corrected data...")
        validate_training_data(output_file)
