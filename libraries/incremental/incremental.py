import os
import re
import sys


instream  = sys.stdin
outstream = sys.stdout
linesread = 0


def nextdiff():
    line = instream.readline()
    if not line:
        return None
    line = line.strip()

    match = re.match("([AMD])\s+(.+)", line)
    if not match:
        raise Exception("Line read is not a diff: {}".format(line))

    global linesread
    linesread += 1
    return match.group(1, 2)


def printdiff(op="-", path="-"):
    global linesread
    outstream.write("{} {} {}\n".format(linesread, op, path))


def writefile(path, content):
    oldcontent = None
    try:
        with open(path) as f: oldcontent = f.read()
    except IOError:
        pass

    if not oldcontent or content != oldcontent:
        with open(path, "w") as f: f.write(content)
        printdiff("M" if oldcontent else "A", path)
    else:
        printdiff()


def deletefile(path):
    if os.path.exists(path):
        os.unlink(path)
        printdiff("D", path)
    else:
        printdiff()
