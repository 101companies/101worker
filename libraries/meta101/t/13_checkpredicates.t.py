from TAP.Simple import *
import os
import meta101

plan(33)

os.environ["repo101dir"] = os.getcwd()
pdir        = "t/predicates/"
noargs      = pdir + "noargs.py"
using       = pdir + "using.py"
using1      = pdir + "using1"
using2      = pdir + "using2"
nonexistent = pdir + "nonexistent-file"
phase       = meta101.Predicates()

def testpredicate(comment, rule, success, predicates, failures,
                  filename="whatever"):
    result = phase.match(rule, filename=filename)
    ok(result is not None, comment) if success else ok(result is None, comment)
    eq_ok(len(phase.predicates), predicates,
          "...predicate count is {}".format(predicates))
    eq_ok(len(phase.failures),   failures,
          "...failure count is {}"  .format(failures))


rule = {"predicate" : noargs}
testpredicate("no arguments predicate matches with no arguments", rule,
              success=True, predicates=1, failures=0)

rule["args"] = []
testpredicate("no arguments predicate matches with empty arguments", rule,
              success=True, predicates=1, failures=0)

rule["args"] = [1, 2 ,3]
testpredicate("no arguments predicate doesn't match with arguments", rule,
              success=False, predicates=1, failures=0)


rule   = {"predicate" : using, "args" : "somelib"}
testpredicate("dotNet predicate fails with nonexistent file", rule,
              success=False, predicates=2, failures=1, filename=nonexistent)


testpredicate("dotNet predicate doesn't match 'somelib' on using1", rule,
              success=False, predicates=2, failures=1, filename=using1)

testpredicate("dotNet predicate matches 'somelib' on using2", rule,
              success=True, predicates=2, failures=1, filename=using2)


rule["args"] = ["otherlib"]
testpredicate("dotNet predicate matches 'otherlib' on using1", rule,
              success=True, predicates=2, failures=1, filename=using1)

testpredicate("dotNet predicate doesn't match 'otherlib' on using2", rule,
              success=False, predicates=2, failures=1, filename=using2)


rule["args"] = ["somelib", "otherlib"]
testpredicate("dotNet predicate matches both libs on using1", rule,
              success=True, predicates=2, failures=1, filename=using1)

testpredicate("dotNet predicate matches both libs on using2", rule,
              success=True, predicates=2, failures=1, filename=using2)


rule  = {"predicate" : nonexistent}
testpredicate("match nonexistent predicate fails", rule,
              success=False, predicates=3, failures=2)
