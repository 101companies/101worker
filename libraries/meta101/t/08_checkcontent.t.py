from TAP.Simple import *
import os
import meta101

plan(5)

phase = meta101.Basics()


def dies_ok(code, message=None):
    try:
        code()
    except Exception as e:
        exception = e
    else:
        exception = None
    ok(exception, message)

dies_ok(lambda: phase.checkcontent("irrelevant", "nonexistent"),
        "nonexistent file dies")


ok(    phase.checkcontent( "test:\s*\n\t.+",  "Makefile"),
       "match with normal pattern")
ok(not phase.checkcontent( "asdf:\s*\n\t.+",  "Makefile"),
       "mismatch with normal pattern")
ok(    phase.checkcontent("#test:\s*\n\t.+#", "Makefile"),
       "match with # around pattern")
ok(not phase.checkcontent("#asdf:\s*\n\t.+#", "Makefile"),
       "mismatch with # around pattern")
