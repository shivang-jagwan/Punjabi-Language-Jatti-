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
**Author:** Mr. Angad Singh

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
12. [String Methods](#string-methods)
13. [Error Handling](#error-handling)
14. [Examples](#examples)
15. [Installation](#installation)
16. [VS Code Extension](#vs-code-extension)
17. [Documentation](#documentation)

---

## 🎯 About Jatti

Created by **Mr. Angad Singh** to make programming accessible and fun!

### Why Jatti?

✨ **Easy to Learn** - Clear, readable syntax  
✨ **Fun Syntax** - Punjabi keywords make coding enjoyable  
✨ **Powerful** - Full functional and procedural support  
✨ **Fast** - Compiled bytecode execution via C VM  

---

## ✨ Features

### Core Features
- ✅ **Interpreted Language** - Run code directly via C VM
- ✅ **Dynamic Typing** - Types determined at runtime
- ✅ **Functions** - First-class functions with recursion
- ✅ **Collections** - Lists and dictionaries
- ✅ **String Support** - Full string operations and methods
- ✅ **Exception Handling** - `chal_koshish_karle` / `pakad` blocks
- ✅ **File I/O** - Read and write files
- ✅ **Loops & Conditionals** - Full control flow

### Advanced Features
- ✅ **Recursion** - Full support for recursive functions
- ✅ **List Operations** - Indexing and iteration
- ✅ **String Methods** - 8 Punjabi string methods (vada_likha, chhota_likha, vand_karo, etc.)
- ✅ **Built-in Functions** - 8 utility functions plus 2 Punjabi aliases
- ✅ **Math Operations** - Complete arithmetic including power operator (**)
- ✅ **Debugging** - Clear error messages with cultural roasts

### IDE Support
- ✅ **VS Code Extension** - Full editor integration
- ✅ **Syntax Highlighting** - Color-coded syntax
- ✅ **Run Button** - One-click execution
- ✅ **Output Panel** - Dedicated output pane
- ✅ **Error Messages** - Clear error reporting with roasts

---

## 🚀 Quick Start

### Install Jatti

```powershell
# From repository root, use:
jatti run yourfile.jatti

# Or fallback:
.\jatti.cmd run yourfile.jatti
```

### Your First Program

**File: `hello.jatti`**

```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

**Run it:**

```powershell
jatti run hello.jatti
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
```jatti
chal_oye greeting ban "Hello"
chal_oye name ban "World"
chilla_we greeting
```

### Numbers (Integer & Float)
```jatti
chal_oye age ban 25
chal_oye height ban 5.9
chal_oye pi ban 3.14159
```

### Boolean
```jatti
chal_oye isTrue ban sach
chal_oye isFalse ban jhoot
```

### Lists
```jatti
chal_oye fruits ban ["apple", "banana", "mango"]
chal_oye numbers ban [1, 2, 3, 4, 5]
chal_oye mixed ban [1, "text", 3.14, sach]
```

### Dictionaries
```jatti
chal_oye person ban {
    "name": "Singh",
    "age": 25,
    "city": "Punjab"
}
```

### Khaali (None)
```jatti
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
| `ate` | And | AND operator |
| `ya_te` | Or | OR operator |
| `nahi` | Not | NOT operator |

---

## ➕ Operations

### Arithmetic

```jatti
sun_we
    chal_oye a ban 10
    chal_oye b ban 3
    
    chilla_we a + b          fuddu_chiz 13
    chilla_we a - b          fuddu_chiz 7
    chilla_we a * b          fuddu_chiz 30
    chilla_we a / b          fuddu_chiz 3.33
    chilla_we a % b          fuddu_chiz 1
ja_we
```

### Comparison

```jatti
sun_we
    chal_oye x ban 5
    
    chilla_we x vadha_hai 3           fuddu_chiz sach
    chilla_we x nikka_hai 10          fuddu_chiz sach
    chilla_we x barabar 5             fuddu_chiz sach
ja_we
```

### Logical

```jatti
sun_we
    chal_oye a ban sach
    chal_oye b ban jhoot
    
    je a ate b                   fuddu_chiz AND operator
        chilla_we "Both sach"
ja_we
```

---

## 🔀 Control Flow

### If-Else

```jatti
sun_we
    chal_oye age ban 18
    
    je age vadha_hai 18
        chilla_we "Adult"
    nahin_taan
        chilla_we "Minor"
ja_we
```

### For Loop

```jatti
sun_we
    har_ek i range_banao(1, 5)
        chilla_we i
ja_we
```

**Output:**
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

---

## 🎁 Built-in Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `range_banao(n)` | Create range | `range_banao(5)` → 0,1,2,3,4 |
| `kinna_lamba()` | Length | `kinna_lamba([1,2,3])` → 3 |
| `kism()` | Type | `kism(5)` → number |
| `likh()` | Write file | `likh("file.txt", "text")` |
| `padh()` | Read file | `padh("file.txt")` |
| `ganao()` | Sum | `ganao([1,2,3])` → 6 |
| `sab_ton_vaddha()` | Max | `sab_ton_vaddha([1,5,3])` → 5 |
| `sab_ton_chhota()` | Min | `sab_ton_chhota([1,5,3])` → 1 |
| `chal_sort_hoja()` / `sorted()` | Sort | `chal_sort_hoja([3,1,2])` → [1,2,3] |
| `chal_reverse_hoja()` / `reversed()` | Reverse | `chal_reverse_hoja([1,2,3])` → [3,2,1] |

---

## 🔤 String Methods

Jatti provides powerful string manipulation functions:

| Method | Purpose | Example |
|--------|---------|---------|
| `vada_likha(str)` | Uppercase | `vada_likha("hello")` → "HELLO" |
| `chhota_likha(str)` | Lowercase | `chhota_likha("HELLO")` → "hello" |
| `saf_karo(str)` | Trim spaces | `saf_karo("  text  ")` → "text" |
| `vand_karo(str, delim)` | Split string | `vand_karo("a,b,c", ",")` → ["a", "b", "c"] |
| `badal_de(str, old, new)` | Replace | `badal_de("hello", "l", "L")` → "heLLo" |
| `shuru_hunda(str, prefix)` | Check start | `shuru_hunda("hello", "he")` → sach |
| `khatam_hunda(str, suffix)` | Check end | `khatam_hunda("hello", "lo")` → sach |
| `dhundh_ja(str, substr)` | Find index | `dhundh_ja("hello", "ll")` → 2 |

### String Methods Examples

```jatti
sun_we
    chal_oye text ban "Jatti Programming"
    
    chilla_we vada_likha(text)          fuddu_chiz JATTI PROGRAMMING
    chilla_we chhota_likha(text)        fuddu_chiz jatti programming
    
    chal_oye words ban vand_karo(text, " ")
    chilla_we words                     fuddu_chiz ["Jatti", "Programming"]
    
    je shuru_hunda(text, "Jatti")
        chilla_we "Shuru hunda Jatti naal"
    
    chal_oye position ban dhundh_ja(text, "a")
    chilla_we position                 fuddu_chiz 1
    
    chal_oye replaced ban badal_de(text, "Jatti", "JATTI")
    chilla_we replaced                 fuddu_chiz JATTI Programming
    
    je khatam_hunda(text, "ing")
        chilla_we "Khatam hunda ing naal"
ja_we
```

---

## ❌ Error Handling

### Try-Catch Blocks

```jatti
sun_we
    chal_koshish_karle
        chal_oye result ban 10 / 0
    pakad err
        chilla_we "Error caught: " + err
ja_we
```

### Error Output With Roasts

Jatti shows a random Punjabi roast first, then the error:

```text
🔥 Roast: Syntax nu respect de.
❌ JATTI ERROR
🔴 Error: Program must start with sun_we.
📍 Line 1
```

### Available Roasts

- "Galti ho gayi !! koi gall nahi."
- "Dhyaan de, Jatti style rakhi !!"
- "Phir ohi mistake !!"
- "Tu compiler nu test kar reha !!"
- "Compiler thak gaya. Tu vi !!"
- "Tu coding chadd de !!"
- "Tere to nhi hona oye !!"
- "Eh ki likh ta tu?"
- "Dimag use kar le thoda."
- "Jatti Lang mazak nahi hai."
- "Syntax nu respect de."

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
ja_we
```

### Example 2: String Processing

```jatti
sun_we
    chal_oye sentence ban "Jatti is amazing"
    
    chal_oye upper_text ban vada_likha(sentence)
    chilla_we upper_text
    
    chal_oye words ban vand_karo(sentence, " ")
    chal_oye word_count ban kinna_lamba(words)
    chilla_we word_count
ja_we
```

### Example 3: File Operations

```jatti
sun_we
    likh("output.txt", "Hello from Jatti!")
    
    chal_oye content ban padh("output.txt")
    chilla_we content
ja_we
```

---

## 🎨 Installation

### Windows

```powershell
# Clone repository
git clone https://github.com/yourrepo/jatti-lang.git

# Navigate to directory
cd jatti-lang

# Run a file
jatti run yourfile.jatti
```

See [LOCAL_SETUP.md](./LOCAL_SETUP.md) for detailed setup.

---

## 🎨 VS Code Extension

### Features
- ✅ Syntax highlighting
- ✅ Run button (▶️)
- ✅ Keyboard shortcuts (Ctrl+Alt+R)
- ✅ Dedicated output panel
- ✅ Error reporting
- ✅ Marketplace icon

### Usage
1. Create `hello.jatti`
2. Click ▶️ button or press Ctrl+Alt+R
3. See output in **Jatti** output panel

---

## 📚 Documentation

Complete documentation available:

- **[Language Specification](./LANGUAGE_SPECIFICATION.md)** - Complete reference
- **[Beginner Tutorial](./BEGINNER_TUTORIAL.md)** - Start here!
- **[Intermediate Guide](./INTERMEDIATE_GUIDE.md)** - Advanced techniques
- **[Advanced Topics](./ADVANCED_TOPICS.md)** - Best practices
- **[Language Basics](./LANGUAGE_BASICS.md)** - Variables/operators/loops

---

## 🎓 Learning Path

**Beginner:**
1. Read: [Beginner Tutorial](./BEGINNER_TUTORIAL.md)
2. Try: `hello.jatti` example
3. Practice: Simple programs

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
- **Lines of Code:** 3500+
- **Keywords:** 27
- **Built-in Functions:** 8 (plus 2 Punjabi aliases)
- **String Methods:** 8 Punjabi methods
- **Total Functions:** 16 + 2 aliases = 18
- **Examples:** 60+
- **Documentation:** 1700+ lines

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 👤 Author

**Mr. Singh / Mr. Angad Singh**

- Created: January 2025
- Language: Jatti
- Inspiration: Punjabi culture, Python simplicity

---

## 🙏 Acknowledgments

Thanks to:
- Punjabi language speakers
- Python community for inspiration
- All contributors and users

---

## 📞 Support

- 📧 Email: jatti-lang@example.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 📜 Version History

### v0.4.0 (Current - Production Ready) ✅
- ✅ Full recursive function support
- ✅ String methods API with Punjabi names (vada_likha, chhota_likha, vand_karo, badal_de, saf_karo, shuru_hunda, khatam_hunda, dhundh_ja)
- ✅ Safe string handling
- ✅ All comparison operators
- ✅ Punjabi roast error messages with exception types
- ✅ VS Code output panel integration
- ✅ Try-catch exception handling
- ✅ Comprehensive test coverage

### v0.3.0
- Basic language features
- String operations
- Collections (lists, dicts)
- Control flow (if/else, loops)

---

**Happy Coding! 🎉 - Jatti Lang Team**
