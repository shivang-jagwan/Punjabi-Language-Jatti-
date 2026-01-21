# 🎓 Jatti Language - Beginner Tutorial

Welcome to Jatti! This tutorial will teach you the basics of the language step by step.

---

## Part 1: Hello World

Every Jatti program starts with `sun_we` and ends with `ja_we`.

Create a file called `hello.jatti`:

```jatti
sun_we
    chilla_we "Hello, World!"
ja_we
```

Run it:
```bash
jatti run hello.jatti
```

**Output:**
```
Hello, World!
```

**Explanation:**
- `sun_we` = "Listen up" (program start)
- `chilla_we` = "shout/print" (output)
- `ja_we` = "that's all" (program end)
- Code inside must be indented (4 spaces)

---

## Part 2: Variables

Variables store values. Use `chal_oye` to create them:

```jatti
sun_we
    chal_oye name ban "Singh"
    chal_oye age ban 25
    chal_oye height ban 5.9
    
    chilla_we name
    chilla_we age
    chilla_we height
ja_we
```

**Output:**
```
Singh
25
5.9
```

**Explanation:**
- `chal_oye` = "Let's have" (variable declaration)
- `ban` = "is" or "equals" (assignment)
- `chilla_we` = prints the value

### Changing Variables

```jatti
sun_we
    chal_oye x ban 10
    chilla_we x         # Output: 10
    
    chal_oye x ban 20
    chilla_we x         # Output: 20
ja_we
```

### Comments

```jatti
sun_we
    # This is a comment
    chal_oye name ban "Singh"  # Comments can go here too
    chilla_we name
ja_we
```

---

## Part 3: Basic Math

```jatti
sun_we
    chal_oye a ban 10
    chal_oye b ban 5
    
    chilla_we a + b     # Output: 15 (addition)
    chilla_we a - b     # Output: 5 (subtraction)
    chilla_we a * b     # Output: 50 (multiplication)
    chilla_we a / b     # Output: 2 (division)
ja_we
```

**Output:**
```
15
5
50
2
```

### More Math

```jatti
sun_we
    chilla_we 10 % 3    # Output: 1 (fuddu_chizainder)
    chilla_we 2 ** 3    # Output: 8 (power)
ja_we
```

---

## Part 4: If Statements (Conditionals)

Make decisions based on conditions:

```jatti
sun_we
    chal_oye age ban 16
    
    je age vadha_hai 18
        chilla_we "You can vote!"
    nahin_taan
        chilla_we "Too young to vote"
ja_we
```

**Output:**
```
Too young to vote
```

**Explanation:**
- `je` = "if"
- `vadha_hai` = "is greater than" (>)
- `nahin_taan` = "else"

### Comparison Operators

```jatti
sun_we
    chal_oye score ban 85
    
    # > greater than
    je score vadha_hai 90
        chilla_we "Great!"
    
    # < less than
    je score nikka_hai 50
        chilla_we "Need to improve"
    
    # == equal
    je score barabar 85
        chilla_we "Perfect score!"
ja_we
```

### Multiple Conditions

```jatti
sun_we
    chal_oye age ban 25
    chal_oye has_license ban sach
    
    # AND condition
    je (age vadha_ya_barabar 18) ate (has_license barabar sach)
        chilla_we "You can drive!"
ja_we
```

**Explanation:**
- `ate` = "and"
- `hor` = "or"
- `nahi` = "not"

---

## Part 5: Loops - While

Repeat code until a condition is jhoot:

```jatti
sun_we
    chal_oye count ban 1
    
    jadon_tak count nikka_ya_barabar 5
        chilla_we count
        chal_oye count ban count + 1
ja_we
```

**Output:**
```
1
2
3
4
5
```

**Explanation:**
- `jadon_tak` = "while"
- `nikka_ya_barabar` = "<=" (less than or equal)

### roko_oye_roko & chalo_oye_chalo

```jatti
sun_we
    chal_oye i ban 0
    
    jadon_tak i nikka_hai 10
        je i barabar 5
            roko_oye_roko          # Exit the loop
        chilla_we i
        chal_oye i ban i + 1
ja_we
```

**Output:**
```
0
1
2
3
4
```

---

## Part 6: Loops - For

Iterate over collections:

```jatti
sun_we
    chal_oye fruits ban ["Apple", "Banana", "Cherry"]
    
    har_ek fruit fruits
        chilla_we fruit
ja_we
```

**Output:**
```
Apple
Banana
Cherry
```

**Explanation:**
- `har_ek` = "for each"
- Works with lists, tuples, dictionaries, ranges

### Using range()

```jatti
sun_we
    har_ek i range(1, 6)
        chilla_we i
ja_we
```

**Output:**
```
1
2
3
4
5
```

---

## Part 7: Lists

Store multiple values:

```jatti
sun_we
    chal_oye numbers ban [10, 20, 30, 40, 50]
    
    # Access by index
    chilla_we numbers[0]   # Output: 10
    chilla_we numbers[2]   # Output: 30
    chilla_we numbers[-1]  # Output: 50 (last element)
ja_we
```

**Index:**
```
     [10, 20, 30, 40, 50]
      0   1   2   3   4    (forward)
     -5  -4  -3  -2  -1    (backward)
```

### Modifying Lists

```jatti
sun_we
    chal_oye nums ban [1, 2, 3]
    
    nums.append(4)         # Add 4 → [1, 2, 3, 4]
    nums.insert(1, 99)     # Insert 99 at index 1 → [1, 99, 2, 3, 4]
    nums.fuddu_chizove(99)        # fuddu_chizove 99 → [1, 2, 3, 4]
    
    chilla_we nums
ja_we
```

### List Operations

```jatti
sun_we
    chal_oye items ban ["a", "b", "c"]
    
    chilla_we kinna_lamba(items)      # Output: 3 (length)
    chilla_we items.contains("b")     # Output: sach (sach)
ja_we
```

---

## Part 8: Strings

Text values:

```jatti
sun_we
    chal_oye message ban "Hello, Jatti!"
    
    chilla_we message
    chilla_we kinna_lamba(message)    # Output: 14 (length)
ja_we
```

### String Methods

```jatti
sun_we
    chal_oye text ban "Hello World"
    
    chilla_we text.upper_case_oye()        # HELLO WORLD
    chilla_we text.lower_case_oye()        # hello world
    chilla_we text.tut_ja_oye(" ")         # ["Hello", "World"]
    chilla_we text.badal_ja_oye("World", "Jatti")  # Hello Jatti
ja_we
```

### String Concatenation

```jatti
sun_we
    chal_oye first_name ban "Singh"
    chal_oye last_name ban "Kumar"
    
    chilla_we first_name hor " " hor last_name  # Output: Singh Kumar
ja_we
```

---

## Part 9: Functions

Reusable blocks of code:

```jatti
kaam greet(name)
    chilla_we "Hello, " hor name
ja_we

sun_we
    greet("Singh")
    greet("Priya")
    greet("Raj")
ja_we
```

**Output:**
```
Hello, Singh
Hello, Priya
Hello, Raj
```

**Explanation:**
- `kaam` = "function"
- Functions must be defined before `sun_we`
- Parameters are in parentheses

### Functions with Return

```jatti
kaam add(a, b)
    chal_oye result ban a + b
    wapas_kar result
ja_we

sun_we
    chal_oye sum ban add(5, 3)
    chilla_we sum       # Output: 8
ja_we
```

**Explanation:**
- `wapas_kar` = "return"

### Default Parameters

```jatti
kaam greet(name, greeting="Hi")
    chilla_we greeting hor ", " hor name
ja_we

sun_we
    greet("Singh")              # Output: Hi, Singh
    greet("Singh", "Hello")     # Output: Hello, Singh
ja_we
```

---

## Part 10: Error Handling

Handle problems gracefully:

```jatti
sun_we
    chal_koshish_karle
        chal_oye numbers ban [1, 2, 3]
        chilla_we numbers[10]   # Error! Index out of range
    pakad error
        chilla_we "Error: " hor error
    ja_we
ja_we
```

**Output:**
```
Error: list index out of range
```

**Explanation:**
- `chal_koshish_karle` = start protected code block
- `pakad` = "catch" exception
- `ja_we` = end error handling block

### Common Errors

```jatti
sun_we
    # Division by zero
    chal_koshish_karle
        chal_oye x ban 10 / 0
    pakad error
        chilla_we "Cannot / by zero"
    ja_we
    
    # Undefined variable
    chal_koshish_karle
        chilla_we undefined_var
    pakad error
        chilla_we "Variable not found"
    ja_we
ja_we
```

---

## Part 11: Dictionaries

Store data with labels:

```jatti
sun_we
    chal_oye person ban {
        naam: "Singh",
        age: 25,
        city: "Punjab"
    }
    
    chilla_we person["naam"]      # Output: Singh
    chilla_we person["age"]       # Output: 25
ja_we
```

### Dictionary Operations

```jatti
sun_we
    chal_oye student ban {
        naam: "Priya",
        grade: "A"
    }
    
    chilla_we kinna_lamba(student)    # Output: 2
    chilla_we student.get_keys()      # Output: ["naam", "grade"]
    chilla_we student.get_values()    # Output: ["Priya", "A"]
ja_we
```

---

## Part 12: Complete Example Program

Here's a simple program using everything you learned:

```jatti
kaam calculate_grade(score)
    je score vadha_ya_barabar 90
        wapas_kar "A"
    nahin_taan_je score vadha_ya_barabar 80
        wapas_kar "B"
    nahin_taan_je score vadha_ya_barabar 70
        wapas_kar "C"
    nahin_taan
        wapas_kar "F"
ja_we

sun_we
    chal_oye students ban {
        singh: 85,
        priya: 92,
        raj: 78,
        neha: 95
    }
    
    har_ek name, score students
        chal_oye grade ban calculate_grade(score)
        chilla_we name hor ": " hor score hor " (" hor grade hor ")"
ja_we
```

**Output:**
```
singh: 85 (B)
priya: 92 (A)
raj: 78 (C)
neha: 95 (A)
```

---

## Part 13: What's Next?

You now know the basics! chalo_oye_chalo with:

1. **Intermediate Guide** - Learn about comprehensions, lambdas, and advanced features
2. **Advanced Topics** - Explore performance tips, best practices, and debugging
3. **Example Programs** - See real-world applications
4. **API Reference** - Complete documentation of all functions and methods

---

## Cheat Sheet

```jatti
# Variables
chal_oye x ban 10

# Output
chilla_we x

# Math
+ - * / % **

# Comparison
vadha_hai (>) nikka_hai (<) barabar (==) 
barabar_nahi_hai (!=) vadha_ya_barabar (>=) nikka_ya_barabar (<=)

# Logical
ate (AND) hor (OR) nahi (NOT)

# Control Flow
je (if) nahin_taan_je (elif) nahin_taan (else)
jadon_tak (while) har_ek (for) roko_oye_roko chalo_oye_chalo

# Functions
kaam name(params) ... wapas_kar value ja_we

# Error Handling
chal_koshish_karle ... pakad error ... ja_we

# Collections
[list] {dict} (tuple)
```

---

## Tips for Learning

1. **Type out the code** - Don't just copy/paste
2. **Experiment** - Change numbers and strings, see what happens
3. **roko_oye_roko things** - Errors are how you learn
4. **Start small** - Combine simple things into complex programs
5. **Have fun** - Programming should be enjoyable!

---

**Happy Coding! 🎉**

Questions? See the Troubleshooting Guide.
