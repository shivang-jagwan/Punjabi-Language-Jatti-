#!/usr/bin/env python3
"""Minimal regression runner for Jatti.

Runs each test case in tests/cases/*.jatti via cli.py and compares stdout to
its matching tests/expected/<name>.txt file.

Optionally also validates the build pipeline by compiling each case to Python
and running the generated .py, comparing output to the same expected stdout.

Usage:
  python tests/run_regressions.py
  python tests/run_regressions.py --build
  python tests/run_regressions.py --case 05_foreach_range

Exit code:
  0 if all tests pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import difflib
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = REPO_ROOT / "tests" / "cases"
EXPECTED_DIR = REPO_ROOT / "tests" / "expected"
TMP_DIR = REPO_ROOT / "tests" / "tmp"

CLI_PY = REPO_ROOT / "cli.py"


def _run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def _normalize_output(s: str) -> str:
    # Normalize newlines and strip only trailing whitespace lines.
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return s


def _diff(expected: str, actual: str, name: str) -> str:
    expected_lines = expected.splitlines(keepends=True)
    actual_lines = actual.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            expected_lines,
            actual_lines,
            fromfile=f"expected/{name}",
            tofile=f"actual/{name}",
        )
    )


def _load_expected(case_stem: str) -> str:
    expected_path = EXPECTED_DIR / f"{case_stem}.txt"
    if not expected_path.exists():
        raise FileNotFoundError(f"Missing expected output file: {expected_path}")
    return expected_path.read_text(encoding="utf-8")


def _find_cases(selected: str | None) -> list[Path]:
    cases = sorted(CASES_DIR.glob("*.jatti"))
    if selected:
        selected = selected.strip()
        if selected.endswith(".jatti"):
            selected = selected[:-6]
        cases = [p for p in cases if p.stem == selected]
    return cases


def run_case_interpreter(case_path: Path) -> tuple[int, str]:
    cmd = [sys.executable, str(CLI_PY), "run", str(case_path)]
    proc = _run(cmd, cwd=REPO_ROOT)
    return proc.returncode, _normalize_output(proc.stdout)


def run_case_build(case_path: Path) -> tuple[int, str]:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    out_py = TMP_DIR / f"{case_path.stem}.py"

    # Build
    cmd_build = [sys.executable, str(CLI_PY), "build", str(case_path), "-o", str(out_py)]
    proc_build = _run(cmd_build, cwd=REPO_ROOT)
    if proc_build.returncode != 0:
        return proc_build.returncode, _normalize_output(proc_build.stdout)

    # Run compiled output. Use repo root so imports like `from compiler...` resolve.
    cmd_run = [sys.executable, str(out_py)]
    proc_run = _run(cmd_run, cwd=REPO_ROOT)
    return proc_run.returncode, _normalize_output(proc_run.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true", help="Also test compile_to_python() output")
    parser.add_argument("--case", default=None, help="Run a single case by stem (e.g., 05_foreach_range)")
    args = parser.parse_args()

    if not CLI_PY.exists():
        print(f"ERROR: cli.py not found at {CLI_PY}")
        return 1

    cases = _find_cases(args.case)
    if not cases:
        print("No test cases found.")
        return 1

    # Clean tmp outputs for deterministic runs
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    failed = 0

    for case_path in cases:
        expected = _load_expected(case_path.stem)

        rc, out = run_case_interpreter(case_path)
        if rc != 0:
            failed += 1
            print(f"[FAIL] {case_path.name} (interpreter exit={rc})")
            print(out)
            continue

        if out != expected:
            failed += 1
            print(f"[FAIL] {case_path.name} (interpreter output mismatch)")
            print(_diff(expected, out, case_path.stem))
            continue

        if args.build:
            rc_b, out_b = run_case_build(case_path)
            if rc_b != 0:
                failed += 1
                print(f"[FAIL] {case_path.name} (build exit={rc_b})")
                print(out_b)
                continue

            if out_b != expected:
                failed += 1
                print(f"[FAIL] {case_path.name} (build output mismatch)")
                print(_diff(expected, out_b, case_path.stem))
                continue

        print(f"[PASS] {case_path.name}")

    if failed:
        print(f"\n{failed} failing case(s).")
        return 1

    print("\nAll regressions passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
