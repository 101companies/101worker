import os
from   StringIO   import StringIO
import time
from   TAP.Simple import *
import meta101
import incremental101 as inc
execfile("t/dies_ok.py")

plan(14)

os.environ[   "repo101dir" ] = "/repo"
os.environ["targets101dir" ] = "/targets"
os.environ["matches101dump"] = "nonexistent"
os.environ[    "last101run"] = str(time.time())

# monkey-patch functions in incremental101
written = []
deleted = []
inc.writejson  = lambda path, data: written.append([path, data])
inc.deletefile = lambda path      : deleted.append(path)
inc.outstream  = StringIO()

def testmatches(wantmatches, wantwritten, wantdeleted, comment):
    global written, deleted, dump
    written = []
    deleted = []
    meta101.matchall("matches")
    eq_ok(written.pop()[1]["matches"], wantmatches, comment)
    eq_ok(written, wantwritten, "...correct files and data written")
    eq_ok(deleted, wantdeleted, "...correct files deleted")


dies_ok(lambda: meta101.matchall("matches"), "missing environment variable dies")

os.environ["rules101dump"] = "t/rules/nonexistent.json"
dies_ok(lambda: meta101.matchall("matches"), "missing rules dump dies")

os.environ["rules101dump"] = "t/rules/invalid.json"
dies_ok(lambda: meta101.matchall("matches"), "invalid json in rules dump dies")

os.environ["rules101dump"] = "t/rules/malformed.json"
dies_ok(lambda: meta101.matchall("matches"), "malformed rules dump dies")

os.environ["rules101dump"] = "t/rules/empty.json"
dies_ok(lambda: meta101.matchall("whatever"), "invalid phase dies")


inc.instream = StringIO("""A /repo/added
M /repo/modified
D /repo/deleted""")

testmatches([], [], [
                 "/targets/added.matches.json",
                 "/targets/modified.matches.json",
                 "/targets/deleted.matches.json"
             ], "input with no rules gives empty matches")


os.environ["rules101dump"] = "t/rules/rules.json"
inc.instream = StringIO()
testmatches([], [], [], "no input gives empty matches")


# TODO also test dominators

inc.instream = StringIO("""A /repo/file.py
D /repo/some.py
M /repo/dir/Makefile
M /repo/file.rb
A /repo/Main.java
A /repo/test.sh
A /repo/t/test.t.py
D /repo/main.c""")

units = {
    "java" : [
        {"metadata" : {"geshi"    : "java"}},
        {"metadata" : {"language" : "Java"}},
    ],
    "make" : [
        {"metadata" : {"geshi"     : "text"}},
        {"metadata" : {"dependsOn" : "make"}},
    ],
    "python" : [
        {"metadata" : {"geshi"    : "python"}},
        {"metadata" : {"language" : "Python"}},
    ],
    "pytap" : [
        {"metadata" : {"geshi"     : "python"}},
        {"metadata" : {"language"  : "Python"}},
        {"metadata" : {"dependsOn" : "PyTAP" }},
    ],
}

testmatches([
               {"filename" : "Main.java"   , "units" : units["java"  ]},
               {"filename" : "dir/Makefile", "units" : units["make"  ]},
               {"filename" : "file.py"     , "units" : units["python"]},
               {"filename" : "t/test.t.py" , "units" : units["pytap" ]},
           ],
           [
               ["/targets/file.py.matches.json",      units["python"]],
               ["/targets/dir/Makefile.matches.json", units["make"  ]],
               ["/targets/Main.java.matches.json",    units["java"  ]],
               ["/targets/t/test.t.py.matches.json",  units["pytap" ]],
           ],
           [
               "/targets/some.py.matches.json",
               "/targets/file.rb.matches.json",
               "/targets/test.sh.matches.json",
               "/targets/main.c.matches.json",
           ], "rules with input match correctly")
