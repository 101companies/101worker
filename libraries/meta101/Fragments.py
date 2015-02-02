from .Phase import Phase


class Fragments(Phase):


    def suffix(self):
        return ".fragments.json"


    def applicable(self, rule):
        return "fragment" in rule
