from TAP.Simple import *
import os
import meta101

plan(42)


using1      = "t/predicates/using1"
using2      = "t/predicates/using2"
nonexistent = "t/predicates/nonexistent-file"

os.environ["repo101dir"] = os.getcwd()
os.environ["predicates101dir"] = os.path.abspath("t/predicates")
os.environ["predicates101deps"] =  os.path.abspath("t/worker/predicates101meta/module.json")

phase = meta101.Predicates()


def testpredicate(comment, rule, success, predicates, failures, filename=None):
    if not filename:
        filename = "file{}-{}-{}-{}".format(rule, success, predicates, failures)

    result = phase.match(rule, filename=filename, relative=filename)
    ok(result is not None, comment) if success else ok(result is None, comment)
    eq_ok(len(phase.predicates), predicates,
          "...predicate count is {}".format(predicates))
    eq_ok(len(phase.failures),   failures,
          "...failure count is {}"  .format(failures))


rule = {"predicate" : "noargs"}
testpredicate("no arguments predicate matches with no arguments", rule,
              success=True, predicates=1, failures=0)

rule["args"] = []
testpredicate("no arguments predicate matches with empty arguments", rule,
              success=True, predicates=1, failures=0)

rule["args"] = [1, 2 ,3]
testpredicate("no arguments predicate doesn't match with arguments", rule,
              success=False, predicates=1, failures=0)


rule   = {"predicate" : "using", "args" : "somelib"}
testpredicate("dotNet predicate fails with nonexistent file", rule,
              success=False, predicates=2, failures=1, filename=nonexistent)


testpredicate("dotNet predicate doesn't match 'somelib' on using1", rule,
              success=False, predicates=2, failures=1, filename=using1)
#Fail
testpredicate("dotNet predicate matches 'somelib' on using2", rule,
              success=True, predicates=2, failures=1, filename=using2)


rule["args"] = ["otherlib"]
testpredicate("dotNet predicate matches 'otherlib' on using1", rule,
              success=True, predicates=2, failures=1, filename=using1)

testpredicate("dotNet predicate doesn't match 'otherlib' on using2", rule,
              success=False, predicates=2, failures=1, filename=using2)

#Fail
rule["args"] = ["somelib", "otherlib"]
testpredicate("dotNet predicate matches both libs on using1", rule,
              success=True, predicates=2, failures=1, filename=using1)

testpredicate("dotNet predicate matches both libs on using2", rule,
              success=True, predicates=2, failures=1, filename=using2)


rule  = {"predicate" : "missing"}
testpredicate("match nonexistent predicate fails", rule,
              success=False, predicates=2, failures=2)

rule  = {"predicate" : "wrongname"}
testpredicate("match predicate not called predicate.py fails", rule,
              success=False, predicates=3, failures=3)

rule  = {"predicate" : "../weird"}
testpredicate("non-alphanumeric predicate name is rejected", rule,
              success=False, predicates=3, failures=4)

rule  = {"predicate" : "moduledep"}
testpredicate("non-alphanumeric predicate name is rejected", rule,
              success=False, predicates=3, failures=4)
#