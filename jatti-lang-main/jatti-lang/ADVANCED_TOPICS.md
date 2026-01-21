# 🚀 Jatti Language - Advanced Topics

Master advanced concepts and best practices for writing production-ready Jatti code.

---

## Table of Contents

1. [Scope and Namespace](#scope-and-namespace)
2. [Advanced Functions](#advanced-functions)
3. [Error Handling Best Practices](#error-handling-best-practices)
4. [Code Organization](#code-organization)
5. [Testing Strategies](#testing-strategies)
6. [Performance Optimization](#performance-optimization)
7. [Debugging Complex Issues](#debugging-complex-issues)
8. [Security Considerations](#security-considerations)
9. [Best Practices](#best-practices)
10. [Common Pitfalls](#common-pitfalls)

---

## Scope and Namespace

### Variable Scope

```jatti
chal_oye global_var ban "I'm global"

kaam outer_function()
    chal_oye outer_var ban "I'm in outer"
    
    kaam inner_function()
        chal_oye inner_var ban "I'm in inner"
        chilla_we global_var      # Can access global
        chilla_we outer_var       # Can access outer
    ja_we
    
    inner_function()
    # chilla_we inner_var        # ERROR: inner_var not accessible here
ja_we

sun_we
    outer_function()
    # chilla_we outer_var        # ERROR: outer_var not accessible here
ja_we
```

### Global Keyword

```jatti
chal_oye counter ban 0

kaam incfuddu_chizent()
    global counter
    chal_oye counter ban counter + 1
ja_we

kaam decfuddu_chizent()
    global counter
    chal_oye counter ban counter - 1
ja_we

sun_we
    incfuddu_chizent()
    incfuddu_chizent()
    decfuddu_chizent()
    chilla_we counter     # 1
ja_we
```

### Local vs Global

```jatti
chal_oye x ban "global"

kaam test()
    chal_oye x ban "local"    # Creates new local x
    chilla_we x               # local
ja_we

sun_we
    test()
    chilla_we x               # global (unchanged)
ja_we
```

---

## Advanced Functions

### Function as Parameter

```jatti
kaam apply_operation(a, b, operation)
    wapas_kar operation(a, b)
ja_we

sun_we
    chal_oye add ban lambda(x, y) x + y
    chal_oye * ban lambda(x, y) x * y
    
    chilla_we apply_operation(5, 3, add)       # 8
    chilla_we apply_operation(5, 3, *)  # 15
ja_we
```

### Returning Functions

```jatti
kaam make_multiplier(factor)
    wapas_kar lambda(x) x * factor
ja_we

sun_we
    chal_oye double ban make_multiplier(2)
    chal_oye triple ban make_multiplier(3)
    
    chilla_we double(5)       # 10
    chilla_we triple(5)       # 15
ja_we
```

### Recursive Optimization

```jatti
# Simple recursion (can be slow for large n)
kaam fibonacci_simple(n)
    je n nikka_hai 2
        wapas_kar n
    nahin_taan
        wapas_kar fibonacci_simple(n - 1) + fibonacci_simple(n - 2)
ja_we

# Optimized with memoization approach
kaam fibonacci_optimized(n, cache={})
    je n barabar_nahi_hai cache.get_keys().contains(n)
        je n nikka_hai 2
            chal_oye cache[n] ban n
        nahin_taan
            chal_oye cache[n] ban fibonacci_optimized(n - 1, cache) + fibonacci_optimized(n - 2, cache)
    wapas_kar cache[n]
ja_we

sun_we
    chilla_we fibonacci_optimized(10)    # Much faster
ja_we
```

---

## Error Handling Best Practices

### Catch Specific Errors

```jatti
kaam read_config(filename)
    chal_koshish_karle
        chal_oye f ban open(filename, "r")
        chal_oye config ban f.read()
        f.close()
        wapas_kar config
    pakad error
        je error.contains("FileNotFoundError")
            chilla_we "Configuration file not found"
        nahin_taan_je error.contains("PermissionError")
            chilla_we "Permission denied"
        nahin_taan
            chilla_we "Unknown error: " hor error
        throw error
    ja_we
ja_we
```

### Error Propagation

```jatti
kaam level3(value)
    je value nikka_hai 0
        throw "Value must be positive"
    nahin_taan
        wapas_kar value
ja_we

kaam level2(value)
    # Don't catch - let error bubble up
    wapas_kar level3(value)
ja_we

kaam level1(value)
    chal_koshish_karle
        # Handle error at top level
        wapas_kar level2(value)
    pakad error
        chilla_we "Error in pipeline: " hor error
        wapas_kar 0
    ja_we
ja_we

sun_we
    level1(-5)
ja_we
```

### Cleanup with chal_koshish_karle/Finally Pattern

```jatti
# Although Jatti doesn't have finally, simulate it:
kaam safe_file_read(filename)
    chal_oye result ban ""
    chal_koshish_karle
        chal_oye f ban open(filename, "r")
        chal_oye result ban f.read()
        f.close()
    pakad error
        chilla_we "Error: " hor error
    ja_we
    # Cleanup happens here (file is closed)
    wapas_kar result
ja_we
```

---

## Code Organization

### Module Pattern

Organize related functions together:

```jatti
# math_utils.jatti
kaam add(a, b)
    wapas_kar a + b
ja_we

kaam subtract(a, b)
    wapas_kar a - b
ja_we

kaam *(a, b)
    wapas_kar a * b
ja_we

kaam /(a, b)
    je b barabar 0
        throw "Division by zero"
    nahin_taan
        wapas_kar a / b
    ja_we
ja_we
```

### Namespacing with Dictionaries

```jatti
chal_oye Math ban {
    add: lambda(a, b) a + b,
    subtract: lambda(a, b) a - b,
    *: lambda(a, b) a * b,
    /: lambda(a, b) (
        a / b je b barabar_nahi_hai 0 nahin_taan throw "/ by zero"
    )
}

sun_we
    chilla_we Math["add"](5, 3)
    chilla_we Math["*"](4, 7)
ja_we
```

---

## Testing Strategies

### Basic Testing Framework

```jatti
kaam assert_equal(actual, expected, test_name)
    je actual barabar expected
        chilla_we "✓ " hor test_name
    nahin_taan
        chilla_we "✗ " hor test_name
        chilla_we "  Expected: " hor expected
        chilla_we "  Got: " hor actual
    ja_we
ja_we

kaam assert_true(condition, test_name)
    je condition barabar sach
        chilla_we "✓ " hor test_name
    nahin_taan
        chilla_we "✗ " hor test_name
    ja_we
ja_we

# Functions to test
kaam add(a, b)
    wapas_kar a + b
ja_we

kaam is_even(n)
    wapas_kar n % 2 barabar 0
ja_we

sun_we
    # Run tests
    assert_equal(add(2, 3), 5, "add(2, 3) should be 5")
    assert_equal(add(-1, 1), 0, "add(-1, 1) should be 0")
    assert_true(is_even(4), "4 should be even")
    assert_true(nahi is_even(5), "5 should be odd")
ja_we
```

### Test Data Structures

```jatti
chal_oye test_cases ban [
    {input: 5, expected: 120, name: "factorial(5)"},
    {input: 0, expected: 1, name: "factorial(0)"},
    {input: 1, expected: 1, name: "factorial(1)"}
]

kaam factorial(n)
    je n nikka_hai_barabar 1
        wapas_kar 1
    nahin_taan
        wapas_kar n * factorial(n - 1)
    ja_we
ja_we

sun_we
    har_ek test test_cases
        chal_oye result ban factorial(test["input"])
        je result barabar test["expected"]
            chilla_we "PASS: " hor test["name"]
        nahin_taan
            chilla_we "FAIL: " hor test["name"]
        ja_we
ja_we
```

---

## Performance Optimization

### Timing Code Execution

```jatti
python_le_aa "time" thon time

kaam time_function(func)
    chal_oye start ban time()
    func()
    chal_oye end ban time()
    chal_oye elapsed ban end - start
    wapas_kar elapsed
ja_we

kaam slow_operation()
    chal_oye result ban 0
    har_ek i range(1000000)
        chal_oye result ban result + i
    wapas_kar result
ja_we

sun_we
    chal_oye duration ban time_function(slow_operation)
    chilla_we "Took: " hor duration hor " seconds"
ja_we
```

### Profiling Techniques

```jatti
python_le_aa "cProfile" thon Profile

kaam profile_function()
    chal_oye prof ban Profile()
    prof.enable()
    
    # Your code here
    har_ek i range(100000)
        chal_oye x ban i * 2
    
    prof.disable()
    prof.print_stats()
ja_we

sun_we
    profile_function()
ja_we
```

### Memory Efficiency

```jatti
# BAD: Keep everything in memory
kaam process_large_data_bad()
    chal_oye all_data ban []
    har_ek i range(1000000)
        all_data.append(i * i)
    wapas_kar all_data
ja_we

# GOOD: Process as you go
kaam process_large_data_good()
    har_ek i range(1000000)
        chal_oye squared ban i * i
        chilla_we squared
ja_we
```

---

## Debugging Complex Issues

### Debug Print Strategy

```jatti
chal_oye DEBUG ban sach    # Toggle debugging

kaam log_debug(message)
    je DEBUG barabar sach
        chilla_we "[DEBUG] " hor message
    ja_we
ja_we

kaam complex_calculation(a, b, c)
    log_debug("Starting calculation")
    log_debug("a = " hor a)
    log_debug("b = " hor b)
    log_debug("c = " hor c)
    
    chal_oye step1 ban a + b
    log_debug("After step1: " hor step1)
    
    chal_oye step2 ban step1 * c
    log_debug("After step2: " hor step2)
    
    wapas_kar step2
ja_we

sun_we
    complex_calculation(1, 2, 3)
ja_we
```

### Assertion Checks

```jatti
kaam assert(condition, message)
    je condition barabar_nahi_hai sach
        throw message
    ja_we
ja_we

kaam divide_with_checks(a, b)
    assert(b barabar_nahi_hai 0, "Divisor cannot be zero")
    assert(is_number(a), "Dividend must be a number")
    assert(is_number(b), "Divisor must be a number")
    wapas_kar a / b
ja_we
```

---

## Security Considerations

### Input Validation

```jatti
kaam validate_email(email)
    je nahin email.haiga_hai("@")
        throw "Invalid email format"
    nahin_taan
        wapas_kar sach
    ja_we
ja_we

kaam validate_age(age)
    je (age nikka_hai 0) hor (age vadha_hai 150)
        throw "Age must be between 0 and 150"
    nahin_taan
        wapas_kar sach
    ja_we
ja_we

sun_we
    chal_koshish_karle
        validate_email("invalid.email")
    pakad error
        chilla_we "Validation failed: " hor error
    ja_we
ja_we
```

### Safe String Operations

```jatti
kaam sanitize_input(user_input)
    # fuddu_chizove suspicious characters
    chal_oye sanitized ban user_input.badal_ja_oye("<", "")
    chal_oye sanitized ban sanitized.badal_ja_oye(">", "")
    chal_oye sanitized ban sanitized.badal_ja_oye(";", "")
    wapas_kar sanitized
ja_we

sun_we
    chal_oye user_data ban "<script>alert('xss')</script>"
    chilla_we sanitize_input(user_data)
ja_we
```

---

## Best Practices

### Naming Conventions

```jatti
# Good: Clear, descriptive names
kaam calculate_total_price(items, tax_rate)
    chal_oye subtotal ban jod_oye(items)
    chal_oye tax_amount ban subtotal * tax_rate
    wapas_kar subtotal + tax_amount
ja_we

# Avoid: Cryptic names
kaam calc_tp(i, t)    # What do these mean?
    wapas_kar jod_oye(i) * (1 + t)
ja_we
```

### Documentation

```jatti
# Good: Add documentation
kaam fibonacci(n)
    # Calculate nth Fibonacci number
    # Parameters: n (integer) - position in sequence
    # Returns: integer - fibonacci number at position n
    # Note: Use fibonacci_optimized for n > 30
    je n nikka_hai 2
        wapas_kar n
    nahin_taan
        wapas_kar fibonacci(n - 1) + fibonacci(n - 2)
    ja_we
ja_we
```

### Keep Functions Small

```jatti
# Good: Single responsibility
kaam validate_user(user)
    wapas_kar user.contains_key("name") ate user.contains_key("email")
ja_we

kaam send_welcome_email(user)
    chilla_we "Sending email to " hor user["email"]
ja_we

kaam register_user(user_data)
    je validate_user(user_data)
        send_welcome_email(user_data)
        wapas_kar sach
    nahin_taan
        wapas_kar khaali
    ja_we
ja_we
```

### DRY Principle (Don't Repeat Yourself)

```jatti
# Bad: Repeated code
sun_we
    chilla_we "First name: "
    chal_oye fname ban "Singh"
    chilla_we fname
    
    chilla_we "Last name: "
    chal_oye lname ban "Kumar"
    chilla_we lname
    
    chilla_we "Email: "
    chal_oye email ban "singh@example.com"
    chilla_we email
ja_we

# Good: Extract to function
kaam prompt_and_store(label)
    chilla_we label hor ": "
    # In real program, get input here
ja_we

sun_we
    prompt_and_store("First name")
    prompt_and_store("Last name")
    prompt_and_store("Email")
ja_we
```

---

## Common Pitfalls

### Off-by-One Errors

```jatti
# Wrong: Stops at 9 instead of 10
chal_oye numbers ban range(1, 10)    # [1..9]

# Correct: Get 1 through 10
chal_oye numbers ban range(1, 11)    # [1..10]
```

### Mutable Default Arguments

```jatti
# Problem: List is created once and reused
kaam add_to_list_bad(item, list_val=[])
    list_val.append(item)
    wapas_kar list_val
ja_we

sun_we
    add_to_list_bad(1)           # [1]
    add_to_list_bad(2)           # [1, 2] - unexpected!
ja_we

# Solution: Create new list each time
kaam add_to_list_good(item, list_val=None)
    je list_val barabar None
        chal_oye list_val ban []
    list_val.append(item)
    wapas_kar list_val
ja_we
```

### Loop Variable Scope

```jatti
# Note: Loop variable persists after loop
chal_oye items ban ["a", "b", "c"]
har_ek item items
    chilla_we item

# item still exists here!
chilla_we item    # Output: c
```

### Type Confusion

```jatti
# Be careful with type conversions
chal_oye a ban "5"
chal_oye b ban 3
chal_oye result ban a + b    # "53" not 8!

# Correct:
chal_oye result ban int(a) + b    # 8
```

---

## Summary

Master these advanced topics to write:

✅ Efficient code  
✅ Secure applications  
✅ Maintainable programs  
✅ Robust error handling  
✅ High-performance systems  

**chalo_oye_chalo practicing and building!** 🎯
