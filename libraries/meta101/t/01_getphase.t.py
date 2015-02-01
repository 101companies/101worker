from TAP.Simple import *
import meta101

plan(4)


def dies_ok(code, message=None):
    try:
        code()
    except Exception as e:
        exception = e
    else:
        exception = None
    ok(exception, message)

dies_ok(lambda: meta101.getphase("a"), "invalid phase dies")


basics     = meta101.getphase("basics"    )
predicates = meta101.getphase("predicates")
fragments  = meta101.getphase("fragments" )

ok(basics     is meta101.Basics,         "basics phase class")
ok(predicates is meta101.Predicates, "predicates phase class")
ok(fragments  is meta101.Fragments,   "fragments phase class")
