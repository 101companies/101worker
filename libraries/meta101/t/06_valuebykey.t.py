from   TAP.Simple   import *
import meta101
from   meta101.util import valuebykey
execfile("t/dies_ok.py")

plan(4)

matches = []
dies_ok(lambda: valuebykey("key", matches), "empty matches given dies")


matches = [
    {
        "metadata" : {
            "otherkey" : "whatever",
            "another"  : "not used",
        },
    },
    {
        "metadata" : {
            "somekey"  : "somevalue",
        },
    },
]

dies_ok(lambda: valuebykey("key", matches), "no values found dies")


findme = {
    "metadata" : {
        "key"      : "this is found",
        "otherkey" : "othervalue",
    },
}
matches.append(findme)

eq_ok(valuebykey("key", matches), "this is found", "single value is found")


matches.append({
    "metadata" : {
        "key" : "this comes too late",
    },
})

eq_ok(valuebykey("key", matches), "this is found",
      "only first value of multiple is ever found")
