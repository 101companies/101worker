from .Phase import Phase


class Basics(Phase):


    def suffix(self):
        return ".matches.json"


    def applicable(self, rule):
        return all(key not in rule for key in
                  ("fpredicate", "predicate", "fragment"))
