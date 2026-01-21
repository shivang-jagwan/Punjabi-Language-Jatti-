#!/usr/bin/env python3
# Auto-generated from Jatti code

# Minimal Jatti stdlib (embedded)
class __JattiThrown(Exception):
    pass

def __jatti_exception_value(e):
    # Match interpreter-style error payloads where practical
    if isinstance(e, __JattiThrown):
        return e.args[0] if e.args else None
    if isinstance(e, ZeroDivisionError):
        return 'Zero naal divide nahi kar sakde.'
    if isinstance(e, TypeError):
        return 'Galat type operation hoyi hai.'
    if isinstance(e, NameError):
        # Best-effort; Python messages vary
        return f'Variable define nahi hoya: {e}'
    return str(e)

def kinna_lamba(obj):
    return len(obj)

def sort_hoja_oye(lst):
    if not isinstance(lst, list):
        raise TypeError('sort_hoja_oye: only works with lists')
    return sorted(lst)

def ulta_hoja_oye(lst):
    if not isinstance(lst, list):
        raise TypeError('ulta_hoja_oye: only works with lists')
    return list(reversed(lst))

def jod_oye(lst):
    if not isinstance(lst, list):
        raise TypeError('jod_oye: only works with lists')
    return sum(lst)

def average_kad(lst):
    if not isinstance(lst, list):
        raise TypeError('average_kad: only works with lists')
    if len(lst) == 0:
        raise ValueError('average_kad: cannot average empty list')
    return sum(lst) / len(lst)

def sabton_vaddha(lst):
    if not isinstance(lst, list):
        raise TypeError('sabton_vaddha: only works with lists')
    if len(lst) == 0:
        raise ValueError('sabton_vaddha: cannot find max of empty list')
    return max(lst)

def sabton_nikka(lst):
    if not isinstance(lst, list):
        raise TypeError('sabton_nikka: only works with lists')
    if len(lst) == 0:
        raise ValueError('sabton_nikka: cannot find min of empty list')
    return min(lst)

def dona_nu_jod_oye(str1, str2):
    return str(str1) + str(str2)

def range_banao(*args):
    if len(args) == 1:
        return list(range(int(args[0])))
    if len(args) == 2:
        return list(range(int(args[0]), int(args[1])))
    if len(args) == 3:
        return list(range(int(args[0]), int(args[1]), int(args[2])))
    raise ValueError('range_banao: takes 1-3 arguments')

def __jatti_main__():
    try:
        x = 10 / 0
        print("unreachable")
    except Exception as __jatti_e__:
        err = __jatti_exception_value(__jatti_e__)
        print(err)

if __name__ == '__main__':
    __jatti_main__()