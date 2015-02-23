from TAP.Simple import *
import meta101

plan(5)


class TestPhase(meta101.Phase):

    def keys(self):
        return ["stuff"]

    def suffix(self):
        return ".test.json"

    def applicable(self, rule):
        return "ignorme" not in rule

    def checkstuff(self, stuff, result, add, **kwargs):
        result["stuff"] = stuff + add
        return add

phase = TestPhase()


is_ok(phase.match({"ignorme" : 123}), None, "non-applicable rule ignored")

eq_ok(phase.match({}), {},
      "empty rule creates just empty result")
eq_ok(phase.match({"a" : 0, "b" : 1}), {},
      "rule without checkable constraints creates empty result")


is_ok(phase.match({"stuff" : 123}, add=0), None,
      "if a constraint function returns false None is returned")
eq_ok(phase.match({"stuff" : 123}, add=1), {"stuff" : 124},
      "if all constraint functions return true result is returned")
