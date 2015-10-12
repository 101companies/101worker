from TAP.Simple   import *
from meta101.util import tolist

plan(3)


eq_ok(tolist( "thing" ),  ["thing"],  "single thing tolist becomes a list")
eq_ok(tolist(["thing"]),  ["thing"],  "list tolist remains the same")
eq_ok(tolist({"thing"}), [{"thing"}], "anything else also gets put in a list")
