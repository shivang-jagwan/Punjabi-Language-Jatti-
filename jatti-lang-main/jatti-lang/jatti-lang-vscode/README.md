# 🚀 Jatti Language

**A Modern Programming Language Inspired by Punjabi**

```
     ██  █████  ████████ ████████ ██   ██ 
     ██ ██   ██    ██       ██    ██   ██
     ██ ███████    ██       ██    ██   ██
██   ██ ██   ██    ██       ██    ██  
 █████  ██   ██    ██       ██    ██   ██
```

**Version:** 0.4.0  
**Status:** Production Ready ✅  
**License:** MIT  
**Author:** Mr. AngadSingh

---

## 📋 Table of Contents

1. [About Jatti](#about-jatti)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Syntax Reference](#syntax-reference)
5. [Data Types](#data-types)
6. [Keywords](#keywords)
7. [Operations](#operations)
8. [Control Flow](#control-flow)
9. [Functions](#functions)
10. [Collections](#collections)
11. [Built-in Functions](#built-in-functions)
12. [Examples](#examples)
13. [Installation](#installation)
14. [VS Code Extension](#vs-code-extension)
15. [Documentation](#documentation)

---

## 🎯 About Jatti

Jatti is a **modern, interpreted programming language** that combines:
- **Punjabi-inspired syntax** for readability
- **Python-like simplicity** for learning
- **Strong typing support** for reliability
- **Fast execution** for development speed

Created by **Mr. Angad Singh** to make programming accessible and fun!

### Why Jatti?

✨ **Easy to Learn** - Clear, readable syntax  
✨ **Fun Syntax** - Punjabi keywords make coding enjoyable  
✨ **Powerful** - Full OOP, functional, and procedural support  
✨ **Fast** - Compiled to Python for speed  

---

## ✨ Features

### Core Features
- ✅ **Interpreted Language** - Run code directly
- ✅ **Dynamic Typing** - Types determined at runtime
- ✅ **Functions** - First-class functions, closures
- ✅ **Collections** - Lists, dictionaries, sets
- ✅ **String Support** - Unicode, string operations
- ✅ **Exception Handling** - chal_koshish_karle-catch blocks
- ✅ **File I/O** - Read and write files
- ✅ **Loops & Conditionals** - Full control flow

### Advanced Features
- ✅ **Recursion** - Full support for recursive functions
- ✅ **Lambda Functions** - Anonymous functions
- ✅ **List Comprehensions** - Compact list creation
- ✅ **Built-in Functions** - 20+ utility functions
- ✅ **String Methods** - Powerful string manipulation
- ✅ **Math Operations** - Complete arithmetic
- ✅ **Debugging** - Debug mode for tracing

### IDE Support
- ✅ **VS Code Extension** - Full editor integration
- ✅ **Syntax Highlighting** - Color-coded syntax
- ✅ **Run Button** - One-click execution
- ✅ **Output Panel** - See results instantly
- ✅ **Error Messages** - Clear error reporting

---

## 🚀 Quick Start

### Install Jatti

**Option 1: Download from GitHub**
```bash
git clone https://github.com/s-angad/jatti-lang
cd jatti-lang
```

**Option 2: For VS Code**
1. Install extension: Search "Jatti Language" in Extensions
2. Download Jatti CLI from GitHub
3. Extract to your project folder

### Your First Program

**File: `hello.jatti`**
```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

**Run it:**
```bash
python cli.py run hello.jatti
```

**Output:**
```
Hello Jatti!
```

---

## 📝 Syntax Reference

### Program Structure

Every Jatti program must have this structure:

```jatti
sun_we
    fuddu_chiz Your code here
ja_we
```

**Translation:**
- `sun_we` = "Listen"  (Start main block)
- `ja_we` = "Go" (End main block)
- `fuddu_chiz` = Comment

### Comments

```jatti
fuddu_chiz This is a comment
fuddu_chiz Use fuddu_chiz to add notes
```

---

## 🔤 Data Types

### Strings
```
chal_oye greeting ban "Hello"
chal_oye name ban "World"
chilla_we greeting
```

### Numbers (Integer & Float)
```
chal_oye age ban 25
chal_oye height ban 5.9
chal_oye pi ban 3.14159
```

### Boolean
```
chal_oye isTrue ban sach
chal_oye isFalse ban jhoot
```

### Lists
```
chal_oye fruits ban ["apple", "banana", "mango"]
chal_oye numbers ban [1, 2, 3, 4, 5]
chal_oye mixed ban [1, "text", 3.14, sach]
```

### Dictionaries
```
chal_oye person ban {
    "name": "Singh",
    "age": 25,
    "city": "Punjab"
}
```

### Khaali (None)
```
chal_oye empty ban khaali
```

---

## 🔑 Keywords

| Keyword | Meaning | Usage |
|---------|---------|-------|
| `sun_we` | Listen | Start main block |
| `ja_we` | Go | End main block |
| `chal_oye` | Let's go | Variable assignment |
| `ban` | Is/Become | Assignment operator |
| `chilla_we` | Shout | Print output |
| `fuddu_chiz` | Nonsense/Comment | Add comment |
| `je` | If | Conditional |
| `nahin_taan_je` | if else if | if Else block |
| `nahin_taan` | Otherwise | Else block |
| `har_ek` | Every one | For loop |
| `jadon_tak` | While | While loop |
| `roko_oye_roko` | Stop/Halt | Exit loop |
| `chalo_oye_chalo` | Go/Continue | Skip iteration |
| `kaam` | Work/Function | Define function |
| `wapas_kar` | Return | Return value |
| `chal_koshish_karle` | Attempt/Try | Try block |
| `pakad` | Catch | Catch block |
| `vadha_hai` | Greater than | > |
| `nikka_hai` | Less than | < |
| `barabar` | Equal | == |
| `barabar_nahi_hai` | Not equal | != |
| `vadha_ya_barabar` | Greater or equal | >= |
| `nikka_ya_barabar` | Less or equal | <= |
| `sach` | Truth | Boolean true |
| `jhoot` | Lie | Boolean false |
| `khaali` | Empty | Null/None value |

---

## ⚠️ Special Conditions & Requirements

**IMPORTANT:** These conditions must be followed for code to work correctly:

### 1. **Program Structure (REQUIRED)**
- Every Jatti program MUST start with `sun_we` and end with `ja_we`
- `sun_we` must be at line 1 (no blank lines before it)
- `ja_we` must be the last line
- All code must be indented inside the `sun_we...ja_we` block

### 2. **Functions (REQUIRED)**
- Functions MUST have a `wapas_kar` (return) statement - this is **NOT optional**
- Functions must be defined inside the `sun_we...ja_we` block
- Function calls MUST be in an assignment context: `chal_oye result ban function_name()`
- Or in a print context: `chilla_we function_name()`

### 3. **Control Flow Blocks**
- `if...else` blocks use indentation (Python-style), NO closing keyword
- Multiple conditions: use `nahin_taan_je` for "else if", then `nahin_taan` for final "else"
- Example:
  ```jatti
  je condition1
      fuddu_chiz do something
# Jatti VS Code Extension (snapshot folder)

This folder is a snapshot/duplicate copy.

Use the canonical extension docs in the repo root:

- [jatti-lang-vscode/README.md](../../../jatti-lang-vscode/README.md)
- [jatti-lang-vscode/USER_SETUP_GUIDE.md](../../../jatti-lang-vscode/USER_SETUP_GUIDE.md)
```jatti
sun_we
    har_ek i range_banao(1, 5)
        chilla_we i
ja_we
```

Output:
```
1
2
3
4
```

### While Loop

```jatti
sun_we
    chal_oye count ban 0
    
    jadon_tak count nikka_hai 5
        chilla_we count
        chal_oye count ban count + 1
ja_we
```

### roko_oye_roko & chalo_oye_chalo

```jatti
sun_we
    har_ek i range_banao(1, 10)
        je i barabar 5
            roko_oye_roko
        nahin_taan
            chilla_we i
ja_we
```

---

## 🔧 Functions

### Define Function

**Important:** Functions MUST be inside the `sun_we...ja_we` block and MUST have a `wapas_kar` (return) statement!

```jatti
sun_we
    kaam greet(name)
        chilla_we "Hello, " + name
        wapas_kar "Done"
    
    chal_oye result ban greet("Singh")
ja_we
```

### Return Value

```jatti
sun_we
    kaam add(x, y)
        wapas_kar x + y
    
    chal_oye result ban add(5, 3)
    chilla_we result
ja_we
```

### Parameters

```jatti
sun_we
    kaam product(a, b, c)
        wapas_kar a * b * c
    
    chilla_we product(2, 3, 4)
ja_we
```

---

## 📦 Collections

### Lists

```jatti
sun_we
    chal_oye fruits ban ["apple", "banana", "mango"]
    
    fuddu_chiz Access elements
    chilla_we fruits[0]         fuddu_chiz apple
    chilla_we fruits[1]         fuddu_chiz banana
    
    fuddu_chiz List length
    chilla_we kinna_lamba(fruits)  fuddu_chiz 3
    
    fuddu_chiz Loop through list
    har_ek fruit fruits
        chilla_we fruit
ja_we
```

### Dictionaries

```jatti
sun_we
    chal_oye person ban {"name": "Singh", "age": 25}
    
    fuddu_chiz Access values
    chilla_we person["name"]    fuddu_chiz Singh
    chilla_we person["age"]     fuddu_chiz 25
ja_we
```

### List Operations

```jatti
sun_we
    chal_oye list ban [1, 2, 3]
    
    fuddu_chiz Add element
    chal_oye list ban list te [4]
    
    fuddu_chiz fuddu_chizove element
    fuddu_chiz (use slicing or built-in functions)
ja_we
```

---

## 🎁 Built-in Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `range_banao(n)`| Create range | `range_banao(5)` → 0,1,2,3,4 |
| `kinna_lamba()` | Length | `kinna_lamba([1,2,3])` → 3 |
| `kism()` | Type | `kism(5)` → int |
| `likh()` | Write to file | `likh("file.txt", "text")` |
| `padh()` | Read file | `padh("file.txt")` |
| `ganao()` | Sum | `ganao([1,2,3])` → 6 |
| `sab_ton_vaddha()` | Max | `sab_ton_vaddha([1,5,3])` → 5 |
| `sab_ton_chhota()` | Min | `sab_ton_chhota([1,5,3])` → 1 |
| `sorted()` | Sort | `sorted([3,1,2])` → [1,2,3] |
| `reversed()` | Reverse | `reversed([1,2,3])` → [3,2,1] |

---

## 💡 Examples

### Example 1: Calculator

```jatti
sun_we
    kaam calculate(a, op, b)
        je op barabar "+"
            wapas_kar a + b
        nahin_taan_je op barabar "-"
            wapas_kar a - b
        nahin_taan_je op barabar "*"
            wapas_kar a * b
        nahin_taan
            wapas_kar a / b
    
    chal_oye result1 ban calculate(10, "+", 5)
    chilla_we result1
    
    chal_oye result2 ban calculate(10, "-", 3)
    chilla_we result2
    
    chal_oye result3 ban calculate(10, "*", 2)
    chilla_we result3
ja_we
```

### Example 2: Fibonacci Sequence

```jatti
sun_we
    fuddu_chiz Generate first 10 Fibonacci numbers
    chal_oye fib ban [0, 1]
    chal_oye count ban 0
    
    jadon_tak count nikka_hai 8
        chal_oye next ban fib[kinna_lamba(fib) - 2] + fib[kinna_lamba(fib) - 1]
        chal_oye fib ban fib te [next]
        chal_oye count ban count + 1
    
    fuddu_chiz Print sequence
    har_ek num fib
        chilla_we num
ja_we
```

### Example 3: Todo List

```jatti
sun_we
    chal_oye todos ban ["Code", "Test", "Deploy"]
    
    chilla_we "Todos:"
    chal_oye count ban kinna_lamba(todos)
    chal_oye index ban 0
    
    jadon_tak index nikka_hai count
        chal_oye num ban index + 1
        chilla_we num
        chilla_we todos[index]
        chal_oye index ban index + 1
ja_we
```

---

## 📥 Installation

### Requirements
- Python 3.6+
- Windows/Mac/Linux

### Setup

**Step 1: Clone Repository**
```bash
git clone https://github.com/s-angad/jatti-lang
cd jatti-lang
```

**Step 2: Run Programs**
```bash
python cli.py run hello.jatti
```

**Step 3: Build to Python (Optional)**
```bash
python cli.py build hello.jatti -o hello.py
```

---

## 🎨 VS Code Extension

### Install Extension
1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search: **"Jatti Language"**
4. Click **Install**
5. **Reload VS Code** (`Ctrl+Shift+P` → "Reload Window")

### Features
- ✅ Syntax highlighting
- ✅ Run button (▶️)
- ✅ Keyboard shortcuts (Ctrl+Shift+J)
- ✅ Output panel
- ✅ Error reporting
- ✅ Custom file icons for `.jatti` files

### Enable Custom File Icons
To see the **Jatti file icon** in your explorer:

1. Open VS Code **Settings** (`Ctrl+,`)
2. Search: **"icon theme"**
3. In **Workbench › Icon Theme**, select **"Jatti File Icons"**
4. Done! Now `.jatti` files will show the custom Jatti icon ✨

### Usage
1. Create `hello.jatti`
2. Click ▶️ button (or press `Ctrl+Shift+J`)
3. See output instantly!

### ⚠️ Important Notes

**Syntax highlighting works everywhere** - Just install the extension and create `.jatti` files  
**Run button requires full package** - Download from https://github.com/s-angad/jatti-lang  
**First time users?** - Read [SETUP_FOR_USERS.md](./SETUP_FOR_USERS.md)  
**Troubleshooting?** - See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

## 📚 Documentation

Complete documentation available:

- **[Language Specification](./LANGUAGE_SPECIFICATION.md)** - Complete reference
- **[Beginner Tutorial](./BEGINNER_TUTORIAL.md)** - Start here!
- **[Intermediate Guide](./INTERMEDIATE_GUIDE.md)** - Advanced techniques
- **[Advanced Topics](./ADVANCED_TOPICS.md)** - Best practices

---

## 🔍 CLI Commands

```bash
# Run a program
python cli.py run program.jatti

# Build to Python
python cli.py build program.jatti -o output.py

# Format code
python cli.py format program.jatti

# Debug mode
python cli.py run program.jatti --debug

# Show help
python cli.py --help
```

---

## 🐛 Known Limitations

_(None at this time - all major issues have been fixed!)_

### Previously Fixed Issues ✅
- ✅ **Recursive Functions** - Now fully supported (v0.4.0+)
- ✅ **String Safety** - Operators in strings no longer cause errors
- ✅ **Comparison Operators** - All 6 operators working (>, <, ==, !=, >=, <=)
- ✅ **Documentation** - All keywords now accurate and tested

---

## 🎓 Learning Path

**Beginner:**
1. Read: [Beginner Tutorial](./BEGINNER_TUTORIAL.md)
2. chal_koshish_karle: `hello.jatti` example
3. Practice: Create simple programs

**Intermediate:**
1. Read: [Intermediate Guide](./INTERMEDIATE_GUIDE.md)
2. Learn: Functions, loops, collections
3. Build: Small projects

**Advanced:**
1. Read: [Advanced Topics](./ADVANCED_TOPICS.md)
2. Optimize: Performance tips
3. Master: Complex patterns

---

## 📊 Language Stats

- **Version:** 0.4.0
- **Lines of Code:** 2000+
- **Keywords:** 20+
- **Built-in Functions:** 20+
- **Examples:** 50+
- **Documentation:** 1400+ lines

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 👤 Author

**Mr. Singh**

- Created: January 2025
- Language: Jatti
- Inspiration: Punjabi culture, Python simplicity

---

## 🙏 Acknowledgments

Thanks to:
- Python community for inspiration
- Punjabi language speakers
- All contributors and users

---

## 📞 Support

- 📧 Email: workforangad@gmail.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## � Version History

### v0.4.0 (Current - Production Ready) ✅
**Major Bug Fixes & Improvements:**
- ✅ Full recursive function support (fixed infinite loop issues)
- ✅ Safe string handling (operators in strings no longer cause errors)
- ✅ All 6 comparison operators implemented: `>`, `<`, `==`, `!=`, `>=`, `<=`
- ✅ Complete documentation audit and fixes
- ✅ Comprehensive test coverage
- ✅ Performance optimizations

### v0.3.0
- Basic language features
- String operations
- Collections (lists, dicts)
- Control flow (if/else, loops)

---

## �🚀 Future Roadmap

- [ ] Jatti 0.5.0 - Object-oriented features
- [ ] Jatti 0.6.0 - Package manager
- [ ] Jatti 1.0 - Stable release
- [ ] Online playground
- [ ] Mobile support

---

## 🎉 Get Started Now!

```bash
cd jatti-lang
python cli.py run example.jatti
```

**Happy Coding with Jatti! ਜੱਟੀ 🚀**

---

**Made with ❤️ for the Punjabi tech community**

