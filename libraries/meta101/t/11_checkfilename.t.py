from TAP.Simple import *
import meta101

plan(24)

phase = meta101.Matches()


for what in ["filename", "basename", "dirname"]:
    check = getattr(phase, "check" + what)

    ok(    check( "dir/file",           "dir/file"), what + " match string")
    ok(    check(             "#dir#",  "dir/file"), what + " match pattern")
    ok(    check(["dir/file", "#dia#"], "dir/file"),
                    what + " match list element 1")
    ok(    check(["dia/file", "#dir#"], "dir/file"),
                    what + " match list element 2")
    ok(    check(["dir/file", "#dir#"], "dir/file"),
                what + " match both list elements")

    ok(not check( "dir/file",           "dia/file"), what + " mismatch string")
    ok(not check(             "#dir#",  "dia/file"), what + " mismatch pattern")
    ok(not check(["dir/file", "#dir#"], "dia/file"), what + " mismatch list")
