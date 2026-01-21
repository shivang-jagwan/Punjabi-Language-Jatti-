# Jatti Standard Library - Built-in Functions
# These functions are available to all Jatti programs

def kinna_lamba(obj):
    """Get length of list/string/dict"""
    try:
        return len(obj)
    except:
        raise TypeError(f"kinna_lamba: {type(obj).__name__} has no length")


def sort_hoja_oye(lst):
    """Sort a list and return sorted copy"""
    if not isinstance(lst, list):
        raise TypeError("sort_hoja_oye: only works with lists")
    return sorted(lst)


def ulta_hoja_oye(lst):
    """Reverse a list and return reversed copy"""
    if not isinstance(lst, list):
        raise TypeError("ulta_hoja_oye: only works with lists")
    return list(reversed(lst))


def jod_oye(lst):
    """Sum all elements in a list"""
    if not isinstance(lst, list):
        raise TypeError("jod_oye: only works with lists")
    try:
        return sum(lst)
    except:
        raise TypeError("jod_oye: list contains non-numeric values")


def average_kad(lst):
    """Calculate average of list elements"""
    if not isinstance(lst, list):
        raise TypeError("average_kad: only works with lists")
    if len(lst) == 0:
        raise ValueError("average_kad: cannot average empty list")
    try:
        return sum(lst) / len(lst)
    except:
        raise TypeError("average_kad: list contains non-numeric values")


def sabton_vaddha(lst):
    """Find maximum value in list"""
    if not isinstance(lst, list):
        raise TypeError("sabton_vaddha: only works with lists")
    if len(lst) == 0:
        raise ValueError("sabton_vaddha: cannot find max of empty list")
    try:
        return max(lst)
    except:
        raise TypeError("sabton_vaddha: list contains incomparable values")


def sabton_nikka(lst):
    """Find minimum value in list"""
    if not isinstance(lst, list):
        raise TypeError("sabton_nikka: only works with lists")
    if len(lst) == 0:
        raise ValueError("sabton_nikka: cannot find min of empty list")
    try:
        return min(lst)
    except:
        raise TypeError("sabton_nikka: list contains incomparable values")


def dona_nu_jod_oye(str1, str2):
    """Join two strings"""
    return str(str1) + str(str2)


def range_banao(*args):
    """Create a range of numbers - supports range(stop), range(start, stop), range(start, stop, step)"""
    if len(args) == 1:
        # range(stop)
        return list(range(int(args[0])))
    elif len(args) == 2:
        # range(start, stop)
        return list(range(int(args[0]), int(args[1])))
    elif len(args) == 3:
        # range(start, stop, step)
        return list(range(int(args[0]), int(args[1]), int(args[2])))
    else:
        raise ValueError("range_banao: takes 1-3 arguments")


# String methods (added to string class dynamically)
class JattiString(str):
    """Extended string class with Jatti methods"""
    
    def upper_case_oye(self):
        """Convert to uppercase"""
        return self.upper()
    
    def lower_case_oye(self):
        """Convert to lowercase"""
        return self.lower()
    
    def tut_ja_oye(self, delim=" "):
        """Split string by delimiter"""
        return self.split(delim)
    
    def jud_ja_oye(self, lst):
        """Join list with this string as separator"""
        return self.join(str(x) for x in lst)
    
    def badal_ja_oye(self, old, new):
        """Replace occurrences"""
        return self.replace(old, new)
    
    def haiga_hai(self, substring):
        """Check if contains substring"""
        return substring in self
    
    def shuru_hunda_hai(self, prefix):
        """Check if starts with prefix"""
        return self.startswith(prefix)
    
    def khatam_hunda_hai(self, suffix):
        """Check if ends with suffix"""
        return self.endswith(suffix)
    
    def trim_hoja_oye(self):
        """Remove leading/trailing whitespace"""
        return self.strip()


# List methods
class JattiList(list):
    """Extended list class with Jatti methods"""
    
    def contains(self, item):
        """Check if list contains item"""
        return item in self
    
    def index_of(self, item):
        """Find index of item"""
        try:
            return self.index(item)
        except ValueError:
            return -1
    
    def reverse_it(self):
        """Reverse list in place"""
        self.reverse()
        return self
    
    def sort_it(self):
        """Sort list in place"""
        self.sort()
        return self


# Dict methods
class JattiDict(dict):
    """Extended dict class with Jatti methods"""
    
    def get_keys(self):
        """Get all keys as list"""
        return list(self.keys())
    
    def get_values(self):
        """Get all values as list"""
        return list(self.values())
    
    def has_key(self, key):
        """Check if key exists"""
        return key in self
