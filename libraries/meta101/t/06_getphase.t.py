from TAP.Simple import *
import meta101
execfile("t/dies_ok.py")

plan(4)


dies_ok(lambda: meta101.getphase("a"), "invalid phase dies")


ok(meta101.getphase("matches")    is meta101.Matches,
      "matches phase class instantiated")
ok(meta101.getphase("predicates") is meta101.Predicates,
   "predicates phase class instantiated")
ok(meta101.getphase("fragments")  is meta101.Fragments,
    "fragments phase class instantiated")
