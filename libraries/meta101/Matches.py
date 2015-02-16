from .Phase import Phase


class Matches(Phase):
    suffix = ".matches.json"


    def applicable(self, rule):
        # XXX probably better to use a whitelist approach
        return all(key not in rule for key in
                  ("fpredicate", "predicate", "fragment"))
