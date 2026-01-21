# 📚 Jatti Language - Intermediate Guide

This guide covers advanced features for developers ready to build more complex programs.

---

## Table of Contents

1. [List Comprehensions](#list-comprehensions)
2. [Dictionary Comprehensions](#dictionary-comprehensions)
3. [Lambda Functions](#lambda-functions)
4. [Advanced Control Flow](#advanced-control-flow)
5. [Working with Ranges](#working-with-ranges)
6. [File Operations](#file-operations)
7. [Python Library Integration](#python-library-integration)
8. [Debugging Techniques](#debugging-techniques)
9. [Performance Tips](#performance-tips)
10. [Common Patterns](#common-patterns)

---

## List Comprehensions

Generate lists efficiently:

### Basic Comprehension

```jatti
# Create list of squares
chal_oye squares ban [x * x har_ek x [1, 2, 3, 4, 5]]
chilla_we squares     # [1, 4, 9, 16, 25]
```

### With Conditions

```jatti
# Get only even numbers
chal_oye numbers ban [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
chal_oye evens ban [x har_ek x numbers je x % 2 barabar 0]
chilla_we evens       # [2, 4, 6, 8, 10]

# Get numbers greater than 5
chal_oye big_nums ban [x har_ek x numbers je x vadha_hai 5]
chilla_we big_nums    # [6, 7, 8, 9, 10]
```

### With Transformations

```jatti
# Double and filter
chal_oye doubled_evens ban [x * 2 har_ek x numbers je x % 2 barabar 0]
chilla_we doubled_evens    # [4, 8, 12, 16, 20]

# Convert strings to uppercase
chal_oye words ban ["hello", "world", "jatti"]
chal_oye upper_words ban [w.upper_case_oye() har_ek w words]
chilla_we upper_words      # ["HELLO", "WORLD", "JATTI"]
```

### Nested Comprehensions

```jatti
# Create multiplication table
chal_oye table ban [x * y har_ek x range(1, 4) har_ek y range(1, 4)]
chilla_we table    # [1, 2, 3, 2, 4, 6, 3, 6, 9]

# Flatten nested lists
chal_oye matrix ban [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
chal_oye flat ban [num har_ek row matrix har_ek num row]
chilla_we flat     # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## Dictionary Comprehensions

Generate dictionaries efficiently:

### Basic Dictionary Comprehension

```jatti
# Create number-to-square mapping
chal_oye squares_dict ban {x: x*x har_ek x range(1, 6)}
chilla_we squares_dict    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### From Lists

```jatti
# Create word-to-length mapping
chal_oye words ban ["apple", "banana", "cherry"]
chal_oye word_lengths ban {w: kinna_lamba(w) har_ek w words}
chilla_we word_lengths    # {apple: 5, banana: 6, cherry: 6}
```

### With Conditions

```jatti
# Only include even squares
chal_oye numbers ban range(1, 11)
chal_oye even_squares ban {x: x*x har_ek x numbers je x % 2 barabar 0}
chilla_we even_squares    # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}
```

---

## Lambda Functions

Anonymous functions for quick operations:

### Basic Lambdas

```jatti
# Simple function
chal_oye square ban lambda(x) x * x
chilla_we square(5)       # 25

# Multiple parameters
chal_oye add ban lambda(a, b) a + b
chilla_we add(3, 4)       # 7

# String operations
chal_oye reverse_str ban lambda(s) s[::-1]
chilla_we reverse_str("hello")    # "olleh"
```

### Using with Built-in Functions

```jatti
# Though Jatti has limited functional features, lambdas work with comprehensions
chal_oye double_nums ban [(lambda(x) x * 2)(n) har_ek n [1, 2, 3, 4]]
chilla_we double_nums     # [2, 4, 6, 8]
```

---

## Advanced Control Flow

### Multiple Return Values

```jatti
kaam get_user_info()
    wapas_kar "Singh", 25, "punjab@email.com"
ja_we

sun_we
    chal_oye name, age, email ban get_user_info()
    chilla_we name        # Singh
    chilla_we age         # 25
    chilla_we email       # punjab@email.com
ja_we
```

### Tuple Unpacking in Loops

```jatti
sun_we
    chal_oye pairs ban [(1, 2), (3, 4), (5, 6)]
    
    har_ek a, b pairs
        chilla_we a hor " + " hor b hor " = " hor (a + b)
ja_we
```

**Output:**
```
1 + 2 = 3
3 + 4 = 7
5 + 6 = 11
```

### Dictionary Iteration

```jatti
sun_we
    chal_oye person ban {
        naam: "Singh",
        age: 25,
        city: "Punjab"
    }
    
    # Iterate over key-value pairs
    har_ek key, value person
        chilla_we key hor ": " hor value
ja_we
```

---

## Working with Ranges

### Range Variations

```jatti
sun_we
    # 0 to 9
    har_ek i range(10)
        chilla_we i
ja_we

sun_we
    # 1 to 9 (start, stop)
    har_ek i range(1, 10)
        chilla_we i
ja_we

sun_we
    # 1, 3, 5, 7, 9 (start, stop, step)
    har_ek i range(1, 10, 2)
        chilla_we i
ja_we

sun_we
    # Countdown: 10, 9, 8, 7, 6, 5
    har_ek i range(10, 4, -1)
        chilla_we i
ja_we
```

### Range in List Comprehensions

```jatti
# First 10 squares
chal_oye squares ban [x * x har_ek x range(1, 11)]

# Fibonacci-like sequence
chal_oye fib ban [i har_ek i range(1, 100, 1)]
```

---

## File Operations

### Reading Files

```jatti
python_le_aa "os" thon path

kaam read_file(filename)
    chal_koshish_karle
        chal_oye f ban open(filename, "r")
        chal_oye content ban f.read()
        f.close()
        wapas_kar content
    pakad error
        chilla_we "Error reading file: " hor error
        wapas_kar ""
    ja_we
ja_we

sun_we
    chal_oye content ban read_file("data.txt")
    chilla_we content
ja_we
```

### Writing Files

```jatti
kaam write_file(filename, content)
    chal_koshish_karle
        chal_oye f ban open(filename, "w")
        f.write(content)
        f.close()
        chilla_we "File written successfully"
    pakad error
        chilla_we "Error: " hor error
    ja_we
ja_we

sun_we
    write_file("output.txt", "Hello, Jatti!")
ja_we
```

### File Operations

```jatti
python_le_aa "os" thon listdir, path

sun_we
    # List files in directory
    chal_oye files ban listdir(".")
    har_ek f files
        chilla_we f
ja_we
```

---

## Python Library Integration

### Math Operations

```jatti
python_le_aa "math" thon sqrt, sin, cos, pi, floor, ceil

sun_we
    chilla_we sqrt(16)         # 4.0
    chilla_we sin(pi / 2)      # 1.0
    chilla_we floor(3.7)       # 3
    chilla_we ceil(3.2)        # 4
ja_we
```

### Random Numbers

```jatti
python_le_aa "random" thon randint, random, choice, shuffle

sun_we
    # Random integer 1-10
    chilla_we randint(1, 10)
    
    # Random float 0-1
    chilla_we random()
    
    # Random choice from list
    chal_oye colors ban ["red", "green", "blue"]
    chilla_we choice(colors)
ja_we
```

### Date and Time

```jatti
python_le_aa "datetime" thon datetime

sun_we
    chal_oye now ban datetime.now()
    chilla_we now
ja_we
```

### JSON Operations

```jatti
python_le_aa "json" thon dumps, loads

sun_we
    chal_oye data ban {
        naam: "Singh",
        age: 25,
        hobbies: ["reading", "coding"]
    }
    
    # Convert to JSON string
    chal_oye json_str ban dumps(data)
    chilla_we json_str
    
    # Parse JSON string
    chal_oye parsed ban loads(json_str)
    chilla_we parsed["naam"]
ja_we
```

---

## Debugging Techniques

### Using Debug Mode

```bash
# Run with debug trace
jatti run program.jatti --debug
```

Shows each line executed with line numbers and variable values.

### Print Debugging

```jatti
kaam calculate_total(items, tax_rate)
    chal_oye subtotal ban jod_oye(items)
    chilla_we "DEBUG: subtotal = " hor subtotal
    
    chal_oye tax ban subtotal * tax_rate
    chilla_we "DEBUG: tax = " hor tax
    
    wapas_kar subtotal + tax
ja_we

sun_we
    chal_oye amounts ban [100, 200, 150]
    chal_oye total ban calculate_total(amounts, 0.10)
    chilla_we "Total: " hor total
ja_we
```

### chal_koshish_karle/Catch for Testing

```jatti
sun_we
    chal_koshish_karle
        # Test division by zero
        chal_oye result ban 10 / 0
    pakad error
        chilla_we "Caught: " hor error
    ja_we
ja_we
```

### Assertion-like Checks

```jatti
kaam validate_age(age)
    je (age nikka_hai 0) hor (age vadha_hai 150)
        throw "Invalid age: " hor age
    nahin_taan
        chilla_we "Age is valid"
ja_we

sun_we
    chal_koshish_karle
        validate_age(-5)
    pakad error
        chilla_we "Error: " hor error
    ja_we
ja_we
```

---

## Performance Tips

### Avoid Redundant Calculations

```jatti
# BAD: Recalculate inside loop
kaam bad_example()
    har_ek i range(1000000)
        chilla_we kinna_lamba([1, 2, 3, 4, 5])
ja_we

# GOOD: Calculate once, reuse
kaam good_example()
    chal_oye list_length ban kinna_lamba([1, 2, 3, 4, 5])
    har_ek i range(1000000)
        chilla_we list_length
ja_we
```

### Use List Comprehensions

```jatti
# BAD: Multiple append calls
chal_oye result ban []
har_ek x range(1000)
    result.append(x * 2)

# GOOD: List comprehension (faster)
chal_oye result ban [x * 2 har_ek x range(1000)]
```

### Avoid Deep Nesting

```jatti
# BAD: Deeply nested loops
har_ek i range(100)
    har_ek j range(100)
        har_ek k range(100)
            chilla_we i hor j hor k

# GOOD: Flatten with list comprehension
chal_oye coords ban [i hor j hor k har_ek i range(100) har_ek j range(100) har_ek k range(100)]
```

---

## Common Patterns

### Counting Occurrences

```jatti
kaam count_occurrences(items, target)
    chal_oye count ban 0
    har_ek item items
        je item barabar target
            chal_oye count ban count + 1
    wapas_kar count
ja_we

sun_we
    chal_oye numbers ban [1, 2, 3, 2, 4, 2, 5]
    chal_oye twos ban count_occurrences(numbers, 2)
    chilla_we twos    # 3
ja_we
```

### Grouping by Value

```jatti
kaam group_by_length(words)
    chal_oye groups ban {}
    har_ek word words
        chal_oye length ban kinna_lamba(word)
        je length barabar_nahi_hai groups.get_keys().contains(length)
            chal_oye groups[length] ban []
        groups[length].append(word)
    wapas_kar groups
ja_we

sun_we
    chal_oye words ban ["a", "to", "the", "and", "go", "programming"]
    chal_oye grouped ban group_by_length(words)
    chilla_we grouped
ja_we
```

### Combining Lists

```jatti
kaam merge_lists(list1, list2)
    wapas_kar list1 + list2
ja_we

sun_we
    chal_oye a ban [1, 2, 3]
    chal_oye b ban [4, 5, 6]
    chal_oye combined ban merge_lists(a, b)
    chilla_we combined    # [1, 2, 3, 4, 5, 6]
ja_we
```

### Finding Maximum/Minimum

```jatti
kaam find_longest_word(words)
    chal_oye longest ban words[0]
    har_ek word words
        je kinna_lamba(word) vadha_hai kinna_lamba(longest)
            chal_oye longest ban word
    wapas_kar longest
ja_we

sun_we
    chal_oye words ban ["hello", "world", "jatti", "programming"]
    chilla_we find_longest_word(words)    # programming
ja_we
```

---

## Next Steps

Ready for more? Explore:

1. **Advanced Topics** - Optimization, best practices, and complex patterns
2. **Example Programs** - Real-world applications
3. **API Reference** - Complete documentation
4. **Migration Guide** - Convert Python code to Jatti

---

**Keep improving your Jatti skills!** 🚀
