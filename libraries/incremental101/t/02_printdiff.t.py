from TAP.Simple import *
from StringIO   import StringIO
import incremental101 as inc

plan(4)

def doline(*args):
    inc.outstream = StringIO()
    inc.printdiff(*args)
    return inc.outstream.getvalue()


eq_ok(inc.linesread, 0, "no lines read yet")
eq_ok(doline(), "\n0 - -\n", "empty diff")

inc.linesread = 5
eq_ok(doline(), "\n5 - -\n", "empty diff with appropriate line count")

inc.linesread = 123
eq_ok(doline("A", "/path/to/file"), "\n123 A /path/to/file\n", "diff with path")
