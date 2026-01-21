# 📖 Jatti Language - Complete Specification

**Version:** 0.4.0  
**Last Updated:** January 2026  
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [Syntax Basics](#syntax-basics)
3. [Data Types](#data-types)
4. [Operators](#operators)
5. [Control Flow](#control-flow)
6. [Functions](#functions)
7. [Built-in Functions](#built-in-functions)
8. [String Methods](#string-methods)
9. [Collections](#collections)
10. [Error Handling](#error-handling)
11. [Advanced Features](#advanced-features)
12. [Standard Library](#standard-library)
13. [CLI Tools](#cli-tools)

---

## Overview

**Jatti** is a dynamically-typed, interpreted programming language designed to be accessible to Punjabi speakers and developers familiar with Python. It combines familiar programming concepts with Punjabi-influenced syntax.

### Key Features
- 🇮🇳 Punjabi-inspired keywords (intuitive and memorable)
- 🐍 Python-compatible (compiles to Python)
- ⚡ Dynamic typing with automatic type coercion
- 🔄 First-class functions and lambdas
- 📚 Rich collection types (lists, dicts, tuples)
- 🛡️ Exception handling with chal_koshish_karle/catch
- 🎯 Simple, readable syntax

### Design Philosophy
- **Accessibility:** Non-programmers should understand the syntax
- **Expressiveness:** Powerful enough for real programs
- **Compatibility:** Works with Python libraries seamlessly

---

## Syntax Basics

### Comments
```jatti
# This is a comment
# Comments start with # and go to end of line
```

### Programs
Every Jatti program has this structure:
```jatti
sun_we
    # Your code here
ja_we
```

- `sun_we` = Program start (like Python's `if __name__ == "__main__":`)
- `ja_we` = Program end
- Code inside must be indented with 4 spaces

### Example Program
```jatti
sun_we
    chilla_we "Hello, World!"
    chal_oye x ban 5
    chilla_we x
ja_we
```

---

## Data Types

### Primitives

#### Numbers (Integer & Float)
```jatti
chal_oye age ban 25          # Integer
chal_oye price ban 19.99     # Float
chal_oye negative ban -10    # Negative
```

#### Strings
```jatti
chal_oye name ban "Singh"
chal_oye greeting ban 'Hello'
chal_oye multiline ban "Line 1
Line 2
Line 3"
```

**Escape Sequences:**
```jatti
"\n"      # Newline
"\t"      # Tab
"\\"      # Backslash
"\""      # Double quote
"\'"      # Single quote
```

#### Booleans
```jatti
chal_oye is_active ban sach     # sach
chal_oye is_deleted ban khaali   # jhoot
```

### Collections

#### Lists (Arrays)
```jatti
chal_oye numbers ban [1, 2, 3, 4, 5]
chal_oye mixed ban [1, "two", 3.0, sach]
chal_oye empty ban []

# Access by index
chilla_we numbers[0]      # Output: 1
chilla_we numbers[-1]     # Output: 5 (last element)

# Slicing
chal_oye slice ban numbers[1:3]   # [2, 3]
```

#### Dictionaries
```jatti
chal_oye person ban {
    naam: "Singh",
    age: 25,
    city: "Punjab"
}

# Access by key
chilla_we person["naam"]         # Output: Singh
chilla_we person.get("country")  # Output: None (if key doesn't exist)
```

#### Tuples (Immutable)
```jatti
chal_oye point ban (10, 20, 30)
chilla_we point[0]    # Output: 10
```

---

## Operators

### Arithmetic
```jatti
chal_oye sum ban 10 + 5        # 15
chal_oye diff ban 10 - 5       # 5
chal_oye product ban 10 * 5    # 50
chal_oye quotient ban 10 / 5   # 2
chal_oye fuddu_chizainder ban 10 % 3  # 1
chal_oye power ban 2 ** 3      # 8
```

### Comparison
```jatti
chal_oye a ban 5
chal_oye b ban 3

je a vadha_hai b              # a > b (greater than)
je a nikka_hai b              # a < b (less than)
je a barabar b                # a == b (equal)
je a barabar_nahi_hai b       # a != b (not equal)
je a vadha_ya_barabar b       # a >= b (greater than or equal)
je a nikka_ya_barabar b       # a <= b (less than or equal)
```

### Logical
```jatti
je (x vadha_hai 5) hor (y nikka_hai 3)        # OR
je (x vadha_hai 5) ate (y nikka_hai 3)        # AND
je nahi (x barabar 0)                     # NOT
```

### Assignment
```jatti
chal_oye x ban 10
chal_oye x ban x + 5          # x = 15
```

---

## Control Flow

### If/Elif/Else
```jatti
chal_oye score ban 85

je score vadha_ya_barabar 90
    chilla_we "A Grade"
nahin_taan_je score vadha_ya_barabar 80
    chilla_we "B Grade"
nahin_taan_je score vadha_ya_barabar 70
    chilla_we "C Grade"
nahin_taan
    chilla_we "F Grade"
```

**Keywords:**
- `je` = if
- `nahin_taan_je` = elif
- `nahin_taan` = else

### While Loop
```jatti
chal_oye count ban 0
jadon_tak count nikka_hai 5
    chilla_we count
    chal_oye count ban count + 1
```

**Keywords:**
- `jadon_tak` = while
- `roko_oye_roko` = exit loop
- `chalo_oye_chalo` = skip iteration

### For Loop
```jatti
har_ek number [1, 2, 3, 4, 5]
    chilla_we number

har_ek i range(10)
    chilla_we i

har_ek key, value person
    chilla_we key hor value
```

**Keywords:**
- `har_ek` = for
- Works with lists, dicts, ranges, and any iterable

### roko_oye_roko & chalo_oye_chalo
```jatti
har_ek i range(10)
    je i barabar 5
        roko_oye_roko

har_ek i range(10)
    je i % 2 barabar 0
        chalo_oye_chalo
    chilla_we i
```

---

## Functions

### Definition
```jatti
kaam greet(name)
    chilla_we "Hello, " hor name
ja_we

greet("Singh")
```

### With Return
```jatti
kaam add(a, b)
    chal_oye result ban a + b
    wapas_kar result
ja_we

chal_oye sum ban add(5, 3)
chilla_we sum      # Output: 8
```

### Default Parameters
```jatti
kaam greet(name, greeting="Hello")
    chilla_we greeting hor ", " hor name
ja_we

greet("Singh")           # Output: Hello, Singh
greet("Singh", "Hi")     # Output: Hi, Singh
```

### Multiple Return Values
```jatti
kaam get_coordinates()
    wapas_kar 10, 20
ja_we

chal_oye x, y ban get_coordinates()
```

### Lambda Functions
```jatti
chal_oye square ban lambda(x) x * x
chilla_we square(5)        # Output: 25

# With multiple arguments
chal_oye * ban lambda(a, b) a * b
chilla_we *(3, 4)   # Output: 12
```

### Recursion
```jatti
kaam factorial(n)
    je n barabar 1
        wapas_kar 1
    nahin_taan
        wapas_kar n * factorial(n - 1)
ja_we

chilla_we factorial(5)     # Output: 120
```

---

## Built-in Functions

### String Functions
```jatti
kinna_lamba("hello")              # 5 (length)
```

### List Functions
```jatti
chal_oye numbers ban [3, 1, 4, 1, 5]

kinna_lamba(numbers)              # 5 (length)
sort_hoja_oye(numbers)            # Sorts list
ulta_hoja_oye(numbers)            # Reverses list
jod_oye(numbers)                  # 14 (sum)
average_kad(numbers)              # 2.8 (average)
sabton_vaddha(numbers)            # 5 (max)
sabton_nikka(numbers)             # 1 (min)
```

### Dictionary Functions
```jatti
chal_oye person ban {naam: "Singh", age: 25}

kinna_lamba(person)               # 2 (number of keys)
person.get_keys()                 # ["naam", "age"]
person.get_values()               # ["Singh", 25]
```

### Type Conversion
```jatti
chal_oye num_str ban "42"
chal_oye num ban int(num_str)     # 42

chal_oye float_str ban "3.14"
chal_oye pi ban float(float_str)  # 3.14

chal_oye str_num ban str(42)      # "42"
```

### Range
```jatti
range(5)           # 0, 1, 2, 3, 4
range(1, 5)        # 1, 2, 3, 4
range(1, 10, 2)    # 1, 3, 5, 7, 9
```

---

## String Methods

```jatti
chal_oye text ban "Hello World"

text.upper_case_oye()             # "HELLO WORLD"
text.lower_case_oye()             # "hello world"
text.tut_ja_oye(" ")              # ["Hello", "World"]
text.badal_ja_oye("World", "Jatti") # "Hello Jatti"
text.haiga_hai("World")           # sach (sach)
text.shuru_hunda_hai("Hello")     # sach (sach)
text.khatam_hunda_hai("World")    # sach (sach)
text.trim_hoja_oye()              # "Hello World"
```

---

## Collections

### List Operations
```jatti
chal_oye nums ban [1, 2, 3]

# Add element
nums.append(4)                    # [1, 2, 3, 4]

# Insert at position
nums.insert(1, 99)                # [1, 99, 2, 3, 4]

# Check if exists
nums.contains(99)                 # sach

# Find index
nums.index_of(2)                  # 1 (0-based)

# fuddu_chizove element
nums.fuddu_chizove(99)                   # [1, 2, 3, 4]

# Get and fuddu_chizove last
chal_oye last ban nums.pop()      # 4, nums = [1, 2, 3]
```

### List Comprehension
```jatti
# Simple
chal_oye squares ban [x * x har_ek x [1, 2, 3, 4, 5]]
# Result: [1, 4, 9, 16, 25]

# With condition
chal_oye evens ban [x har_ek x [1, 2, 3, 4, 5] je x % 2 barabar 0]
# Result: [2, 4]

# With expression
chal_oye doubled ban [x * 2 har_ek x range(1, 6)]
# Result: [2, 4, 6, 8, 10]
```

### Dictionary Comprehension
```jatti
chal_oye mapping ban {x: x*2 har_ek x range(1, 5)}
# Result: {1: 2, 2: 4, 3: 6, 4: 8}
```

---

## Error Handling

### chal_koshish_karle/Catch
```jatti
chal_koshish_karle
    chal_oye result ban 10 / 0
pakad error
    chilla_we "Error: " hor error
ja_we
```

### Raise Exception
```jatti
kaam validate_age(age)
    je age nikka_hai 0
        throw "Age cannot be negative"
    nahin_taan
        chilla_we "Age is valid"
ja_we
```

### Error Types
```jatti
chal_koshish_karle
    chal_oye value ban numbers[100]  # IndexError
pakad error
    chilla_we error
ja_we

chal_koshish_karle
    chal_oye x ban undefined_var     # NameError
pakad error
    chilla_we error
ja_we

chal_koshish_karle
    chal_oye result ban "text" / 5   # TypeError
pakad error
    chilla_we error
ja_we
```

---

## Advanced Features

### Global Variables
```jatti
chal_oye global_var ban "global"

kaam modify_global()
    global global_var
    chal_oye global_var ban "modified"
ja_we

modify_global()
chilla_we global_var    # Output: modified
```

### Variable Unpacking
```jatti
chal_oye a, b, c ban [1, 2, 3]
chilla_we a            # 1
chilla_we b            # 2
chilla_we c            # 3

chal_oye x, y ban (10, 20)
```

### Ternary Expressions
```jatti
chal_oye status ban "Active" je user_logged_in sach khaali "Inactive"
```

### Multiple Assignments
```jatti
chal_oye x, y ban 5, 10
chal_oye a, b, c ban 1, 2, 3
```

---

## Standard Library

### Importing Python Libraries
```jatti
python_le_aa "math" thon sqrt, sin, cos, pi
chal_oye root ban sqrt(16)         # 4.0

python_le_aa "random" thon randint
chal_oye dice ban randint(1, 6)
```

### Common Imports
```jatti
# Math library
python_le_aa "math" thon sqrt, floor, ceil, pi, sin, cos, tan

# Random library
python_le_aa "random" thon randint, random, choice

# Time library
python_le_aa "time" thon time, sleep

# Operating system
python_le_aa "os" thon getcwd, listdir, mkdir
```

---

## CLI Tools

### jatti run
Execute a Jatti program:
```bash
jatti run program.jatti
jatti run program.jatti --debug    # With debug trace
```

### jatti build
Compile to Python:
```bash
jatti build program.jatti          # Creates program.py
jatti build program.jatti -o out.py
```

### jatti format
Format code:
```bash
jatti format program.jatti         # Display formatted code
jatti format program.jatti -i      # Format in-place
```

---

## Keywords Reference

| Jatti | English | Purpose |
|-------|---------|---------|
| `sun_we` | program start | Mark program beginning |
| `ja_we` | program end | Mark program ending |
| `chal_oye` | let/var | Variable assignment |
| `ban` | equals/assign | Assignment operator |
| `chilla_we` | print | Output to console |
| `kaam` | function | Define function |
| `wapas_kar` | return | Return from function |
| `je` | if | Conditional statement |
| `nahin_taan_je` | elif | Else if |
| `nahin_taan` | else | Else clause |
| `jadon_tak` | while | While loop |
| `har_ek` | for | For loop |
| `roko_oye_roko` | roko_oye_roko | Exit loop |
| `chalo_oye_chalo` | chalo_oye_chalo | Skip iteration |
| `chal_koshish_karle` | chal_koshish_karle | Start exception block |
| `pakad` | catch | Catch exception |
| `throw` | raise/throw | Raise exception |
| `global` | global | Access global variable |
| `lambda` | lambda | Lambda function |
| `sach` | sach | Boolean sach |
| `khaali` | jhoot/empty | Boolean jhoot |

---

## Operators Reference

| Operator | Name | Example |
|----------|------|---------|
| `+` | Addition | `5 + 3` → 8 |
| `-` | Subtraction | `5 - 3` → 2 |
| `*` | Multiplication | `5 * 3` → 15 |
| `/` | Division | `10 / 2` → 5 |
| `%` | Modulo | `10 % 3` → 1 |
| `**` | Power | `2 ** 3` → 8 |
| `=` | Assignment | `x = 5` |
| `==` | Equal | `5 == 5` → sach |
| `!=` | Not equal | `5 != 3` → sach |
| `<` | Less than | `3 < 5` → sach |
| `>` | Greater than | `5 > 3` → sach |
| `<=` | Less or equal | `5 <= 5` → sach |
| `>=` | Greater or equal | `5 >= 3` → sach |
| `and` / `ate` | Logical AND | `sach ate sach` → sach |
| `or` / `hor` | Logical OR | `sach hor khaali` → sach |
| `not` / `nahi` | Logical NOT | `nahi sach` → khaali |

---

## Error Messages

When something goes wrong, you'll see helpful error messages:

```
SyntaxError: Unknown keyword 'chhala' on line 5
Did you mean 'chal_oye'?

NameError: Variable 'username' is not defined on line 12
Available variables: name, age, city

TypeError: Cannot / string by number
Line 8: chal_oye result ban "hello" / 5
                                    ^ error here

IndexError: List index 10 out of range (list size: 5)
Line 15: chilla_we numbers[10]
                      ^ error here

ZeroDivisionError: Cannot / by zero
Line 7: chal_oye result ban 10 / 0
                                ^ error here
```

---

## Version History

### v0.4.0 (Current)
- ✅ Complete CLI tooling (run, build, format)
- ✅ Enhanced error handling and debugging
- ✅ All Phase 3 advanced features
- ✅ Windows/Linux/Mac compatibility

### v0.3.0
- ✅ Advanced operators (%, **)
- ✅ Dictionary/Tuple/Range support
- ✅ List/Dict comprehensions
- ✅ Global keyword

### v0.2.0
- ✅ Standard library functions
- ✅ String methods
- ✅ List operations
- ✅ Error handling (chal_koshish_karle/catch)

### v0.1.0
- ✅ Core syntax and keywords
- ✅ Variables and functions
- ✅ Control flow (if/while/for)
- ✅ Basic operators

---

## Summary

Jatti is a complete, production-ready programming language with:

✅ Simple, readable Punjabi-inspired syntax  
✅ Dynamic typing with type coercion  
✅ Comprehensive built-in functions  
✅ Exception handling and debugging  
✅ Python library compatibility  
✅ Professional CLI tooling  
✅ Detailed error messages  

**Ready to build real programs!** 🚀
