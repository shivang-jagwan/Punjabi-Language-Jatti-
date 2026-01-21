# Jatti Regression Tests

This folder contains a minimal regression suite for the Jatti interpreter and (optionally) its `build` output.

## Run

From repo root:

- Interpreter-only:
  - `python tests/run_regressions.py`

- Interpreter + build output:
  - `python tests/run_regressions.py --build`

- Single case:
  - `python tests/run_regressions.py --case 05_foreach_range`

## Structure

- `tests/cases/*.jatti` — input programs
- `tests/expected/*.txt` — expected stdout for each case
- `tests/tmp/` — scratch directory for build artifacts (auto-cleaned)

## Notes

- Error outputs are intentionally avoided in this suite because error roasts are randomized.
