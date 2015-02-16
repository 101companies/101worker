import os
from   StringIO       import StringIO
from   TAP.Simple     import *
from   meta101.util   import diff
import incremental101 as     inc
execfile("t/dies_ok.py")

plan(5)


called = []
switch = {
    "A" : lambda **kwargs: called.append(["A", kwargs]),
    "M" : lambda **kwargs: called.append(["M", kwargs]),
    "D" : lambda **kwargs: called.append(["D", kwargs]),
}


inc.instream  = StringIO()
diff(".suffix", **switch)
eq_ok(called, [], "diff with no input doesn't call anything")


inc.instream = StringIO("A /path/repo/file\n")
dies_ok(lambda: diff(".suffix", **switch), "missing environment variables dies")


os.environ[   "repo101dir"] = "/path/repo"
os.environ["targets101dir"] = "/path/targets"

inc.instream = StringIO("""A /path/repo/added.json
A /path/targets/ignored.json
M /path/repo/somedir/modified.java
M /path/somewhere/else.java
D /path/repo/some/more/dirs/deleted
D /some/totally/different/path
""")

called = []
want   = [
    ["A", {
        "target"     : "/path/targets/added.json.suffix",
        "targetbase" : "/path/targets/added.json",
        "filename"   : "/path/repo/added.json",
        "relative"   : "added.json",
        "dirname"    : "",
        "basename"   : "added.json",
    }],
    ["M", {
        "target"     : "/path/targets/somedir/modified.java.suffix",
        "targetbase" : "/path/targets/somedir/modified.java",
        "filename"   : "/path/repo/somedir/modified.java",
        "relative"   : "somedir/modified.java",
        "dirname"    : "somedir",
        "basename"   : "modified.java",
    }],
    ["D", {
        "target"     : "/path/targets/some/more/dirs/deleted.suffix",
        "targetbase" : "/path/targets/some/more/dirs/deleted",
        "filename"   : "/path/repo/some/more/dirs/deleted",
        "relative"   : "some/more/dirs/deleted",
        "dirname"    : "some/more/dirs",
        "basename"   : "deleted",
    }],
]
diff(".suffix", **switch)
eq_ok(called, want, "repo paths are called correctly, other paths are ignored")



for entry in want:
    target = entry[1]["target"]
    entry[1]["target"] = [target + "1", target + "2"]

called = []
inc.instream.seek(0)
diff([".suffix1", ".suffix2"], **switch)
eq_ok(called, want, "multiple suffixes using a list")

called = []
inc.instream.seek(0)
diff((".suffix1", ".suffix2"), **switch)
eq_ok(called, want, "multiple suffixes using a tuple")
