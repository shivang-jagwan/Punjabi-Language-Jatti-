import random
import traceback
from typing import Optional, List

ROASTS = [
    "Galti ho gayi !! koi gall nahi.",
    "Dhyaan de, Jatti style rakhi !!",
    "Phir ohi mistake !!",
    "Tu compiler nu test kar reha !!",
    "Compiler thak gaya. Tu vi !!",
    "Tu coding chadd de !!",
    "Tere to nhi hona oye !!",
    "Eh ki likh ta tu?",
    "Dimag use kar le thoda.",
    "Jatti Lang mazak nahi hai.",
    "Syntax nu respect de.",
]

# Error context for better debugging
ERROR_CONTEXT = {
    'code_lines': [],  # All lines of the program
    'current_line': 1,
    'function_stack': [],  # Stack of function calls
}


def set_code_context(lines: List[str]):
    """Store the entire program for error context display"""
    ERROR_CONTEXT['code_lines'] = lines


def push_function(func_name: str, line_no: int):
    """Track function call stack for better error messages"""
    ERROR_CONTEXT['function_stack'].append({
        'name': func_name,
        'line': line_no
    })


def pop_function():
    """Remove function from stack"""
    if ERROR_CONTEXT['function_stack']:
        ERROR_CONTEXT['function_stack'].pop()


def get_error_context(line_no: Optional[int] = None) -> str:
    """Generate detailed error context with code snippet"""
    if line_no is None:
        line_no = ERROR_CONTEXT['current_line']
    
    context_lines = []
    lines = ERROR_CONTEXT['code_lines']
    
    if not lines or line_no < 1 or line_no > len(lines):
        return ""
    
    # Show context: 2 lines before, current line, 2 lines after
    start = max(0, line_no - 3)
    end = min(len(lines), line_no + 2)
    
    context_lines.append("📋 Code Context:")
    for i in range(start, end):
        prefix = ">>> " if (i + 1) == line_no else "    "
        line_text = lines[i] if i < len(lines) else ""
        line_num = i + 1
        context_lines.append(f"{prefix}{line_num:3d} | {line_text}")
    
    return "\n".join(context_lines)


def get_stack_trace() -> str:
    """Generate call stack trace for debugging"""
    if not ERROR_CONTEXT['function_stack']:
        return ""
    
    trace_lines = ["📞 Call Stack:"]
    for i, func_info in enumerate(ERROR_CONTEXT['function_stack']):
        indent = "  " * i
        trace_lines.append(f"{indent}└─ {func_info['name']}() at line {func_info['line']}")
    
    return "\n".join(trace_lines)


def roast_error(msg, line_no=None):
    """Enhanced error reporting with context and debugging info"""
    print("\n" + "="*60)
    print("❌ JATTI ERROR")
    print("="*60)
    
    print(f"\n🔴 Error: {msg}")
    
    if line_no is not None:
        print(f"📍 Line {line_no}")
    
    # Show code context
    context = get_error_context(line_no)
    if context:
        print("\n" + context)
    
    # Show call stack if any
    stack = get_stack_trace()
    if stack:
        print("\n" + stack)
    
    # Show roast message
    print("\n" + "# " + random.choice(ROASTS))
    print("="*60 + "\n")
    
    raise SystemExit


def warning(msg, line_no=None):
    """Warnings that don't stop execution"""
    print(f"⚠️  Warning (Line {line_no}): {msg}") if line_no else print(f"⚠️  Warning: {msg}")


def info(msg):
    """Informational messages"""
    print(f"ℹ️  Info: {msg}")


def soft_error(msg, line_no=None, recovery_value=None):
    """Non-fatal error that returns a recovery value instead of exiting"""
    print(f"⚠️  Error (Line {line_no}): {msg}") if line_no else print(f"⚠️  Error: {msg}")
    if recovery_value is not None:
        print(f"   Recovering with value: {recovery_value}")
    return recovery_value


def get_warnings_summary() -> List[str]:
    """Get summary of all warnings during execution"""
    return ERROR_CONTEXT.get('warnings', [])


def clear_error_context():
    """Reset error tracking for new program"""
    ERROR_CONTEXT['code_lines'] = []
    ERROR_CONTEXT['current_line'] = 1
    ERROR_CONTEXT['function_stack'] = []
    ERROR_CONTEXT['warnings'] = []
