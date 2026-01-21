# Jatti Language - VS Code Extension

Execute Jatti programming language files directly from VS Code with a single click!

## Features

✨ **Quick Execution**
- ▶️ **Run Button** - Click to execute instantly
- ⌨️ **Ctrl+Shift+J** - Keyboard shortcut for fast runs
- 🖥️ **Ctrl+Shift+T** - Run in integrated terminal
- 🖱️ **Right-click Menu** - Context menu support

🛠️ **Developer Tools**
- 🔨 **Build to Python** - Compile `.jatti` to `.py`
- 📝 **Format Code** - Auto-format your files
- 📊 **Live Output Panel** - See results instantly

## Requirements

- VS Code 1.80.0 or higher
- Python 3.6+
- **Jatti CLI files** in your workspace

## Installation

1. **Install Extension** in VS Code (search "Jatti Language")
2. **Download Jatti CLI** from: https://github.com/jatti-lang/jatti-lang
3. **Extract to your project folder**
4. **Done!** Start using `.jatti` files

## Quick Start

1. Create `hello.jatti`:
```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

2. Press **Ctrl+Shift+J** or click ▶️

3. See output in the **Jatti** panel!

## Commands

| Command | Shortcut | What it does |
|---------|----------|-------------|
| Run | Ctrl+Shift+J | Execute file |
| Run in Terminal | Ctrl+Shift+T | Open terminal & run |
| Build | - | Compile to Python |
| Format | - | Format code |

## How to Use

### Method 1: Click the Run Button
1. Open a `.jatti` file
2. Look for ▶️ button in top-right
3. Click it!

### Method 2: Keyboard Shortcut
- Press `Ctrl+Shift+J` to run instantly

### Method 3: Right-Click Menu
- Right-click on code
- Select "Run Jatti File"

### Method 4: Command Palette
- Press `Ctrl+Shift+P`
- Type "Jatti: Run"

## Output Panel

Results appear in the **Jatti** output panel at the bottom:

```
⏳ Running: hello.jatti
━━━━━━━━━━━━━━━━━━━━━━━━
Hello Jatti!
━━━━━━━━━━━━━━━━━━━━━━━━
✅ Execution completed!
```

## Examples

**Math:**
```jatti
sun_we
    chal_oye a ban 10
    chal_oye b ban 5
    chilla_we a + b
ja_we
```

**Loops:**
```jatti
sun_we
    har_ek i range_banao(1, 6)
        chilla_we i
ja_we
```

**Functions:**
```jatti
sun_we
    kaam add(x, y)
        wapas_kar x + y
    
    chal_oye result ban add(3, 4)
    chilla_we result
ja_we
```

## Troubleshooting

**No buttons showing?**
- Ensure file ends in `.jatti`
- Reload VS Code: `Ctrl+Shift+P` → "Reload Window"

**Python not found?**
- Install Python and add to PATH
- Restart VS Code

**Still not working?**
- Check that `cli.py` exists in workspace
- Verify Python version: `python --version`

## License

MIT License - Feel free to use and modify!

## Support

For issues and feedback, visit the project repository.

---

**Happy Coding with Jatti! 🎉**
