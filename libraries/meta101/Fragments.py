from .Phase import Phase


class Fragments(Phase):


    def __init__(self, *args):
        super(Fragments, self).__init__(*args)
        self.locators = set()


    def dump(self):
        dump = super(Fragments, self).dump()
        dump["locators"] = list(self.locators)
        return dump


    def suffix(self):
        return ".fragments.json"


    def applicable(self, rule):
        return "fragment" in rule
