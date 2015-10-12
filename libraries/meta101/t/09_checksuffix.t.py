from TAP.Simple import *
import meta101

plan(6)

phase = meta101.Matches()


ok(    phase.checksuffix( ".py",              "a.py"), "match suffix")
ok(not phase.checksuffix( ".py",              "a.pm"), "mismatch suffix")
ok(    phase.checksuffix([".py"],             "b.py"), "match suffix list")
ok(not phase.checksuffix([".py"],             "b.pm"), "mismatch suffix list")
ok(    phase.checksuffix([".py", ".c", ".o"], "c.py"), "match suffixes list")
ok(not phase.checksuffix([".py", ".c", ".o"], "c.pm"), "mismatch suffixes list")
