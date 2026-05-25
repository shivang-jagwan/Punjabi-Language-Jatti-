#!/usr/bin/env python3
"""
Jatti LLM Inference Server
Backend service for Jatti code generation using fine-tuned LLM.
Supports both OpenAI API and local model inference.
"""

from flask import Flask, request, jsonify
import os
from typing import Dict, Optional
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, codellama, gpt-local
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
PORT = int(os.getenv("PORT", 5000))

# ============================================================================
# OPENAI INTEGRATION
# ============================================================================

def generate_with_openai(prompt: str, context: Optional[str] = None, max_tokens: int = 500) -> Dict:
    """Generate Jatti code using OpenAI API."""
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        
        system_prompt = """You are an expert Jatti programming language code generator.

Jatti Language Reference:
- Keywords: sun_we (start), ja_we (end), chilla_we (print), chal_oye (variable), ban (assign), kaam (function), wapas_kar (return)
- Loops: har_ek (for), jadon_tak (while), roko_oye_roko (break), chalo_oye_chalo (continue)
- Conditionals: je (if), nahin_taan_je (elif), nahin_taan (else)
- Data types: numbers, strings (quoted), lists [], dicts {}, sach (true), jhoot (false), khaali (null)
- String methods: vada_likha(), chhota_likha(), vand_karo(), badal_de(), dhundh_ja(), shuru_hunda(), khatam_hunda(), saf_karo()
- Built-in functions: kinna_lamba(), ganao(), sab_ton_vaddha(), sab_ton_chhota(), chal_sort_hoja(), chal_reverse_hoja(), range_banao(), kism(), likh(), padh()
- Error handling: chal_koshish_karle (try), pakad (catch)
- Operators: + - * / % ** (power), vadha_hai (>), nikka_hai (<), barabar (==), barabar_nahi_hai (!=), vadha_ya_barabar (>=), nikka_ya_barabar (<=), ate (and), ya_te (or), nahi (not)

IMPORTANT:
- All programs MUST start with 'sun_we' and end with 'ja_we'
- Use 4-space indentation
- Wrap code blocks in clean, idiomatic Jatti syntax
- Include comments with 'fuddu_chiz' where helpful
"""
        
        user_message = f"{prompt}"
        if context:
            user_message += f"\n\nContext/Requirements: {context}"
        
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=max_tokens,
            top_p=0.95
        )
        
        code = response.choices[0].message["content"]
        
        return {
            "success": True,
            "code": code,
            "model": MODEL_NAME,
            "tokens_used": response.usage.total_tokens,
            "provider": "openai"
        }
    
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "provider": "openai"
        }

# ============================================================================
# CODELLAMA LOCAL INTEGRATION
# ============================================================================

def generate_with_codellama(prompt: str, context: Optional[str] = None, max_tokens: int = 500) -> Dict:
    """Generate Jatti code using local CodeLlama model."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/CodeLlama-34b-hf")
        model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/CodeLlama-34b-hf",
            device_map="auto",
            torch_dtype=torch.float16
        )
        
        system_prompt = """You are an expert Jatti programming language code generator. Generate clean Jatti code."""
        
        user_message = f"Generate Jatti code for: {prompt}"
        if context:
            user_message += f"\n\nContext: {context}"
        
        full_prompt = f"[INST] {system_prompt}\n\n{user_message} [/INST]"
        
        inputs = tokenizer.encode(full_prompt, return_tensors="pt").to(device)
        
        outputs = model.generate(
            inputs,
            max_new_tokens=max_tokens,
            temperature=0.3,
            top_p=0.95,
            do_sample=True
        )
        
        code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return {
            "success": True,
            "code": code,
            "model": "CodeLlama-34b",
            "tokens_used": len(outputs[0]),
            "provider": "codellama"
        }
    
    except Exception as e:
        logger.error(f"CodeLlama error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "provider": "codellama"
        }

# ============================================================================
# HYBRID APPROACH (Fallback)
# ============================================================================

def generate_jatti_code(prompt: str, context: Optional[str] = None, max_tokens: int = 500) -> Dict:
    """Main entry point for code generation."""
    
    if LLM_PROVIDER == "openai":
        return generate_with_openai(prompt, context, max_tokens)
    elif LLM_PROVIDER == "codellama":
        return generate_with_codellama(prompt, context, max_tokens)
    else:
        return {"success": False, "error": "Unknown LLM provider"}

# ============================================================================
# FLASK ENDPOINTS
# ============================================================================

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "provider": LLM_PROVIDER,
        "model": MODEL_NAME
    })

@app.route("/api/generate", methods=["POST"])
def generate():
    """Generate Jatti code from English prompt."""
    try:
        data = request.json
        prompt = data.get("prompt")
        context = data.get("context")
        max_tokens = data.get("max_tokens", 500)
        
        if not prompt:
            return jsonify({"error": "Missing 'prompt' field"}), 400
        
        if not OpenAI_API_KEY and LLM_PROVIDER == "openai":
            return jsonify({"error": "OpenAI API key not configured"}), 500
        
        result = generate_jatti_code(prompt, context, max_tokens)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 500
    
    except Exception as e:
        logger.error(f"Error in /api/generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/validate", methods=["POST"])
def validate():
    """Validate generated Jatti code."""
    try:
        data = request.json
        code = data.get("code")
        
        if not code:
            return jsonify({"error": "Missing 'code' field"}), 400
        
        # Basic validation checks
        is_valid = True
        errors = []
        
        if not code.strip().startswith("sun_we"):
            is_valid = False
            errors.append("Code must start with 'sun_we'")
        
        if not code.strip().endswith("ja_we"):
            is_valid = False
            errors.append("Code must end with 'ja_we'")
        
        # Check for balanced sun_we/ja_we
        sun_count = code.count("sun_we")
        ja_count = code.count("ja_we")
        if sun_count != ja_count:
            is_valid = False
            errors.append(f"Unbalanced sun_we ({sun_count}) and ja_we ({ja_count})")
        
        return jsonify({
            "valid": is_valid,
            "errors": errors,
            "code_length": len(code),
            "lines": len(code.split('\n'))
        })
    
    except Exception as e:
        logger.error(f"Error in /api/validate: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/explain", methods=["POST"])
def explain():
    """Explain Jatti code in English."""
    try:
        data = request.json
        code = data.get("code")
        
        if not code:
            return jsonify({"error": "Missing 'code' field"}), 400
        
        # Use LLM to explain the code
        prompt = f"Explain this Jatti code in simple English:\n\n{code}"
        
        if LLM_PROVIDER == "openai":
            import openai
            openai.api_key = OPENAI_API_KEY
            
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            explanation = response.choices[0].message["content"]
            
            return jsonify({
                "success": True,
                "explanation": explanation,
                "model": MODEL_NAME
            })
        else:
            return jsonify({"error": "Explain feature only available with OpenAI"}), 501
    
    except Exception as e:
        logger.error(f"Error in /api/explain: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        logger.warning("⚠️  OpenAI API key not set. Set OPENAI_API_KEY environment variable.")
    
    logger.info(f"🚀 Jatti LLM Server starting on port {PORT}")
    logger.info(f"   Provider: {LLM_PROVIDER}")
    logger.info(f"   Model: {MODEL_NAME}")
    logger.info(f"   Health check: http://localhost:{PORT}/health")
    
    app.run(host="0.0.0.0", port=PORT, debug=True)
