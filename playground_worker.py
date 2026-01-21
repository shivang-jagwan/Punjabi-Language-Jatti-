#!/usr/bin/env python3
"""Worker process for Jatti Playground.

Reads Jatti code from stdin, runs it via compiler.core.run, and prints whatever
the interpreter prints to stdout.

This is intentionally tiny so the main server can enforce timeouts/output limits
by controlling this subprocess.
"""

from __future__ import annotations

import sys


def main() -> int:
    code = sys.stdin.read()
    try:
        from compiler.core import run as jatti_run
    except Exception as e:
        print(f"Failed to import Jatti compiler: {e}")
        return 2

    try:
        jatti_run(code)
        return 0
    except SystemExit:
        # roast_error raises SystemExit; error text is already printed.
        return 0
    except Exception as e:
        print(str(e))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
