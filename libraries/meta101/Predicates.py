import imp
import os
import re
from   .Phase import Phase
from   .util  import tolist


class Predicates(Phase):
    suffix = ".predicates.json"
    regex  = re.compile("^\w+$")


    def __init__(self, *args):
        super(Predicates, self).__init__(*args)
        self.predicates = set()


    def dump(self):
        dump = super(Predicates, self).dump()
        dump["predicates"] = list(self.predicates)
        return dump


    def applicable(self, rule):
        return "predicate" in rule


    def keys(self):
        return super(Predicates, self).keys() + ["predicate"]


    def checkpredicate(self, predicate, key, rule, filename, **kwargs):
        if not self.regex.match(predicate):
            raise ValueError("weird predicate name: " + predicate)

        args = tolist(rule["args"]) if "args" in rule else []
        path = os.path.join(os.environ["predicates101dir"],
                            predicate, "predicate.py")

        self.predicates.add(predicate)

        module = imp.load_source("PREDICATE_" + predicate, path)
        return module.run(filename, *args)
