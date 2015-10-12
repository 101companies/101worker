import os
from TAP.Simple   import *
from meta101.util import sourcetotarget
execfile("t/dies_ok.py")

plan(4)


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
