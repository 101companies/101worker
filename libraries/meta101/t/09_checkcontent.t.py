from TAP.Simple import *
import os
import meta101
execfile("t/dies_ok.py")

plan(5)

phase = meta101.Matches()


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
