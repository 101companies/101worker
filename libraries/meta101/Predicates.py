"""
Predicates 101rules matches phase.
"""
import imp
import os
import re
from   .Phase import Phase
from   .util  import tolist


class Predicates(Phase):
    """
    The predicates 101rules matches phase - see Phase. The suffix for this
    phase is ``.predicates.json''.
    """
    suffix = ".predicates.json"
    regex  = re.compile(r"^\w+$")


    def __init__(self, *args):
        """
        Adds a set of predicates to the regular phase.
        """
        super(Predicates, self).__init__(*args)
        self.predicates = set()


    def dump(self):
        """
        Converts the set of predicates into a list and adds it to the dump.
        """
        dump = super(Predicates, self).dump()
        dump["predicates"] = sorted(list(self.predicates))
        return dump


    def applicable(self, rule):
        """
        Returns true if the given rule contains a predicate key.
        """
        return "predicate" in rule


    def keys(self):
        """
        Adds a predicate key to the end of the regular phase's keys.
        """
        return super(Predicates, self).keys() + ["predicate"]


    def checkpredicate(self, predicate, rule, filename, **kwargs):
        """
        TODO: Freddy & Thies changed this, so they can document.
        """
        if not self.regex.match(predicate):
            raise ValueError("weird predicate name: " + predicate)

        args = tolist(rule["args"]) if "args" in rule else []
        path = os.path.join(os.environ["predicates101dir"],
                            predicate, "predicate.py")

        self.predicates.add(predicate)

        module = imp.load_source("PREDICATE_" + predicate, path)
        return module.run(filename, *args)
