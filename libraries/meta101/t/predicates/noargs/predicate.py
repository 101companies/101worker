"""
Test predicate that returns a match if it is given no arguments.
"""

def run(filename, *args):
    return len(args) == 0
