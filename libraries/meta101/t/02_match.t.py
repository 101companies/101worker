from TAP.Simple import *
import meta101

plan(5)


class TestPhase(meta101.Phase):

    def suffix(self):
        return ".test.json"

    def applicable(self, rule):
        return "ignorme" not in rule

    def checkstuff(self, stuff, result, add, **kwargs):
        result["stuff"] = stuff + add
        return add

phase = TestPhase({})


is_ok(phase.match(0, {"ignorme" : 123}), None, "non-applicable rule ignored")

eq_ok(phase.match(1, {}), {"id" : 1},
      "empty rule creates just id result")
eq_ok(phase.match(2, {"a" : 0, "b" : 1}), {"id" : 2},
      "rule without checkable constraints creates just id result")


is_ok(phase.match(3, {"stuff" : 123}, add=0), None,
      "if a constraint function returns false None is returned")
eq_ok(phase.match(4, {"stuff" : 123}, add=1), {"id" : 4, "stuff" : 124},
      "if all constraint functions return true result is returned")
