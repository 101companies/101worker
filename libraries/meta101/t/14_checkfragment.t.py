#from TAP.Simple        import *
from TestMore import *
from meta101.Fragments import Fragments
#execfile("t/dies_ok.py")

plan(14)
fragments = Fragments()
java      = "t/fragments/Employee.java"

def test(f, t, start=None, end=None, name=None):
    got = fragments.checkfragment(fragment=f, result={}, targetbase=t)
    if start is None:
        is_ok(got, None, end)
    else:
        eq_ok(got, {"lines" : {"from" : start, "to" : end}}, name)


dies_ok(lambda: test("what/ever", "nonexistent"), "nonexistent extractor dies")
dies_ok(lambda: test("",           java        ), "invalid uri dies")


test("class/Employee",   java, 7, 78, "class found")
test("class/Employee/0", java, 7, 78, "indexed class found")
test("class/Company",    java, None,  "wrong class not found")
test("class/Employee/1", java, None,  "wrongly indexed class not found")
test("class/Company/1",  java, None,  "wrongly indexed wrong class not found")

test("class/Employee/method/toString",   java, 50, 60, "method found")
test("class/Employee/method/toString/0", java, 50, 60, "indexed method found")
test("class/Employee/method/toStrong",   java, None,   "wrong method not found")
test("class/Employee/method/toString/9", java, None,
     "wrongly indexed method not found")

test("class/Company/method/toString", java, None,
     "wrong class won't find method")
test("class/Employee/12/method/toString", java, None,
     "wrong index won't find method")

test("class/Employee/method/setAddress/argument/address", java, None,
     "nonexistent fragment piece leads to not found")
