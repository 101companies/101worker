from TAP.Simple import *
import incremental101 as inc

plan(2)

# we don't test nextdiff here
def monkeypatch():
    global counter
    counter -= 1       # Python doesn't have counter--,
    return counter + 1 # so this hack will have to do.

inc.nextdiff = monkeypatch


counter = 5
values  = [diff for diff in inc.eachdiff()]
eq_ok(values, [5, 4, 3, 2, 1], "eachdiff iterates over nextdiff's values")


counter = 0
values  = [diff for diff in inc.eachdiff()]
eq_ok(values, [], "eachdiff with no values yields no values")
