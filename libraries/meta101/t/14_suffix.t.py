from TAP.Simple import *
import meta101

plan(3)

eq_ok(meta101.Basics    ().suffix(),    ".matches.json",     "basics suffix")
eq_ok(meta101.Predicates().suffix(), ".predicates.json", "predicates suffix")
eq_ok(meta101.Fragments ().suffix(),  ".fragments.json",  "fragments suffix")
