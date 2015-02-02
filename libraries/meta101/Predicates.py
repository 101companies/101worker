from .Phase import Phase


class Predicates(Phase):


    def suffix(self):
        return ".predicates.json"


    def applicable(self, rule):
        return "predicate" in rule
