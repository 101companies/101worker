from TAP.Simple import *
import meta101

plan(3)

eq_ok(meta101.Matches   .suffix,    ".matches.json",    "matches suffix")
eq_ok(meta101.Predicates.suffix, ".predicates.json", "predicates suffix")
eq_ok(meta101.Fragments .suffix,  ".fragments.json",  "fragments suffix")
