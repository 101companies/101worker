from TAP.Simple import *
import meta101

plan(27)

basics = meta101.Basics    ()
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


ok(not basics.applicable(fpredrule), "fpredicate not applicable to basics")
ok(not  preds.applicable(fpredrule), "fpredicate not applicable to predicates")
ok(not  frags.applicable(fpredrule), "fpredicate not applicable to fragments")

ok(not basics.applicable(predrule), "predicate not applicable to basics")
ok(     preds.applicable(predrule), "predicate applicable to predicates")
ok(not  frags.applicable(predrule), "predicate not applicable to fragments")

ok(not basics.applicable(fragrule), "fragment not applicable to basics")
ok(not  preds.applicable(fragrule), "fragment not applicable to predicates")
ok(     frags.applicable(fragrule), "fragment applicable to fragments")


for rule in normalrules:
    ok(basics.applicable(rule),
       "{} applicable to basics".format(rule.keys()[0]))
    ok(not preds.applicable(rule),
       "{} not applicable to predicates".format(rule.keys()[0]))
    ok(not frags.applicable(rule),
       "{} not applicable to fragments".format(rule.keys()[0]))


ok(not basics.applicable(monsterrule), "combined rule not applicable to basics")
ok(     preds.applicable(monsterrule), "combined rule applicable to predicates")
ok(     frags.applicable(monsterrule), "combined rule applicable to fragments")
