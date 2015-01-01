from TAP.Simple import *
from StringIO   import StringIO
import incremental101 as inc

plan(9)


diffs    = [
    ("A", "/path/to/added"           ),
    ("M", "/modified/file with space"),
    ("D", "   excess spaces   "      ),
]
diffstrings   = ["{} {}\n".format(op, path) for op, path in diffs];
inc.instream  = StringIO("".join(diffstrings))
inc.outstream = StringIO()


eq_ok(inc.linesread,  0,                      "no lines read yet"        )
eq_ok(inc.nextdiff(), diffs[0],               "regular path"             )
eq_ok(inc.nextdiff(), diffs[1],               "path with spaces"         )
eq_ok(inc.nextdiff(), ("D", "excess spaces"), "excess spaces are removed")
eq_ok(inc.linesread,  3,                      "three lines read"         )

is_ok(inc.nextdiff(), None, "no more lines in diff returns None")
eq_ok(inc.linesread,  3,    "line count remained the same"      )


inc.instream = StringIO("B invalid operation\n")

try:
    inc.nextdiff()
except Exception as e:
    exception = e
else:
    exception = None

ok(exception, "invalid line raises exception")
eq_ok(inc.linesread, 3, "line count still remained the same")
