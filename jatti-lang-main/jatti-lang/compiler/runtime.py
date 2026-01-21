class JattiException(Exception):
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass


from compiler.errors import roast_error
import compiler.state as state   # ✅ REQUIRED

variables = {}
functions = {}
python_funcs = {}


def process_string_escapes(s):
    """Convert Jatti escape sequences to Python equivalents"""
    if not isinstance(s, str) or not s.startswith('"') or not s.endswith('"'):
        return s
    
    # Remove outer quotes
    content = s[1:-1]
    
    # Replace escape sequences
    content = content.replace('\\n', '\n')
    content = content.replace('\\t', '\t')
    content = content.replace('\\r', '\r')
    content = content.replace('\\"', '"')
    content = content.replace('\\\\', '\\')
    
    return content


def safe_eval(expr: str):
    try:
        # ---------- numeric comparison safety ----------
        # Check for any comparison operator (checking multi-char operators first to avoid false matches)
        comp_op = None
        left = None
        right = None
        
        # Find comparison operator OUTSIDE of strings
        in_string = False
        i = 0
        while i < len(expr):
            if expr[i] == '"' and (i == 0 or expr[i-1] != '\\'):
                in_string = not in_string
            
            if not in_string:
                # Check for multi-character operators first
                if expr[i:i+2] == ">=":
                    comp_op = ">="
                    left, right = expr[:i], expr[i+2:]
                    break
                elif expr[i:i+2] == "<=":
                    comp_op = "<="
                    left, right = expr[:i], expr[i+2:]
                    break
                elif expr[i:i+2] == "==":
                    comp_op = "=="
                    left, right = expr[:i], expr[i+2:]
                    break
                elif expr[i:i+2] == "!=":
                    comp_op = "!="
                    left, right = expr[:i], expr[i+2:]
                    break
                elif expr[i] == '>':
                    comp_op = ">"
                    left, right = expr[:i], expr[i+1:]
                    break
                elif expr[i] == '<':
                    comp_op = "<"
                    left, right = expr[:i], expr[i+1:]
                    break
            
            i += 1
        
        if comp_op:
            lval = eval(left.strip(), python_funcs, variables)
            rval = eval(right.strip(), python_funcs, variables)

            if not isinstance(lval, (int, float)) or not isinstance(rval, (int, float)):
                if state.IN_TRY > 0:
                    raise JattiException("Comparison sirf numbers layi allowed hai.")
                roast_error(
                    "Comparison sirf numbers layi allowed hai.",
                    state.CURRENT_LINE
                )

            return eval(expr, python_funcs, variables)

        # ---------- division by zero check ----------
        # Look for "/" outside of strings
        in_string = False
        i = 0
        div_by_zero = False
        found_div = False
        while i < len(expr):
            if expr[i] == '"' and (i == 0 or expr[i-1] != '\\'):
                in_string = not in_string
            
            if not in_string and expr[i] == '/':
                found_div = True
                break
            
            i += 1
        
        if found_div:
            # Try to evaluate and let Python catch ZeroDivisionError
            # We'll handle it in the exception handler below
            pass

        return eval(expr, python_funcs, variables)

    except NameError as e:
        name = str(e).split("'")[1]
        if state.IN_TRY > 0:
            raise JattiException(f"Variable define nahi hoya: {name}")
        roast_error(f"Variable define nahi hoya: {name}", state.CURRENT_LINE)


    except ZeroDivisionError:
        if state.IN_TRY > 0:
            raise JattiException("Zero naal divide nahi kar sakde.")
        roast_error(
            "Zero naal divide nahi kar sakde.",
            state.CURRENT_LINE
        )

    except TypeError:
        if state.IN_TRY > 0:
            raise JattiException("Galat type operation hoyi hai.")
        roast_error(
            "Galat type operation hoyi hai.",
            state.CURRENT_LINE
        )

    except Exception:
        if state.IN_TRY > 0:
            raise JattiException(f"Expression error: {expr}")
        roast_error(
            f"Expression error: {expr}",
            state.CURRENT_LINE
        )

def register_builtins():
    """Register Jatti builtin functions in python_funcs for use in eval()"""
    from compiler.stdlib import (
        kinna_lamba, sort_hoja_oye, ulta_hoja_oye, jod_oye, average_kad,
        sabton_vaddha, sabton_nikka, dona_nu_jod_oye, range_banao
    )
    
    python_funcs['kinna_lamba'] = kinna_lamba
    python_funcs['sort_hoja_oye'] = sort_hoja_oye
    python_funcs['ulta_hoja_oye'] = ulta_hoja_oye
    python_funcs['jod_oye'] = jod_oye
    python_funcs['average_kad'] = average_kad
    python_funcs['sabton_vaddha'] = sabton_vaddha
    python_funcs['sabton_nikka'] = sabton_nikka
    python_funcs['dona_nu_jod_oye'] = dona_nu_jod_oye
    python_funcs['range_banao'] = range_banao