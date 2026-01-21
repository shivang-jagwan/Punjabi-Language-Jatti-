# compiler/state.py
CURRENT_LINE = 1
LOOP_DEPTH = 0
IN_TRY = 0

INDENT_TYPE = None   # "space" or "tab"
INDENT_WIDTH = None # 4 for spaces, 1 for tabs
GLOBAL_VARS = set()  # Track which variables are declared as global

# Debugging/tracing
DEBUG_MODE = False  # Set to True to see execution trace
TRACE_EXECUTION = []  # Store execution trace