from TAP.Simple import *
import meta101

plan(27)

matches = meta101.Matches  ()
preds  = meta101.Predicates()
frags  = meta101.Fragments ()

fpredrule   = {"fpredicate" : "whatever"}
predrule    = {"predicate"  : "whatever"}
fragrule    = {"fragment"   : "whatever"}

normalrules = [
    {"suffix"   : "whatever"},
    {"content"  : "whatever"},
    {"filename" : "whatever"},
    {"basename" : "whatever"},
    {"dirname"  : "whatever"},
]

items = fpredrule.items() + predrule.items() + fragrule.items()
for rule in normalrules:
    items += rule.items()
monsterrule = dict(items)


ok(not matches.applicable(fpredrule), "fpredicate not applicable to matches")
ok(not  preds.applicable(fpredrule), "fpredicate not applicable to predicates")
ok(not  frags.applicable(fpredrule), "fpredicate not applicable to fragments")

ok(not matches.applicable(predrule), "predicate not applicable to matches")
ok(     preds.applicable(predrule), "predicate applicable to predicates")
ok(not  frags.applicable(predrule), "predicate not applicable to fragments")

ok(not matches.applicable(fragrule), "fragment not applicable to matches")
ok(not  preds.applicable(fragrule), "fragment not applicable to predicates")
ok(     frags.applicable(fragrule), "fragment applicable to fragments")


for rule in normalrules:
    ok(matches.applicable(rule),
       "{} applicable to matches".format(rule.keys()[0]))
    ok(not preds.applicable(rule),
       "{} not applicable to predicates".format(rule.keys()[0]))
    ok(not frags.applicable(rule),
       "{} not applicable to fragments".format(rule.keys()[0]))


ok(not matches.applicable(monsterrule), "combined rule not applicable to matches")
ok(     preds.applicable(monsterrule), "combined rule applicable to predicates")
ok(     frags.applicable(monsterrule), "combined rule applicable to fragments")
