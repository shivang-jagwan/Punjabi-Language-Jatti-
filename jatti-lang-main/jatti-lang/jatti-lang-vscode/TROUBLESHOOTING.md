# 🔧 Jatti Language Extension Troubleshooting Guide

## ❌ Issue: No Syntax Highlighting

### Solution 1: Reload VS Code
- Press `Ctrl+Shift+P` → Type "Reload Window" → Press Enter
- If you just installed the extension, reload is required!

### Solution 2: Verify Extension is Installed
- Open Extensions (`Ctrl+Shift+X`)
- Search: "Jatti Language"
- Ensure it shows as "Installed" with a green checkmark
- If not, click "Install"

### Solution 3: Verify File Extension
- Make sure your file ends with `.jatti` (not `.jati` or `.txt`)
- Example: `hello.jatti` ✅, `hello.jati` ❌

### Solution 4: Check Extension Output
- Open Output panel (`Ctrl+Shift+U`)
- Select "Jatti" from dropdown
- Look for error messages
- If you see "Extension activated!" - it's working

---

## ❌ Issue: No File Icons

### Solution: Enable Icon Theme
Icons are installed but not enabled by default:

1. Press `Ctrl+,` to open Settings
2. Search: **"icon theme"**
3. Look for: **Workbench › Icon Theme**
4. Click dropdown and select: **"Jatti File Icons"**
5. Done! `.jatti` files now show custom icons ✨

**Note:** You must manually select the icon theme - it doesn't auto-activate.

---

## ❌ Issue: Run Button Not Working

### Error Message: "cli.py not found"

**Cause:** The run commands need `cli.py` from the full Jatti language package.

**Solution:**
The extension only provides syntax highlighting. To use the run button, you need the **complete Jatti language package**:

1. **Download/Clone the full repository:**
   ```bash
   git clone https://github.com/s-angad/jatti-lang.git
   cd jatti-lang
   ```

2. **Create your `.jatti` file in this directory:**
   ```bash
   # This folder must contain:
   # - cli.py (included in repo)
   # - compiler/ (included in repo)
   # - Your .jatti files
   ```

3. **Now the run button will work!**

### What the Run Commands Do:
- **Run** (`Ctrl+Shift+J`) - Execute your code and see output
- **Run in Terminal** (`Ctrl+Shift+T`) - Execute in terminal window
- **Build** - Convert Jatti code to Python
- **Format** - Format your Jatti code

---

## ❌ Issue: Commands Don't Appear in Command Palette

### Solution: Check Activation

1. Open a `.jatti` file in the editor
2. Press `Ctrl+Shift+P` to open Command Palette
3. Type "Jatti" - commands should appear
4. Commands only appear when a `.jatti` file is open

If commands don't appear:
- Reload VS Code (`Ctrl+Shift+P` → "Reload Window")
- Verify extension is installed (Extensions panel)

---

## ❌ Issue: Extension Won't Install

### Possible Causes:

**1. VS Code Too Old**
- Requirement: VS Code 1.80.0 or newer
- Check: Help → About → Find version number
- If older: Download latest from https://code.visualstudio.com/

**2. Extension Corrupted**
- Uninstall: Extensions panel → Uninstall
- Restart VS Code
- Reinstall from marketplace

**3. Connection Issue**
- Check internet connection
- Try again in a few minutes
- Check https://marketplace.visualstudio.com/

---

## ❌ Issue: Extension Disabled by VS Code

### Solution:

Sometimes VS Code automatically disables extensions if they have errors:

1. Open Extensions (`Ctrl+Shift+X`)
2. Look for "Jatti Language" in "Disabled" section
3. Click the arrow next to it → Select "Enable"
4. Click "Enable Locally" if prompted
5. Reload VS Code

---

## ✅ How to Verify Everything is Working

### Checklist:

1. **Extension Installed:**
   ```
   Extensions panel → Search "Jatti" → Shows installed ✅
   ```

2. **Syntax Highlighting:**
   ```
   Create file: test.jatti
   Add code: chilla_we "hello"
   Keywords should be colored ✅
   ```

3. **Icon Theme (Optional):**
   ```
   Settings → Icon Theme → "Jatti File Icons"
   File shows custom icon ✅
   ```

4. **Output Panel:**
   ```
   Ctrl+Shift+U → Select "Jatti" dropdown
   Should show: "Jatti Language Extension v0.1.0 initialized" ✅
   ```

5. **Command Palette:**
   ```
   Open .jatti file
   Ctrl+Shift+P → Type "Jatti"
   Should see 4 commands:
   - Jatti: Run
   - Jatti: Run in Terminal
   - Jatti: Build to Python
   - Jatti: Format File ✅
   ```

---

## 🚀 Getting Full Functionality

**The extension provides:**
- ✅ Syntax highlighting (all `.jatti` files)
- ✅ File icons (after selecting theme)
- ✅ Command palette integration

**For run/build/format commands, you need:**
- 📥 Download: https://github.com/s-angad/jatti-lang
- 📁 Keep `.jatti` files in same folder as `cli.py`
- ▶️ Now run button will work!

---

## 🆘 Still Having Issues?

### Where to Get Help:

1. **GitHub Issues:** https://github.com/s-angad/jatti-lang/issues
2. **Check README:** https://github.com/s-angad/jatti-lang/blob/main/README.md
3. **Verify Installation:** https://github.com/s-angad/jatti-lang#installation

### Information to Include:

If you report an issue, include:
- VS Code version (`Help` → `About`)
- Extension version (Extensions panel)
- Error message (from Output → Jatti)
- Your `.jatti` file (first few lines)
- Your operating system

---

## 📋 Quick Checklist for Fresh Install

- [ ] VS Code 1.80.0 or newer
- [ ] Install "Jatti Language" from Extensions
- [ ] Reload VS Code (`Ctrl+Shift+P` → "Reload Window")
- [ ] Open/create a `.jatti` file
- [ ] Verify syntax highlighting works (keywords colored)
- [ ] (Optional) Set icon theme: Settings → Workbench › Icon Theme → "Jatti File Icons"
- [ ] (If using run button) Download full package: https://github.com/s-angad/jatti-lang

---

**Version:** 0.1.0  
**Last Updated:** January 18, 2026
