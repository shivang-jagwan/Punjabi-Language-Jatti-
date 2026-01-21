# Local Setup (Windows)

This repo contains:
- The Jatti interpreter + CLI (`cli.py`)
- A 2‑pane web playground (`playground_server.py`)
- A VS Code extension (folder `jatti-lang-vscode/`)

## Requirements

- Windows 10/11
- Python 3.10+ recommended (3.8+ usually works)
- Git (optional, but recommended)

## 1) Get the code

```powershell
git clone https://github.com/shivang-jagwan/Punjabi-Language-Jatti-.git
cd Punjabi-Language-Jatti-
```

If you already have the folder, just `cd` into it.

## 2) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

## 3) Run a Jatti file (CLI)

Create `hello.jatti`:

```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

Run:

```powershell
python cli.py run hello.jatti
```

## 4) Build Jatti → Python

```powershell
python cli.py build hello.jatti --out hello.py
python hello.py
```

## 5) Run the web playground (no CLI commands needed)

```powershell
python playground_server.py
```

Open:
- http://127.0.0.1:8000/

## 6) Run regression tests

```powershell
python tests/run_regressions.py
python tests/run_regressions.py --build
```

## Troubleshooting

- PowerShell blocks activation:
  - Run PowerShell as Admin once: `Set-ExecutionPolicy RemoteSigned`
- Port 8000 already used:
  - `python playground_server.py --port 9000`
