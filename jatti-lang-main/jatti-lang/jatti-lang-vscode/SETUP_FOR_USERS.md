# 📖 Jatti Language Extension - Setup Guide for Users

## 🎯 What This Extension Does

When installed on another PC, the Jatti Language extension provides:

✅ **Syntax highlighting** for `.jatti` files  
✅ **Custom file icons** for `.jatti` files (must enable manually)  
✅ **Buttons/commands** to run, build, and format code  

---

## 📥 Installation Steps

### Step 1: Install Extension
1. Open **VS Code**
2. Press `Ctrl+Shift+X` (Extensions panel)
3. Search: **"Jatti Language"**
4. Click **Install**
5. Wait for installation to complete

### Step 2: Reload VS Code (IMPORTANT!)
1. Press `Ctrl+Shift+P` (Command Palette)
2. Type: **"Reload Window"**
3. Press Enter

**Why?** VS Code needs to reload to activate the extension!

---

## 🎨 Enable Custom File Icons (Optional)

To see the custom Jatti icon on `.jatti` files:

1. Press `Ctrl+,` (Settings)
2. Search: **"icon theme"**
3. Find: **Workbench › Icon Theme**
4. Click dropdown
5. Select: **"Jatti File Icons"**

✅ Now `.jatti` files will show the custom icon!

---

## ▶️ Using the Run Button

### Prerequisites:
You need the **complete Jatti language package** (not just the extension):

```bash
git clone https://github.com/s-angad/jatti-lang.git
cd jatti-lang
```

This folder contains:
- `cli.py` - The Jatti runtime
- `compiler/` - The compiler
- Your `.jatti` files should go here

### Using Run Commands:

Once you have the full package:

1. Open a `.jatti` file in VS Code
2. Look for these buttons in top-right:
   - ▶️ **Run** - Execute code (see output in panel)
   - 🖥️ **Run in Terminal** - Execute in terminal window
   - 🔨 **Build** - Convert to Python
   - 📝 **Format** - Format code

3. Or use keyboard shortcuts:
   - `Ctrl+Shift+J` - Run
   - `Ctrl+Shift+T` - Run in Terminal

### Example:

```jatti
chilla_we "Hello, World!"  // Print output
```

Click ▶️ button → See output in Jatti panel

---

## ⚠️ Common Issues

### No Syntax Highlighting?
- [ ] Reload VS Code (`Ctrl+Shift+P` → "Reload Window")
- [ ] File must end with `.jatti` (not `.txt` or `.jati`)
- [ ] Extension must be installed (check Extensions panel)

### No File Icons?
- Icons must be enabled manually
- Settings → Icon Theme → "Jatti File Icons"
- Icons only show after you select them

### Run Button Doesn't Work?
- You need the full Jatti package from GitHub
- `cli.py` must be in same folder as your `.jatti` files
- Example folder structure:
  ```
  jatti-lang/
    ├── cli.py
    ├── compiler/
    ├── hello.jatti    ← Put your files here
    └── test.jatti
  ```

### Extension Disabled?
- Open Extensions panel
- Look for "Disabled" section
- Click enable next to "Jatti Language"

---

## 📂 Project Structure

To use run commands properly, your folder should look like:

```
jatti-lang/
├── cli.py                    ← Required for run button
├── compiler/
│   ├── core.py
│   ├── runtime.py
│   ├── state.py
│   └── ...
├── hello.jatti               ← Your code file
├── example.jatti
└── [other files]
```

Create `.jatti` files in this directory, then the run button will work!

---

## ✅ Verification Checklist

After installation, verify:

- [ ] VS Code opened
- [ ] Extension installed (Extensions panel shows "Jatti Language" installed)
- [ ] VS Code reloaded
- [ ] Create `test.jatti` file with code:
  ```jatti
  chal_oye x ban 42
  chilla_we x
  ```
- [ ] Syntax should be colored (keywords in color)
- [ ] (Optional) Icon theme set to "Jatti File Icons"
- [ ] (If full package available) Test run button

---

## 🚀 First Program

1. Make sure you have the full Jatti package downloaded
2. Create file: `hello.jatti`
3. Add this code:
   ```jatti
   chilla_we "Welcome to Jatti! 🚀"
   ```
4. Click ▶️ button (or press `Ctrl+Shift+J`)
5. See output in Jatti panel at bottom

---

## 📚 Full Documentation

For complete Jatti language documentation:

- **Language Syntax:** https://github.com/s-angad/jatti-lang
- **Examples:** https://github.com/s-angad/jatti-lang/tree/main
- **Troubleshooting:** See `TROUBLESHOOTING.md` in extension

---

## ❓ Need Help?

### If syntax highlighting doesn't work:
1. Reload VS Code
2. Check file ends with `.jatti`
3. Check extension is installed

### If run button doesn't work:
1. Download full package: https://github.com/s-angad/jatti-lang
2. Put `.jatti` files in same folder as `cli.py`
3. Test with `chilla_we "hello"`

### For other issues:
Visit: https://github.com/s-angad/jatti-lang/issues

---

## 🎉 You're Ready!

Now you can:
- ✅ Write Jatti code with syntax highlighting
- ✅ Run code with one click
- ✅ Use custom file icons
- ✅ Build to Python
- ✅ Format code

**Happy coding! 🚀**
