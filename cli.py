#!/usr/bin/env python3
"""
Jatti Language CLI - Command line interface for Jatti programs
Usage:
    jatti run <file.jatti> [--debug]      # Run a Jatti program
    jatti build <file.jatti> [-o output.py]  # Compile to Python
    jatti format <file.jatti> [-i]        # Format Jatti code
"""

from compiler.core import run, compile_to_python, format_code
from compiler.errors import roast_error, info
import compiler.state as state
import sys
import os

# Fix encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def print_usage():
    print("""
🚀 Jatti Language CLI
═════════════════════════════════════════════════════════

Usage:
  jatti run <file.jatti> [--debug]       Run a Jatti program
  jatti build <file.jatti> [-o output.py]   Compile to Python
  jatti format <file.jatti> [-i]         Format code in-place
  jatti --version                        Show version
  jatti --help                          Show this help

Examples:
  jatti run example.jatti
  jatti run example.jatti --debug
  jatti build example.jatti -o output.py
  jatti format example.jatti -i

═════════════════════════════════════════════════════════
""")


def cmd_run(args):
    """Run a Jatti program"""
    if not args:
        roast_error("Usage: jatti run <file.jatti> [--debug]", 1)
    
    filepath = args[0]
    debug_mode = "--debug" in args
    
    if not os.path.exists(filepath):
        roast_error(f"File not found: {filepath}", 1)
    
    if debug_mode:
        state.DEBUG_MODE = True
        print("🔍 Debug mode enabled")
        print("="*60)
    
    with open(filepath, encoding='utf-8') as f:
        code = f.read()
    
    run(code)
    
    if debug_mode:
        print("="*60)
        print(f"✅ Program executed successfully")
        if state.TRACE_EXECUTION:
            print(f"\n📊 Execution trace ({len(state.TRACE_EXECUTION)} steps):")
            for i, trace in enumerate(state.TRACE_EXECUTION[:15], 1):
                print(f"   {i}. {trace}")
            if len(state.TRACE_EXECUTION) > 15:
                print(f"   ... and {len(state.TRACE_EXECUTION)-15} more steps")


def cmd_build(args):
    """Compile Jatti to Python"""
    if not args:
        roast_error("Usage: jatti build <file.jatti> [-o output.py]", 1)
    
    filepath = args[0]
    
    if not os.path.exists(filepath):
        roast_error(f"File not found: {filepath}", 1)
    
    # Determine output filename
    output_file = None
    if "-o" in args:
        idx = args.index("-o")
        if idx + 1 < len(args):
            output_file = args[idx + 1]
        else:
            roast_error("Missing output filename after -o", 1)
    else:
        # Default: replace .jatti with .py
        output_file = filepath.replace(".jatti", ".py")
    
    with open(filepath, encoding='utf-8') as f:
        code = f.read()
    
    print(f"🔨 Compiling {filepath}...")
    python_code = compile_to_python(code)
    
    with open(output_file, 'w') as f:
        f.write(python_code)
    
    print(f"✅ Successfully compiled to {output_file}")
    print(f"📝 Lines: {len(python_code.splitlines())}")


def cmd_format(args):
    """Format Jatti code"""
    if not args:
        roast_error("Usage: jatti format <file.jatti> [-i]", 1)
    
    filepath = args[0]
    in_place = "-i" in args
    
    if not os.path.exists(filepath):
        roast_error(f"File not found: {filepath}", 1)
    
    with open(filepath, encoding='utf-8') as f:
        code = f.read()
    
    print(f"📐 Formatting {filepath}...")
    formatted_code = format_code(code)
    
    if in_place:
        with open(filepath, 'w') as f:
            f.write(formatted_code)
        print(f"✅ Formatted in-place: {filepath}")
    else:
        print("📋 Formatted code (use -i to save):")
        print("="*60)
        print(formatted_code)
        print("="*60)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command in ["--help", "-h", "help"]:
        print_usage()
    elif command == "--version":
        print("Jatti Language v0.4.0")
        print("Phase 4: Error Handling & Debugging")
    elif command == "run":
        cmd_run(args)
    elif command == "build":
        cmd_build(args)
    elif command == "format":
        cmd_format(args)
    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()

