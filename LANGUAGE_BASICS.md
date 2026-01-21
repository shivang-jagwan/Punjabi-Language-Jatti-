# Language Basics (Variables, Operators, Control Flow)

This is a quick reference for everyday Jatti syntax.

## Program structure

Every program starts with `sun_we` and ends with `ja_we`.

```jatti
sun_we
    chilla_we "hello"
ja_we
```

## Comments

```jatti
fuddu_chiz this is a comment
```

## Variables

Assignment uses `chal_oye <name> ban <value>`.

```jatti
sun_we
    chal_oye x ban 5
    chal_oye name ban "Jatti"
    chal_oye ok ban sach
    chal_oye none ban khaali
    chilla_we x
    chilla_we name
ja_we
```

## Numbers and strings

```jatti
sun_we
    chal_oye a ban 10
    chal_oye b ban 3
    chilla_we a + b
    chilla_we a * b
    chilla_we a / b
ja_we
```

## Comparison operators (keywords)

Use these in conditions and prints:

- `vadha_hai`  → `>`
- `nikka_hai` → `<`
- `barabar` → `==`
- `barabar_nahi_hai` → `!=`
- `vadha_ya_barabar` → `>=`
- `nikka_ya_barabar` → `<=`

Example:

```jatti
sun_we
    chal_oye x ban 5
    je x vadha_hai 3
        chilla_we "big"
    nahin_taan
        chilla_we "small"
ja_we
```

## If / else-if / else

```jatti
sun_we
    chal_oye n ban 10

    je n vadha_hai 10
        chilla_we "gt 10"
    nahin_taan_je n barabar 10
        chilla_we "eq 10"
    nahin_taan
        chilla_we "lt 10"
ja_we
```

## Loops

### While (`jadon_tak`)

```jatti
sun_we
    chal_oye i ban 1
    chal_oye total ban 0

    jadon_tak i nikka_ya_barabar 5
        chal_oye total ban total + i
        chal_oye i ban i + 1

    chilla_we total
ja_we
```

### For-each (`har_ek`)

```jatti
sun_we
    chal_oye total ban 0
    har_ek i range_banao(1, 6)
        chal_oye total ban total + i
    chilla_we total
ja_we
```

## Try / catch (`chal_koshish_karle` / `pakad`)

```jatti
sun_we
    chal_koshish_karle
        chal_oye x ban 10 / 0
    pakad err
        chilla_we err
ja_we
```

## Next reads

- Full spec: `LANGUAGE_SPECIFICATION.md`
- Beginner tutorial: `BEGINNER_TUTORIAL.md`
- Intermediate guide: `INTERMEDIATE_GUIDE.md`
