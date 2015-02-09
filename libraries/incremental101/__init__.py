"""
Python module for incrementality in 101worker. Implements the diff protocol used
by the runner to communicate changes to and from modules.

In short: modules receive diff information (added, modified and deleted files)
on their stdin and output their own diff information on stdout. Anything that is
not recognized as a diff line by the runner is assumed to be noise and ignored,
because the existing modules sure are noisy.

See 101worker/tools/runner for more information on the runner side of things.
"""

import json
import os
import re
import sys


instream  = sys.stdin
"""
The stream that diff info is read from, defaults to stdin. Leave this alone in
production, it's only here so that tests can use StringIO instead of stdin.
"""

outstream = sys.stdout
"""
The stream that diff info is written to, defaults to stdout. Same as with
instream, leave it alone.
"""

linesread = 0
"""
How many lines of diff have been read so far. Automatically incremented whenever
nextdiff is called and used in printdiff. Don't modify this.
"""


def eachdiff():
    """
    Generator over nextdiff(), so that you can use a for loop.

    Usage:
        for op, path in eachdiff():
            if   op == "A":
                handle_added_file(path)
            elif op == "M":
                handle_modified_file(path)
            elif op == "D":
                handle_deleted_file(path)

    Or alternatively, you can use functions in a dict:
        switch = {
            "A" : addcallback,
            "M" : modifycallback,
            "D" : deletecallback,
        }
        for op, path in eachdiff():
            switch[op](path)
    """
    diff = nextdiff()
    while diff:
        yield diff
        diff = nextdiff()


def nextdiff():
    """
    Reads the next line from stdin and parses it as a diff. Returns a tuple of
    the operation ("A" for added, "M" for modified and "D" for deleted) as the
    first element and the absolute file path as the second.

    Raises an exception if the line is not a diff. Don't catch this exception,
    it means that the runner is broken and is outputting garbage.
    """
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
    """
    Prints a line of diff, padded by newlines on both ends. If no parameters are
    given, this prints an empty diff with only the diff lines read so far being
    communicated. Otherwise both parameters shall be given, op being the diff
    operation ("A" for an added file, "M" for a modified file and "D" for a
    deleted file" and path being the absolute file path.

    Don't call this directly, use writefile and deletefile instead.
    """
    global linesread
    outstream.write("\n{} {} {}\n".format(linesread, op, path))


def writejson(path, data):
    """
    Converts the given data into canonical JSON and then calls writefile.
    """
    writefile(path, json.dumps(data, sort_keys=True, indent=4,
                               separators=(',', ' : ')) + "\n")


def writefile(path, content):
    """
    Writes the given content to the file at the given path and communicates an
    appropriate diff (added or modified) to the runner. The path is turned into
    an absolute path automatically, if it wasn't absolute already.

    If the file already exists, its content will be compared to the given
    content. If they are equal, the file is not actually written and no modify
    diff is communicated. If the content is different, the old file is
    overwritten with the new content.

    If the file doesn't exist, it is created, obviously. If the directory the
    file is to be put into doesn't exist, it is also created.
    """
    path       = os.path.abspath(path)
    dirname    = os.path.dirname(path)
    oldcontent = None

    if os.path.exists(dirname):
        try:
            with open(path) as f: oldcontent = f.read()
        except IOError:
            pass
    else:
        os.makedirs(os.path.dirname(path))

    if not oldcontent or content != oldcontent:
        with open(path, "w") as f:
            f.write(content)
        printdiff("M" if oldcontent else "A", path)
    else:
        printdiff()


def deletefile(path):
    """
    Deletes the file at the given path and communicates an appropriate delete
    diff to the runner. The path is turned into an absolute path automatically,
    if it wasn't absolute already.

    If the file doesn't exist, nothing happens and no delete diff is
    communicated.
    """
    if os.path.exists(path):
        path = os.path.abspath(path)
        os.unlink(path)
        printdiff("D", path)
    else:
        printdiff()
