import importlib
from compiler.errors import roast_error
import compiler.state as state
from compiler.runtime import BreakSignal, ContinueSignal
from compiler.runtime import JattiException, variables, functions, python_funcs, safe_eval, process_string_escapes
from compiler.stdlib import (
    kinna_lamba, sort_hoja_oye, ulta_hoja_oye, jod_oye, average_kad,
    sabton_vaddha, sabton_nikka, dona_nu_jod_oye, range_banao
)



def syntax_error(msg):
    import compiler.state as state
    roast_error(msg, state.CURRENT_LINE)


def evaluate_expression_with_builtins(expr):
    """
    Evaluate an expression that may contain builtin function calls or variables.
    Handles builtin functions, user functions, and regular expressions.
    """
    from compiler.runtime import functions as user_functions
    
    expr_normalized = norm(expr)
    has_parens = "(" in expr and expr.endswith(")")
    fname = expr.split("(", 1)[0] if has_parens else None
    
    # Register builtin functions
    builtin_funcs = {
        'kinna_lamba': kinna_lamba,
        'sort_hoja_oye': sort_hoja_oye,
        'ulta_hoja_oye': ulta_hoja_oye,
        'jod_oye': jod_oye,
        'average_kad': average_kad,
        'sabton_vaddha': sabton_vaddha,
        'sabton_nikka': sabton_nikka,
        'dona_nu_jod_oye': dona_nu_jod_oye,
        'range_banao': range_banao,
    }
    
    if has_parens and fname in builtin_funcs:
        # Handle builtin function call
        args_str = expr[expr.find("(")+1:expr.find(")")]
        args = [safe_eval(norm(arg.strip())) for arg in args_str.split(",") if arg.strip()]
        try:
            return builtin_funcs[fname](*args)
        except Exception as e:
            roast_error(f"Built-in function error: {str(e)}", state.CURRENT_LINE)
    
    elif has_parens and fname in user_functions:
        # Handle user-defined function call
        return evaluate_with_functions(expr, norm)
    
    # Regular expression or variable
    return safe_eval(expr_normalized)


def evaluate_with_functions(expr, norm_fn):
    """
    Evaluate an expression that may contain function calls.
    Handles recursive functions by calling them directly.
    """
    # Parse for function calls: name(args) FIRST before trying safe_eval
    import re
    func_call_pattern = r'(\w+)\s*\('
    match = re.search(func_call_pattern, expr)
    
    # Check if this is a function call BEFORE trying safe_eval
    if match:
        func_name = match.group(1)
        if func_name in functions:
            # This is a user-defined function, handle it specially
            # Don't try safe_eval first, as it will fail with NameError
            pass  # Fall through to function call handling
        else:
            # Not a known function, try safe_eval
            return safe_eval(norm_fn(expr))
    else:
        # No function calls detected, just use safe_eval
        return safe_eval(norm_fn(expr))
    
    # We have a user-defined function call - replace and evaluate
    while True:
        match = re.search(r'(\w+)\s*\(([^()]*)\)', expr)
        if not match:
            break
        
        fname = match.group(1)
        args_str = match.group(2)
        
        if fname not in functions:
            break
        
        # Call the function
        args = [arg.strip() for arg in args_str.split(',')]
        params, body = functions[fname]
        
        if len(args) != len(params):
            roast_error(f"Function {fname} expects {len(params)} args, got {len(args)}", state.CURRENT_LINE)
        
        from compiler.errors import push_function, pop_function
        push_function(fname, state.CURRENT_LINE)
        
        backup = variables.copy()
        try:
            for p, a in zip(params, args):
                variables[p] = evaluate_with_functions(a, norm_fn)
            
            variables.pop("__return__", None)
            execute_block(body, 0, indent_of(body[0]), (state.CURRENT_LINE or 1) - 1)
            
            if "__return__" not in variables:
                roast_error("wapas_kar missing hai.", state.CURRENT_LINE)
            
            result = variables["__return__"]
        finally:
            # Preserve global variables
            global_values = {k: v for k, v in variables.items() if k in state.GLOBAL_VARS}
            variables.clear()
            variables.update(backup)
            # Restore any global variables that were modified
            variables.update(global_values)
            pop_function()
        
        # Replace the function call in the expression with its result
        if isinstance(result, str):
            replacement = f'"{result}"'
        else:
            replacement = str(result)
        
        expr = expr[:match.start()] + replacement + expr[match.end():]
    
    # Now evaluate the modified expression
    return safe_eval(norm_fn(expr))


# ---------------- helpers ----------------
def indent_of(line):
    prefix = line[:len(line) - len(line.lstrip())]

    if not prefix:
        return 0

    # detect indentation type
    has_space = " " in prefix
    has_tab = "\t" in prefix

    #  mixed indentation
    if has_space and has_tab:
        roast_error(
            "Tabs te spaces mix nahi kar sakde.",
            state.CURRENT_LINE
        )

    # determine indent type
    indent_type = "tab" if has_tab else "space"
    indent_width = prefix.count("\t") if has_tab else prefix.count(" ")

    # validate space indentation
    if indent_type == "space" and indent_width % 4 != 0:
        roast_error(
            "Spaces indentation 4 di multiple honi chahidi hai.",
            state.CURRENT_LINE
        )

    # set file-wide indentation style
    if state.INDENT_TYPE is None:
        state.INDENT_TYPE = indent_type
        state.INDENT_WIDTH = 1 if indent_type == "tab" else 4

    # enforce consistency
    if indent_type != state.INDENT_TYPE:
        roast_error(
            f"Indentation mix ho rahi hai. Sirf {state.INDENT_TYPE} use karo.",
            state.CURRENT_LINE
        )

    # return logical indent level
    return indent_width // state.INDENT_WIDTH



import re

def norm(expr):
    """Convert Jatti keywords to Python, protecting string literals"""
    
    # Extract and protect strings
    strings = {}
    string_placeholder = "__STRING_{}_"
    counter = 0
    
    # Find all quoted strings and replace with placeholders
    i = 0
    result = ""
    while i < len(expr):
        if expr[i] == '"':
            # Find matching closing quote
            j = i + 1
            while j < len(expr) and expr[j] != '"':
                if expr[j] == '\\':
                    j += 2  # Skip escaped character
                else:
                    j += 1
            j += 1  # Include closing quote
            
            # Store string with placeholder
            string_key = string_placeholder.format(counter)
            strings[string_key] = expr[i:j]
            result += string_key
            counter += 1
            i = j
        else:
            result += expr[i]
            i += 1
    
    expr = result
    
    # Now do replacements on protected expression
    replacements = {
        r"\bvadha_hai\b": ">",
        r"\bnikka_hai\b": "<",
        r"\bbarabar\b": "==",
        r"\bbarabar_nahi_hai\b": "!=",
        r"\bnikka_ya_barabar\b": "<=",
        r"\bvadha_ya_barabar\b": ">=",
        r"\bhor\b": "and",
        r"\bya_te\b": "or",
        r"\bnahi\b": "not",
        r"\bsach\b": "True",
        r"\bjhoot\b": "False",
        r"\bkhaali\b": "None"
    }

    for pattern, repl in replacements.items():
        expr = re.sub(pattern, repl, expr)

    if expr.startswith("mil_gaya"):
        parts = expr.split(maxsplit=2)
        if len(parts) != 3:
            roast_error("mil_gaya syntax galat hai.", state.CURRENT_LINE)
        _, container, item = parts
        expr = f"{item} in {container}"

    # Restore strings
    for string_key, string_val in strings.items():
        expr = expr.replace(string_key, string_val)

    return expr.strip()


import re

def validate_logical_syntax(stmt):
    # catches: hor hor, ya_te ya_te, hor ya_te, ya_te hor
    bad_pattern = r"\b(hor|ya_te|nahi)\s+(hor|ya_te|nahi)\b"



    if re.search(bad_pattern, stmt):
        roast_error(
            "Logical operator syntax galat hai.",
            state.CURRENT_LINE
        )


# ---------------- block executor ----------------
def execute_block(lines, start, base_indent, line_offset=0):
    import compiler.state as state

    i = start
    while i < len(lines):
        if not lines[i].strip():
            i += 1
            continue

        if indent_of(lines[i]) < base_indent:
            break

        state.CURRENT_LINE = line_offset + i + 1  # sun_we removed + 1-indexed
        
        # Debug logging
        if state.DEBUG_MODE:
            stmt = lines[i].strip()
            if stmt and not stmt.startswith("fuddu_chiz"):
                state.TRACE_EXECUTION.append(f"Line {state.CURRENT_LINE}: {stmt[:50]}")
        
        i = execute_statement(lines, i, base_indent)

    return i


# ---------------- IF / ELSE ----------------
def execute_if_chain(lines, i, base_indent):
    stmt = lines[i].strip()
    cond_raw = stmt.replace("je", "", 1).strip()
    validate_logical_syntax(cond_raw)
    # ----- je validation -----
    if stmt.strip() == "je":
        roast_error(
            "je vich condition missing hai.",
            state.CURRENT_LINE
        )
    cond = norm(cond_raw)

    j = i + 1
    matched = False

    # ----- body existence check -----
    if j >= len(lines) or indent_of(lines[j]) <= base_indent:
        roast_error(
            "je de baad indented body chahidi hai.",
            state.CURRENT_LINE
        )

    if safe_eval(cond):
        matched = True
        try:
            execute_block(
                lines, j, indent_of(lines[j]),
                (state.CURRENT_LINE or 1) - 1
            )
        except (ContinueSignal, BreakSignal):
            raise


    while j < len(lines) and indent_of(lines[j]) > base_indent:
        j += 1

    # ----- else-if / else chain -----
    while j < len(lines):
        stmt = lines[j].strip()

        # ---- else-if ----
        if stmt.startswith("nahin_taan_je"):
            if stmt.strip() == "nahin_taan_je":
                roast_error(
                    "nahin_taan_je vich condition missing hai.",
                    state.CURRENT_LINE
                )

            j += 1
            if j >= len(lines) or indent_of(lines[j]) <= base_indent:
                roast_error(
                    "nahin_taan_je de baad indented body chahidi hai.",
                    state.CURRENT_LINE
                )
            cond_raw = stmt.replace("nahin_taan_je", "", 1).strip()
            validate_logical_syntax(cond_raw)

            if not matched and safe_eval(
                norm(cond_raw)
            ):
                matched = True
                try:
                    execute_block(
                        lines, j, indent_of(lines[j]),
                        (state.CURRENT_LINE or 1) - 1
                    )
                except (ContinueSignal, BreakSignal):
                    raise

            while j < len(lines) and indent_of(lines[j]) > base_indent:
                j += 1

        # ---- else ----
        elif stmt.startswith("nahin_taan"):
            if stmt.strip() != "nahin_taan":
                roast_error(
                    "nahin_taan de baad kuch nahi aunda.",
                    state.CURRENT_LINE
                )

            j += 1
            if j >= len(lines) or indent_of(lines[j]) <= base_indent:
                roast_error(
                    "nahin_taan de baad indented body chahidi hai.",
                    state.CURRENT_LINE
                )

            if not matched:
                try:
                    execute_block(
                        lines, j, indent_of(lines[j]),
                        (state.CURRENT_LINE or 1) - 1
                    )
                except (ContinueSignal, BreakSignal):
                    raise

            while j < len(lines) and indent_of(lines[j]) > base_indent:
                j += 1
            break

        else:
            break

    return j



# ---------------- WHILE ----------------
def execute_loop(lines, i, base_indent):
    stmt = lines[i].strip()
    cond_raw = stmt.replace("jadon_tak", "", 1).strip()
    # 🔒 Logical syntax validation (ADD THIS)
    validate_logical_syntax(cond_raw)

    if stmt.strip() == "jadon_tak":
        roast_error(
            "jadon_tak vich condition missing hai.",
            state.CURRENT_LINE
        )
    cond = norm(cond_raw)
    body_start = i + 1

    if body_start >= len(lines):
        roast_error("jadon_tak body missing hai.", state.CURRENT_LINE)
    if body_start >= len(lines) or indent_of(lines[body_start]) <= base_indent:
        roast_error(
            "jadon_tak de baad indented body chahidi hai.",
            state.CURRENT_LINE
        )

    body_indent = indent_of(lines[body_start])
    body = []

    j = body_start
    while j < len(lines) and indent_of(lines[j]) >= body_indent:
        body.append(lines[j])
        j += 1

    state.LOOP_DEPTH += 1
    while safe_eval(cond):
        try:
            execute_block(body, 0, body_indent, (state.CURRENT_LINE or 1) - 1)
        except ContinueSignal:
            continue
        except BreakSignal:
            break
    state.LOOP_DEPTH -= 1


    return j


# ---------------- FOREACH (LIST + MAP) ----------------
def execute_foreach(lines, i, base_indent):
    stmt = lines[i].strip()

    header = lines[i].strip().replace("har_ek", "", 1).strip()
    
    # Find the last space that's not inside parentheses
    # This handles cases like: "i range_banao(1, 5)" correctly
    paren_depth = 0
    last_space_outside_parens = -1
    for idx, char in enumerate(header):
        if char == '(':
            paren_depth += 1
        elif char == ')':
            paren_depth -= 1
        elif char == ' ' and paren_depth == 0:
            last_space_outside_parens = idx
    
    if last_space_outside_parens == -1:
        roast_error("har_ek syntax galat hai.", state.CURRENT_LINE)
    
    vars_part = header[:last_space_outside_parens].strip()
    iterable_expr = header[last_space_outside_parens:].strip()

    
    # ✅ VALIDATE AFTER DEFINITION
    validate_logical_syntax(iterable_expr)

    # Use the helper to evaluate expressions that may contain builtin functions
    iterable = evaluate_expression_with_builtins(iterable_expr)

    body_start = i + 1
    if body_start >= len(lines) or indent_of(lines[body_start]) <= base_indent:
        roast_error(
            "har_ek de baad indented body chahidi hai.",
            state.CURRENT_LINE
        )
    body_indent = indent_of(lines[body_start])
    body = []

    j = body_start
    while j < len(lines) and (not lines[j].strip() or indent_of(lines[j]) >= body_indent):
        body.append(lines[j])
        j += 1

    # -------- LIST FOREACH --------
    if "," not in vars_part:
        var = vars_part.strip()

        if not isinstance(iterable, list):
            roast_error("har_ek x sirf list layi use hunda hai.", state.CURRENT_LINE)

        state.LOOP_DEPTH += 1
        for item in iterable:
            variables[var] = item
            try:
                execute_block(body, 0, body_indent, (state.CURRENT_LINE or 1) - 1)
            except ContinueSignal:
                continue
            except BreakSignal:
                break
        state.LOOP_DEPTH -= 1


    # -------- MAP FOREACH --------
    else:
        key_var, val_var = [v.strip() for v in vars_part.split(",")]

        if not isinstance(iterable, dict):
            roast_error("har_ek key, value sirf map layi use hunda hai.", state.CURRENT_LINE)

        state.LOOP_DEPTH += 1
        for k, v in iterable.items():
            variables[key_var] = k
            variables[val_var] = v
            try:
                execute_block(body, 0, body_indent, (state.CURRENT_LINE or 1) - 1)
            except ContinueSignal:
                continue
            except BreakSignal:
                break
        state.LOOP_DEPTH -= 1


    return j

# ---------------- TRY / PAKAD ----------------
def execute_try_pakad(lines, i, base_indent):
    state.CURRENT_LINE = (state.CURRENT_LINE or 1)

    if lines[i].strip() != "chal_koshish_karle":
        roast_error("chal_koshish_karle syntax galat hai.", state.CURRENT_LINE)

    if i + 1 >= len(lines):
        roast_error("chal_koshish_karle body missing hai.", state.CURRENT_LINE)

    try_body_start = i + 1
    if indent_of(lines[try_body_start]) <= base_indent:
        roast_error("chal_koshish_karle de baad indented body chahidi hai.", state.CURRENT_LINE)

    try_indent = indent_of(lines[try_body_start])
    try_body = []
    j = try_body_start
    while j < len(lines) and (not lines[j].strip() or indent_of(lines[j]) >= try_indent):
        try_body.append(lines[j])
        j += 1

    if j >= len(lines):
        roast_error("try de baad pakad chahida hai.", state.CURRENT_LINE)

    pakad_stmt = lines[j].strip()
    if not pakad_stmt.startswith("pakad"):
        roast_error("try de baad pakad chahida hai.", state.CURRENT_LINE)

    parts = pakad_stmt.split()
    catch_var = None

    if len(parts) == 2:
        catch_var = parts[1]
        if not catch_var.isidentifier():
            roast_error("pakad vich galat variable naam.", state.CURRENT_LINE)
    elif len(parts) > 2:
        roast_error("pakad syntax galat hai. Format: pakad <var>", state.CURRENT_LINE)
    state.CURRENT_LINE = (state.CURRENT_LINE or 1)

    pakad_body_start = j + 1
    if pakad_body_start >= len(lines) or indent_of(lines[pakad_body_start]) <= base_indent:
        roast_error("pakad de baad indented body chahidi hai.", state.CURRENT_LINE)

    pakad_indent = indent_of(lines[pakad_body_start])
    pakad_body = []
    k = pakad_body_start
    while k < len(lines) and (not lines[k].strip() or indent_of(lines[k]) >= pakad_indent):
        pakad_body.append(lines[k])
        k += 1

    state.IN_TRY += 1
    try:
        execute_block(
            try_body, 0, try_indent,
            (state.CURRENT_LINE or 1) - 1
        )
    except JattiException as e:
        if catch_var:
            variables[catch_var] = e.value
        execute_block(
            pakad_body, 0, pakad_indent,
            (state.CURRENT_LINE or 1) - 1
        )
    except Exception:
        execute_block(
            pakad_body, 0, pakad_indent,
            (state.CURRENT_LINE or 1) - 1
        )
    finally:
        state.IN_TRY -= 1

    return k



# ---------------- STATEMENTS ----------------
def execute_statement(lines, i, base_indent):
    stmt = lines[i].strip()

    if stmt == "pakad" or stmt.startswith("pakad "):
        roast_error(
            "pakad sirf try de baad allowed hai.",
            state.CURRENT_LINE
        )

    # throw
    if stmt.startswith("throw"):
        if state.IN_TRY == 0:
            roast_error(
                "throw sirf try vich allowed hai.",
                state.CURRENT_LINE
            )
        parts = stmt.split(maxsplit=1)
        if len(parts) != 2:
            roast_error("throw vich value chahidi hai.", state.CURRENT_LINE)

        value = safe_eval(norm(parts[1]))
        raise JattiException(value)



    # comment
    if stmt.startswith("fuddu_chiz"):
        return i + 1

    # python import
    if stmt.startswith("python_le_aa"):
        try:
            parts = stmt.split()
            module = parts[1].replace('"', "")
            idx = parts.index("thon")
            mod = importlib.import_module(module)
            for f in parts[idx + 1:]:
                python_funcs[f.strip(",")] = getattr(mod, f.strip(","))
        except:
            roast_error("Python import fail ho gaya.", state.CURRENT_LINE)
        return i + 1

    # input
    if stmt.startswith("das_oye"):
        parts = stmt.split(maxsplit=2)

        if len(parts) != 3:
            roast_error(
                "das_oye syntax galat hai. Format: das_oye <var> eh_chahida \"msg\"",
                state.CURRENT_LINE
            )
        _, var, rest = parts

        if not rest.startswith("eh_chahida"):
            roast_error(
                "das_oye vich 'eh_chahida' keyword chahida hai.",
                state.CURRENT_LINE
            )
        msg = rest.replace("eh_chahida", "", 1).strip()

        if not (msg.startswith('"') and msg.endswith('"')):
            roast_error(
                "Input message quotes vich hona chahida hai.",
                state.CURRENT_LINE
            )
        val = input(msg.strip('"') + ": ")

        try:
            variables[var] = int(val) if "." not in val else float(val)
        except:
            variables[var] = val

        return i + 1


    # function definition

    if stmt.startswith("kaam"):
    # ----- basic structure -----
        if "(" not in stmt or ")" not in stmt:
            roast_error(
                "kaam syntax galat hai. Format: kaam name(arg1, arg2)",
                state.CURRENT_LINE
            )

        head = stmt.split()[1]
        fname = head.split("(")[0]

        # ----- function name validation -----
        if not fname.isidentifier():
            roast_error(
                "Function naam galat hai.",
                state.CURRENT_LINE
            )
        # ----- parameter parsing -----
        param_str = stmt[stmt.find("(")+1:stmt.find(")")]
        if not param_str and "," in stmt:
            roast_error(
                "Function parameters galat hain.",
                state.CURRENT_LINE
            )
        params = [p.strip() for p in param_str.split(",") if p.strip()]

        for p in params:
            if not p.isidentifier():
                roast_error(
                    f"Function parameter galat hai: {p}",
                    state.CURRENT_LINE
                )
        # ----- function body -----
        body = []
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or indent_of(lines[j]) > base_indent):
            body.append(lines[j])
            j += 1
        if not body:
            roast_error(
                "Function body khaali nahi ho sakda.",
                state.CURRENT_LINE
            )
        functions[fname] = (params, body)
        return j


    # return
    if stmt.startswith("wapas_kar"):
        ret_expr = stmt.replace("wapas_kar", "", 1).strip()
        
        # Check for function calls in the expression and handle them
        # This enables recursive functions
        result = evaluate_with_functions(ret_expr, norm)
        variables["__return__"] = result
        return len(lines)

    # assignment (indexed or normal)
    if stmt.startswith("chal_oye"):
        after = stmt.replace("chal_oye", "", 1).strip()
        if " ban " not in f" {after} ":
            roast_error("chal_oye syntax galat hai. Format: chal_oye <var> ban <expr>", state.CURRENT_LINE)

        left, expr = after.split("ban", 1)
        target = left.strip()
        expr = expr.strip()
        if not target:
            roast_error(
                "chal_oye vich variable missing hai.",
                state.CURRENT_LINE
            )


        # indexed assignment
        if "[" in target and "]" in target:
            container_name = target[:target.index("[")].strip()
            index_expr = target[target.index("[")+1:target.index("]")]

            if container_name not in variables:
                roast_error("Variable define nahi hoya.", state.CURRENT_LINE)

            container = variables[container_name]
            index = safe_eval(norm(index_expr))
            value = safe_eval(norm(expr))
            
            try:
                container[index] = value
            except:
                roast_error("Indexed assignment galat hai.", state.CURRENT_LINE)
        else:
            # normal assignment / function call
            has_parens = "(" in expr and expr.endswith(")")
            fname = expr.split("(", 1)[0] if has_parens else None
            
            # Check for built-in functions
            builtin_funcs = {
                'kinna_lamba': kinna_lamba,
                'sort_hoja_oye': sort_hoja_oye,
                'ulta_hoja_oye': ulta_hoja_oye,
                'jod_oye': jod_oye,
                'average_kad': average_kad,
                'sabton_vaddha': sabton_vaddha,
                'sabton_nikka': sabton_nikka,
                'dona_nu_jod_oye': dona_nu_jod_oye,
                'range_banao': range_banao,
            }
            
            if has_parens and fname in builtin_funcs:
                # Handle built-in function call
                args_str = expr[expr.find("(")+1:expr.find(")")]
                args = [safe_eval(norm(arg.strip())) for arg in args_str.split(",") if arg.strip()]
                
                try:
                    result = builtin_funcs[fname](*args)
                    variables[target] = result
                except Exception as e:
                    roast_error(f"Built-in function error: {str(e)}", state.CURRENT_LINE)
            elif has_parens and fname in functions:
                args_str = expr[expr.find("(")+1:expr.find(")")]
                # Handle empty argument list properly
                args = [arg.strip() for arg in args_str.split(",") if arg.strip()] if args_str.strip() else []
                params, body = functions[fname]

                if len(args) != len(params):
                    roast_error("Function arguments ginti galat hai.", state.CURRENT_LINE)

                from compiler.errors import push_function, pop_function
                push_function(fname, state.CURRENT_LINE)
                
                backup = variables.copy()
                try:
                    for p, a in zip(params, args):
                       variables[p] = evaluate_with_functions(a, norm)

                    variables.pop("__return__", None)
                    execute_block(body, 0, indent_of(body[0]), (state.CURRENT_LINE or 1) - 1)

                    if "__return__" not in variables:
                        roast_error("wapas_kar missing hai.", state.CURRENT_LINE)

                    result = variables["__return__"]
                finally:
                    # Preserve global variables
                    global_values = {k: v for k, v in variables.items() if k in state.GLOBAL_VARS}
                    variables.clear()
                    variables.update(backup)
                    # Restore any global variables that were modified
                    variables.update(global_values)
                    pop_function()
                variables[target] = result
            else:
                # Check for method calls (e.g., "string".upper_case_oye())
                if "." in expr and "(" in expr and expr.endswith(")"):
                    # Extract object and method
                    method_pattern = r'(.+)\.(\w+)\((.*)\)'
                    import re as regex_module
                    match = regex_module.match(method_pattern, expr)
                    if match:
                        obj_expr, method_name, args_str = match.groups()
                        obj = safe_eval(norm(obj_expr))
                        
                        # String methods
                        if isinstance(obj, str):
                            string_methods = {
                                'upper_case_oye': lambda: obj.upper(),
                                'lower_case_oye': lambda: obj.lower(),
                                'tut_ja_oye': lambda arg=None: obj.split(arg) if arg else obj.split(),
                                'jud_ja_oye': lambda arg: arg.join(str(x) for x in arg) if hasattr(arg, '__iter__') else obj.join([str(arg)]),
                                'badal_ja_oye': lambda old, new: obj.replace(old, new),
                                'haiga_hai': lambda sub: sub in obj,
                                'shuru_hunda_hai': lambda pre: obj.startswith(pre),
                                'khatam_hunda_hai': lambda suf: obj.endswith(suf),
                                'trim_hoja_oye': lambda: obj.strip(),
                            }
                            
                            if method_name in string_methods:
                                try:
                                    # Parse arguments
                                    if args_str.strip():
                                        method_args = [safe_eval(norm(arg.strip())) for arg in args_str.split(",")]
                                        result = string_methods[method_name](*method_args)
                                    else:
                                        result = string_methods[method_name]()
                                    variables[target] = result
                                except Exception as e:
                                    roast_error(f"String method error: {str(e)}", state.CURRENT_LINE)
                            else:
                                roast_error(f"Unknown string method: {method_name}", state.CURRENT_LINE)
                        # List methods
                        elif isinstance(obj, list):
                            list_methods = {
                                'contains': lambda item: item in obj,
                                'index_of': lambda item: obj.index(item) if item in obj else -1,
                                'reverse_it': lambda: (obj.reverse(), obj)[1],
                                'sort_it': lambda: (obj.sort(), obj)[1],
                            }
                            
                            if method_name in list_methods:
                                try:
                                    if args_str.strip():
                                        method_args = [safe_eval(norm(arg.strip())) for arg in args_str.split(",")]
                                        result = list_methods[method_name](*method_args)
                                    else:
                                        result = list_methods[method_name]()
                                    variables[target] = result
                                except Exception as e:
                                    roast_error(f"List method error: {str(e)}", state.CURRENT_LINE)
                            else:
                                roast_error(f"Unknown list method: {method_name}", state.CURRENT_LINE)
                        # Dict methods
                        elif isinstance(obj, dict):
                            dict_methods = {
                                'get_keys': lambda: list(obj.keys()),
                                'get_values': lambda: list(obj.values()),
                                'has_key': lambda key: key in obj,
                            }
                            
                            if method_name in dict_methods:
                                try:
                                    if args_str.strip():
                                        method_args = [safe_eval(norm(arg.strip())) for arg in args_str.split(",")]
                                        result = dict_methods[method_name](*method_args)
                                    else:
                                        result = dict_methods[method_name]()
                                    variables[target] = result
                                except Exception as e:
                                    roast_error(f"Dict method error: {str(e)}", state.CURRENT_LINE)
                            else:
                                roast_error(f"Unknown dict method: {method_name}", state.CURRENT_LINE)
                        else:
                            roast_error(f"Methods not supported for {type(obj).__name__}", state.CURRENT_LINE)
                    else:
                        variables[target] = safe_eval(norm(expr))
                else:
                    variables[target] = safe_eval(norm(expr))

        return i + 1

    # append
    if stmt.startswith("pa_ander"):
        _, name, expr = stmt.split(maxsplit=2)
        if name not in variables or not isinstance(variables[name], list):
            roast_error("pa_ander sirf list layi use hunda hai.", state.CURRENT_LINE)
        variables[name].append(safe_eval(norm(expr)))
        return i + 1

    # length
    if stmt.startswith("kinna_lamba"):
        _, name = stmt.split(maxsplit=1)
        print(len(variables[name]))
        return i + 1

    # copy
    if stmt.startswith("copy_kar"):
        _, src, dest = stmt.split()
        variables[dest] = variables[src].copy()
        return i + 1

    # clear
    if stmt.startswith("saaf_kar"):
        _, name = stmt.split()
        variables[name].clear()
        return i + 1

    # print
    if stmt.startswith("chilla_we"):
        expr = stmt.replace("chilla_we", "", 1).strip()
        # Use evaluate_expression_with_builtins to support function calls
        result = evaluate_expression_with_builtins(expr)
        # Process escape sequences if it's a string
        if isinstance(result, str):
            result = process_string_escapes(f'"{result}"')
        print(result)
        return i + 1
    
    if stmt == "chal_koshish_karle":
        return execute_try_pakad(lines, i, base_indent)


    # control flow
    if stmt.startswith("je"):
        return execute_if_chain(lines, i, base_indent)

    if stmt.startswith("jadon_tak"):
        return execute_loop(lines, i, base_indent)

    if stmt.startswith("har_ek"):
        return execute_foreach(lines, i, base_indent)
    
    # roko_oye_roko (break)
    if stmt == "roko_oye_roko":
        if state.LOOP_DEPTH == 0:
            roast_error("roko_oye_roko sirf loop vich allowed hai.", state.CURRENT_LINE)
        raise BreakSignal()

    if stmt == "chalo_oye_chalo":
        if state.LOOP_DEPTH == 0:
            roast_error("chalo_oye_chalo sirf loop vich allowed hai.", state.CURRENT_LINE)
        raise ContinueSignal()
    
    # global keyword - declare variables as global scope
    if stmt.startswith("global"):
        # Parse: global var1, var2, var3
        parts = stmt.split(None, 1)
        if len(parts) < 2:
            roast_error("global ke baad variable names chahide ne.", state.CURRENT_LINE)
        
        var_names = parts[1].split(",")
        for var_name in var_names:
            var_name = var_name.strip()
            if var_name:
                state.GLOBAL_VARS.add(var_name)
        return i + 1


    known = (
    "das_oye", "chal_oye", "kaam", "wapas_kar", "chilla_we",
    "je", "nahin_taan_je", "nahin_taan",
    "jadon_tak", "har_ek", "pa_ander",
    "copy_kar", "saaf_kar", "kinna_lamba",
    "fuddu_chiz", "python_le_aa",
    "chal_koshish_karle", "pakad", "throw", "roko_oye_roko", "chalo_oye_chalo", "global"
    )


    first = stmt.split()[0]
    if first not in known:
        syntax_error(f"Unknown keyword: {first}")

    roast_error("Syntax samajh nahi aaya.", state.CURRENT_LINE)


# ---------------- runner ----------------
def run(code):
    import compiler.state as state
    from compiler.runtime import register_builtins, variables, functions, python_funcs
    from compiler.errors import set_code_context, clear_error_context
    
    # Reset state for fresh execution (but preserve DEBUG_MODE set by CLI)
    debug_mode = bool(state.DEBUG_MODE)
    state.CURRENT_LINE = 1
    state.LOOP_DEPTH = 0
    state.IN_TRY = 0
    state.INDENT_TYPE = None
    state.INDENT_WIDTH = None
    state.GLOBAL_VARS = set()
    state.TRACE_EXECUTION = []
    state.DEBUG_MODE = debug_mode

    clear_error_context()

    # Clear runtime state (prevents leaking variables/functions/imports between runs)
    variables.clear()
    functions.clear()
    python_funcs.clear()

    register_builtins()  # Register builtin functions for eval()

    raw = code.splitlines()
    
    # Set error context for better debugging
    set_code_context(raw)

    if not raw or raw[0].strip() != "sun_we":
        roast_error("Program sun_we naal shuru kar.")

    if raw[-1].strip() != "ja_we":
        roast_error("Program ja_we naal khatam kar.", len(raw))

    # Check for duplicate sun_we or ja_we in the middle of code
    for i, line in enumerate(raw[1:-1], start=2):  # Start from line 2, skip first sun_we and last ja_we
        stripped = line.strip()
        if stripped == "sun_we":
            roast_error(f"sun_we sirf program de start layi use hunda hai. Line {i} layi galat jaga hai.", i)
        if stripped == "ja_we":
            roast_error(f"ja_we sirf program de end layi use hunda hai. Line {i} layi galat jaga hai.", i)

    lines = raw[1:-1]

    base_indent = None
    for l in lines:
        if l.strip():
            base_indent = indent_of(l)
            break

    if base_indent != 1:
        roast_error(
        "sun_we de baad 1 indent level chahidi hai (4 spaces ya 1 TAB).",
        2
        )



    execute_block(lines, 0, base_indent, 1)

# ---------------- compiler ----------------
def compile_to_python(code):
    """Compile Jatti code to Python code"""
    from compiler.errors import set_code_context
    from compiler.errors import clear_error_context
    
    clear_error_context()

    raw = code.splitlines()
    set_code_context(raw)
    
    # Validation
    if not raw or raw[0].strip() != "sun_we":
        roast_error("Program sun_we naal shuru kar.")
    
    if raw[-1].strip() != "ja_we":
        roast_error("Program ja_we naal khatam kar.", len(raw))
    
    # Check for duplicate sun_we or ja_we in the middle of code
    for i, line in enumerate(raw[1:-1], start=2):  # Start from line 2, skip first sun_we and last ja_we
        stripped = line.strip()
        if stripped == "sun_we":
            roast_error(f"sun_we sirf program de start layi use hunda hai. Line {i} layi galat jaga hai.", i)
        if stripped == "ja_we":
            roast_error(f"ja_we sirf program de end layi use hunda hai. Line {i} layi galat jaga hai.", i)
    
    lines = raw[1:-1]

    # Determine the required base indent inside sun_we (should be exactly 1 level)
    base_indent_level = None
    for l in lines:
        if l.strip():
            base_indent_level = _indent_level_for_formatting(l)
            break
    if base_indent_level is None:
        base_indent_level = 1
    
    # Generate Python code
    python_lines = ["#!/usr/bin/env python3"]
    python_lines.append("# Auto-generated from Jatti code")
    python_lines.append("")
    
    # Add a minimal runtime so the generated Python file can run standalone.
    python_lines.append("# Minimal Jatti stdlib (embedded)")
    python_lines.append("class __JattiThrown(Exception):")
    python_lines.append("    pass")
    python_lines.append("")
    python_lines.append("def __jatti_exception_value(e):")
    python_lines.append("    # Match interpreter-style error payloads where practical")
    python_lines.append("    if isinstance(e, __JattiThrown):")
    python_lines.append("        return e.args[0] if e.args else None")
    python_lines.append("    if isinstance(e, ZeroDivisionError):")
    python_lines.append("        return 'Zero naal divide nahi kar sakde.'")
    python_lines.append("    if isinstance(e, TypeError):")
    python_lines.append("        return 'Galat type operation hoyi hai.'")
    python_lines.append("    if isinstance(e, NameError):")
    python_lines.append("        # Best-effort; Python messages vary")
    python_lines.append("        return f'Variable define nahi hoya: {e}'")
    python_lines.append("    return str(e)")
    python_lines.append("")
    python_lines.append("def kinna_lamba(obj):")
    python_lines.append("    return len(obj)")
    python_lines.append("")
    python_lines.append("def sort_hoja_oye(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('sort_hoja_oye: only works with lists')")
    python_lines.append("    return sorted(lst)")
    python_lines.append("")
    python_lines.append("def ulta_hoja_oye(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('ulta_hoja_oye: only works with lists')")
    python_lines.append("    return list(reversed(lst))")
    python_lines.append("")
    python_lines.append("def jod_oye(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('jod_oye: only works with lists')")
    python_lines.append("    return sum(lst)")
    python_lines.append("")
    python_lines.append("def average_kad(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('average_kad: only works with lists')")
    python_lines.append("    if len(lst) == 0:")
    python_lines.append("        raise ValueError('average_kad: cannot average empty list')")
    python_lines.append("    return sum(lst) / len(lst)")
    python_lines.append("")
    python_lines.append("def sabton_vaddha(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('sabton_vaddha: only works with lists')")
    python_lines.append("    if len(lst) == 0:")
    python_lines.append("        raise ValueError('sabton_vaddha: cannot find max of empty list')")
    python_lines.append("    return max(lst)")
    python_lines.append("")
    python_lines.append("def sabton_nikka(lst):")
    python_lines.append("    if not isinstance(lst, list):")
    python_lines.append("        raise TypeError('sabton_nikka: only works with lists')")
    python_lines.append("    if len(lst) == 0:")
    python_lines.append("        raise ValueError('sabton_nikka: cannot find min of empty list')")
    python_lines.append("    return min(lst)")
    python_lines.append("")
    python_lines.append("def dona_nu_jod_oye(str1, str2):")
    python_lines.append("    return str(str1) + str(str2)")
    python_lines.append("")
    python_lines.append("def range_banao(*args):")
    python_lines.append("    if len(args) == 1:")
    python_lines.append("        return list(range(int(args[0])))")
    python_lines.append("    if len(args) == 2:")
    python_lines.append("        return list(range(int(args[0]), int(args[1])))")
    python_lines.append("    if len(args) == 3:")
    python_lines.append("        return list(range(int(args[0]), int(args[1]), int(args[2])))")
    python_lines.append("    raise ValueError('range_banao: takes 1-3 arguments')")
    python_lines.append("")

    # Wrap translated code so the mandatory Jatti indentation becomes valid Python
    python_lines.append("def __jatti_main__():")
    
    # Convert Jatti code to Python
    for line in lines:
        converted_lines = convert_line_to_python(line, base_dedent=base_indent_level, extra_indent=1)
        if isinstance(converted_lines, str):
            python_lines.append(converted_lines)
        else:
            python_lines.extend(converted_lines)

    python_lines.append("")
    python_lines.append("if __name__ == '__main__':")
    python_lines.append("    __jatti_main__()")
    
    return "\n".join(python_lines)


def _indent_level_for_formatting(line: str) -> int:
    prefix = line[:len(line) - len(line.lstrip())]
    if not prefix:
        return 0

    # Treat tabs as one indent level, spaces as 4 per level.
    # If mixed indentation appears, fall back to a best-effort conversion.
    tabs = prefix.count("\t")
    spaces = prefix.count(" ")

    if tabs and not spaces:
        return tabs
    if spaces and not tabs:
        return spaces // 4

    # Mixed: approximate by converting tabs to 4 spaces.
    return (tabs * 4 + spaces) // 4


def convert_line_to_python(line, *, base_dedent: int = 0, extra_indent: int = 0):
    """Convert a single Jatti line to Python.

    Returns either a string (single output line) or a list of strings.
    """
    if not line.strip():
        return ""

    indent_level = _indent_level_for_formatting(line)
    indent_level = max(0, indent_level - base_dedent + extra_indent)
    py_indent = "    " * indent_level
    content = line.strip()

    # Comments
    if content.startswith("fuddu_chiz"):
        comment = content.replace("fuddu_chiz", "#", 1).strip()
        return py_indent + comment

    # Variable declaration: chal_oye x ban expr
    if content.startswith("chal_oye ") and " ban " in content:
        _, rest = content.split("chal_oye", 1)
        rest = rest.strip()
        target, expr = rest.split(" ban ", 1)
        return py_indent + f"{target.strip()} = {norm(expr.strip())}"

    # Print: chilla_we expr
    if content.startswith("chilla_we"):
        expr = content.replace("chilla_we", "", 1).strip()
        return py_indent + f"print({norm(expr)})"

    # Control flow
    if content.startswith("je"):
        cond = content.replace("je", "", 1).strip()
        return py_indent + f"if {norm(cond)}:"

    if content.startswith("nahin_taan_je"):
        cond = content.replace("nahin_taan_je", "", 1).strip()
        return py_indent + f"elif {norm(cond)}:"

    if content == "nahin_taan":
        return py_indent + "else:"

    if content.startswith("jadon_tak"):
        cond = content.replace("jadon_tak", "", 1).strip()
        return py_indent + f"while {norm(cond)}:"

    # Foreach: har_ek x iterableExpr  OR  har_ek key, value iterableExpr
    if content.startswith("har_ek"):
        header = content.replace("har_ek", "", 1).strip()

        paren_depth = 0
        last_space_outside_parens = -1
        for idx, ch in enumerate(header):
            if ch == '(':
                paren_depth += 1
            elif ch == ')':
                paren_depth -= 1
            elif ch == ' ' and paren_depth == 0:
                last_space_outside_parens = idx

        if last_space_outside_parens == -1:
            return py_indent + f"# Unsupported har_ek syntax: {header}"

        vars_part = header[:last_space_outside_parens].strip()
        iterable_expr = header[last_space_outside_parens:].strip()

        if "," in vars_part:
            key_var, val_var = [v.strip() for v in vars_part.split(",", 1)]
            return py_indent + f"for {key_var}, {val_var} in {norm(iterable_expr)}.items():"
        else:
            return py_indent + f"for {vars_part} in {norm(iterable_expr)}:"

    # Function definition: kaam name(args)
    if content.startswith("kaam "):
        head = content.split(None, 1)[1]
        fname = head.split("(", 1)[0].strip()
        args = head[head.find("(") + 1: head.rfind(")")].strip() if "(" in head and ")" in head else ""
        return py_indent + f"def {fname}({args}):"

    # Return
    if content.startswith("wapas_kar"):
        expr = content.replace("wapas_kar", "", 1).strip()
        if expr:
            return py_indent + f"return {norm(expr)}"
        return py_indent + "return"

    # Try / catch
    if content == "chal_koshish_karle":
        return py_indent + "try:"

    if content.startswith("pakad"):
        parts = content.split()
        if len(parts) == 2 and parts[1].isidentifier():
            var_name = parts[1]
            return [
                py_indent + "except Exception as __jatti_e__:",
                (py_indent + "    " + f"{var_name} = __jatti_exception_value(__jatti_e__)"),
            ]
        return py_indent + "except Exception:"

    # Throw
    if content.startswith("throw"):
        expr = content.replace("throw", "", 1).strip()
        if expr:
            return py_indent + f"raise __JattiThrown({norm(expr)})"
        return py_indent + "raise __JattiThrown()"

    # Break / continue
    if content == "roko_oye_roko":
        return py_indent + "break"
    if content == "chalo_oye_chalo":
        return py_indent + "continue"

    # List append: pa_ander name expr
    if content.startswith("pa_ander "):
        parts = content.split(maxsplit=2)
        if len(parts) == 3:
            _, name, expr = parts
            return py_indent + f"{name}.append({norm(expr)})"

    # Copy: copy_kar src dest
    if content.startswith("copy_kar "):
        parts = content.split()
        if len(parts) == 3:
            _, src, dest = parts
            return py_indent + f"{dest} = {src}.copy()"

    # Clear: saaf_kar name
    if content.startswith("saaf_kar "):
        parts = content.split()
        if len(parts) == 2:
            _, name = parts
            return py_indent + f"{name}.clear()"

    # Python import: python_le_aa "module" thon x, y
    if content.startswith("python_le_aa") and " thon " in content:
        parts = content.split()
        try:
            module = parts[1].strip('"')
            idx = parts.index("thon")
            names = [p.strip(",") for p in parts[idx + 1:]]
            names = [n for n in names if n]
            if names:
                return py_indent + f"from {module} import {', '.join(names)}"
        except Exception:
            pass

    # Fallback: best-effort keyword normalization
    return py_indent + norm(content)


# ---------------- formatter ----------------
def format_code(code):
    """Format Jatti code with proper indentation"""
    lines = code.splitlines()
    formatted = []
    
    # Ensure sun_we and ja_we are at the start/end
    if not lines or lines[0].strip() != "sun_we":
        formatted.append("sun_we")

    saw_sun_we = False
    saw_ja_we = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted.append("")
            continue

        if stripped == "sun_we":
            if not saw_sun_we:
                formatted.append("sun_we")
                saw_sun_we = True
            continue

        if stripped == "ja_we":
            saw_ja_we = True
            # We'll append it at the end to ensure it's last.
            continue

        indent_level = _indent_level_for_formatting(line)
        content = stripped
        formatted.append("    " * indent_level + content)

    if not saw_ja_we:
        formatted.append("ja_we")
    else:
        # Ensure it's the last non-empty line
        if formatted and formatted[-1].strip() != "ja_we":
            formatted.append("ja_we")

    return "\n".join(formatted)