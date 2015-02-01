from TAP.Simple   import *
from meta101.util import stripregex, tolist

plan(8)


is_ok(stripregex( "thing" ), None,    "stripregex thing does nothing")
is_ok(stripregex("#thing" ), None,    "stripregex #thing does nothing")
is_ok(stripregex( "thing#"), None,    "stripregex thing# does nothing")
eq_ok(stripregex("#thing#"), "thing", "stripregex #thing# returns thing")

eq_ok(stripregex( "thing",  123), 123,
      "stripregex thing with default returns the default")
eq_ok(stripregex("#thing#", 123), "thing",
      "stripregex thing with default returns thing")


eq_ok(tolist( "thing" ), ["thing"], "single thing tolist becomes a list")
eq_ok(tolist(["thing"]), ["thing"], "list tolist remains the same")
