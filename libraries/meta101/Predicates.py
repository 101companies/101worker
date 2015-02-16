import imp
import os
import kludge101
from   .Phase import Phase
from   .util  import tolist


class Predicates(Phase):
    suffix = ".predicates.json"


    def __init__(self, *args):
        super(Predicates, self).__init__(*args)
        self.predicates = set()


    def dump(self):
        dump = super(Predicates, self).dump()
        dump["predicates"] = list(self.predicates)
        return dump


    def applicable(self, rule):
        return "predicate" in rule


    def checkpredicate(self, predicate, key, rule, filename, **kwargs):
        args = tolist(rule["args"]) if "args" in rule else []

        # XXX: move predicates into 101worker
        path = kludge101.checkpath(predicate)
        if not path:
            self.failures.append({
                "error" : "foiled code injection: {}".format(predicate),
                "key"   : key,
                "rule"  : rule,
            })
            return None

        self.predicates.add(predicate)

        try:
            # Python cries about a missing parent module if the name contains
            # dots, so we just replace them with underscores to make it happy.
            module = imp.load_source(predicate.replace(".", "_"), path)
            return module.run(args=args, filePath=filename)
        except Exception as e:
            self.failures.append({
                "error" : str(e),
                "key"   : key,
                "rule"  : rule,
            })
        return None
