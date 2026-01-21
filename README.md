# Jatti Language

Jatti is a Punjabi-inspired programming language (interpreter + CLI) with a simple 2‑pane web playground and a VS Code extension.

## Important docs

- Local setup (Windows): [LOCAL_SETUP.md](./LOCAL_SETUP.md)
- Language basics (variables/operators/loops): [LANGUAGE_BASICS.md](./LANGUAGE_BASICS.md)
- Deployment (Docker/Vercel/Render): [DEPLOYMENT.md](./DEPLOYMENT.md)

Reference docs:

- Beginner tutorial: [BEGINNER_TUTORIAL.md](./BEGINNER_TUTORIAL.md)
- Intermediate guide: [INTERMEDIATE_GUIDE.md](./INTERMEDIATE_GUIDE.md)
- Language specification: [LANGUAGE_SPECIFICATION.md](./LANGUAGE_SPECIFICATION.md)

## Quick start

Create `hello.jatti`:

```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

Run:

```bash
python cli.py run hello.jatti
```

Web playground:

```bash
python playground_server.py
```

Open `http://127.0.0.1:8000/`.

## Auth note (current default)

API-key auth is **disabled by default**.

- To keep it open: leave `JATTI_REQUIRE_API_KEY` unset (or set it to `0`)
- To enable later: set `JATTI_REQUIRE_API_KEY=1` and `JATTI_API_KEY=<secret>`

For variables/operators and core syntax, see [LANGUAGE_BASICS.md](./LANGUAGE_BASICS.md).

<!--

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
  nahin_taan_je condition2
      fuddu_chiz do something else
  nahin_taan
      fuddu_chiz default case
  ```

### 4. **Loops**
- `har_ek` (for loop): Syntax is `har_ek variable iterable`
- `jadon_tak` (while loop): Condition must follow the keyword
- `roko_oye_roko` (break): Can only be used inside loops
- `chalo_oye_chalo` (continue): Can only be used inside loops
- Loop variables can be used in `chilla_we` but not in assignments (use temp variables instead)

### 5. **Expressions & Function Calls**
- User-defined function calls must be in assignment context: `chal_oye result ban function()`
- Nested function calls (e.g., `range_banao(kinna_lamba(list))`) are not supported - assign to a variable first
- String concatenation with `te` only works in `chilla_we` statements, not in assignments
- Use `+` for arithmetic, `te` for string output in print statements

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
    
    chilla_we x vadha_hai 3     fuddu_chiz sach
    chilla_we x nikka_hai 10      fuddu_chiz sach
    chilla_we x barabar 5       fuddu_chiz sach
ja_we
```

### Logical

```jatti
sun_we
    chal_oye a ban sach
    chal_oye b ban jhoot
    
    je a te b                   fuddu_chiz AND operator
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

### Features
- ✅ Syntax highlighting
- ✅ Run button (▶️)
- ✅ Keyboard shortcuts (Ctrl+Shift+J)
- ✅ Output panel
- ✅ Error reporting

### Usage
1. Create `hello.jatti`
2. Click ▶️ button
3. See output instantly!

---

## 📚 Documentation

Complete documentation available:

- **[Language Specification](./LANGUAGE_SPECIFICATION.md)** - Complete reference
- **[Beginner Tutorial](./BEGINNER_TUTORIAL.md)** - Start here!
- **[Intermediate Guide](./INTERMEDIATE_GUIDE.md)** - Advanced techniques
- **[Advanced Topics](./ADVANCED_TOPICS.md)** - Best practices

---

## 🌐 Web Playground

Local 2-pane editor + output UI (no CLI commands needed):

- See [PLAYGROUND.md](./PLAYGROUND.md)

Docker demo:

- `docker build -t jatti-playground .`
- `docker run --rm -p 8000:8000 jatti-playground`

---

## Deploy (Vercel)

This repo includes a Vercel-ready setup:

- Static UI is served from `frontend/` via [vercel.json](vercel.json) rewrites.
- API runs as Vercel Python Functions under `api/`:
    - `/api/run` → [api/run.py](api/run.py)
    - `/api/healthz` → [api/healthz.py](api/healthz.py)

Steps:

1) Push the repo to GitHub.
2) Import the repo in Vercel.
3) Set Environment Variables in Vercel:
    - Optional: `JATTI_REQUIRE_API_KEY=1` and `JATTI_API_KEY` (to enforce X-API-Key)
     - Optional: `JATTI_TIMEOUT_SEC`, `JATTI_MAX_CODE_BYTES`, `JATTI_MAX_OUTPUT_BYTES`
4) Deploy.

Security note: this executes user-provided code. Use conservative limits; if you enable auth, use `JATTI_REQUIRE_API_KEY=1` + a strong `JATTI_API_KEY`.

---

## Deploy (Render)

Render deployment is included via a Blueprint file:

- [render.yaml](render.yaml)

Steps:

1) In Render Dashboard: New → **Blueprint**.
2) Select your GitHub repo.
3) Render reads [render.yaml](render.yaml) and provisions the service.
4) Deploy and open the provided `.onrender.com` URL.

Notes:

- Tune limits in Render env vars: `JATTI_TIMEOUT_SEC`, `JATTI_MAX_CODE_BYTES`, `JATTI_MAX_OUTPUT_BYTES`, `JATTI_RATE_*`.

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

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 👤 Author

**Mr. angad Singh**

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

-->
