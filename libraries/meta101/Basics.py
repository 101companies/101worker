from .Phase import Phase


class Basics(Phase):

    def suffix(self):
        return ".matches.json"


    def applicable(self, rule):
        return Phase.applicable(self, rule) \
           and not "predicate" in rule      \
           and not "fragment"  in rule
