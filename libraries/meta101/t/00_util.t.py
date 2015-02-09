import os
from TAP.Simple   import *
from meta101.util import *

plan(13)

def dies_ok(code, message=None):
    try:
        code()
    except Exception as e:
        exception = e
    else:
        exception = None
    ok(exception, message)


# stripregex

is_ok(stripregex( "thing" ), None,    "stripregex 'thing' does nothing")
is_ok(stripregex("#thing" ), None,    "stripregex '#thing' does nothing")
is_ok(stripregex( "thing#"), None,    "stripregex 'thing#' does nothing")
eq_ok(stripregex("#thing#"), "thing", "stripregex '#thing#' returns 'thing'")

eq_ok(stripregex( "thing",  123), 123,
      "stripregex 'thing' with default returns the default")
eq_ok(stripregex("#thing#", 123), "thing",
      "stripregex '#thing#' with default returns 'thing'")


# tolist

eq_ok(tolist( "thing" ), ["thing"], "single thing tolist becomes a list")
eq_ok(tolist(["thing"]), ["thing"], "list tolist remains the same")


# sourcetotarget

dies_ok(lambda: sourcetotarget("whatever"),
        "missing environment variables in sourcetotarget dies")

os.environ["repo101dir"   ] = "/path/repo"
os.environ["targets101dir"] = "/path/targets"

eq_ok(sourcetotarget("/path/repo/dir/file"), "/path/targets/dir/file",
      "sourcetotarget for repo path rewrites to targets path")

dies_ok(lambda: sourcetotarget("/path/notrepo/dir/file"),
        "non-repo path dies")

eq_ok(sourcetotarget("/path/repo/dir/path/repo/file"),
      "/path/targets/dir/path/repo/file", "repo path is only replaced once")

del os.environ["repo101dir"   ]
del os.environ["targets101dir"]

eq_ok(sourcetotarget("/path/repo/dir/file"), "/path/targets/dir/file",
      "environment variables are cached")
