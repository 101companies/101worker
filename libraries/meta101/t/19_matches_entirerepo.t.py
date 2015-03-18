import json
import os
from   StringIO     import StringIO
from   TAP.Simple   import *
import meta101
import incremental101
execfile("t/tempdir.py")

plan(15)

rule = {
    "suffix"   : ".py",
    "metadata" : {"Language" : "Python"},
}


def setdiff(*inputs):
    lines = []

    for i in inputs:
        op, path = i.split(" ", 2)
        abspath  = os.path.join(os.environ["repo101dir"], path)
        lines.append("{} {}\n".format(op, abspath))

    incremental101.instream = StringIO("".join(lines))


def testmatches(matches, deleted, failures, comment):
    meta101.matchall("matches", entirerepo=True)

    todump = lambda match: {
        "filename" : match,
        "units"    : [{"metadata" : rule["metadata"]}],
    }
    wantdump = {
        "matches"  : [todump(match) for match in matches],
        "failures" : failures,
        "rules"    : [{"rule" : rule}],
    }
    with open(os.environ["matches101dump"]) as f:
        eq_ok(json.load(f), wantdump, comment)

    toderived = lambda f: os.path.join(os.environ["targets101dir"], f) \
                              + meta101.Matches.suffix

    for match in matches:
        with open(toderived(match)) as f:
            eq_ok(json.load(f), [{"metadata" : rule["metadata"]}],
                  "...correct derived matches file for {}".format(match))

    for d in deleted:
        ok(not os.path.exists(toderived(d)),
           "...deleted derived matches file for {}".format(d))


def touch(*files):
    for f in files:
        open(os.path.join(os.environ["repo101dir"], f), "a").close()

def unlink(*files):
    for f in files:
        os.unlink(os.path.join(os.environ["repo101dir"], f))


with tempdir() as tmp:

    os.environ[   "repo101dir" ] = os.path.join(tmp,         "repo")
    os.environ["targets101dir" ] = os.path.join(tmp,      "targets")
    os.environ[  "rules101dump"] = os.path.join(tmp,   "rules.json")
    os.environ["matches101dump"] = os.path.join(tmp, "matches.json")

    os.mkdir(os.environ[   "repo101dir"])
    os.mkdir(os.environ["targets101dir"])

    with open(os.environ["rules101dump"], "w") as f:
        json.dump({"results" : {"rules" : [{"rule" : rule}]}}, f)


    setdiff("A a.py", "M m.py")
    testmatches([], [], {}, "match over entire empty repo, diff is ignored")


    touch("file1.py", "file2.py", "file3.py")
    setdiff("A a.py", "M m.py")
    testmatches(["file1.py", "file2.py", "file3.py"], [], {},
                "match over entire filled repo derives all files")


    unlink("file1.py")
    setdiff("A a.py", "M m.py", "D file1.py")
    testmatches(["file2.py", "file3.py"], ["file1.py"], {},
                "matches with deletions, that part of the diff isn't ignored")


    with open(os.environ["matches101dump"], "r+") as f:
        dump = json.load(f)
        dump["failures"]["file1.py"] = "whagarbl"
        f.seek(0)
        json.dump(dump, f)

    setdiff("A a.py", "M m.py")
    testmatches(["file2.py", "file3.py"], [], {"file1.py" : "whagarbl"},
                "failures are retained if files aren't explicitly deleted")

    setdiff("D file1.py")
    testmatches(["file2.py", "file3.py"], [], {},
                "failures are removed if the diff says the file was deleted")
