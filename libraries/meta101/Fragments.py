import re
import json
from   .Phase import Phase


class Fragments(Phase):
    suffix = ".fragments.json"


    def __init__(self, *args):
        super(Fragments, self).__init__(*args)


    def applicable(self, rule):
        return "fragment" in rule


    def keys(self):
        return super(Fragments, self).keys() + ["fragment"]


    @staticmethod
    def resolve(uri):
        split  = uri.split("/")
        pieces = []
        i      = 0

        while i < len(split):
            piece = {
                "classifier" : split[  i  ],
                "name"       : split[i + 1],
            }

            if i + 2 < len(split) and re.match(r"\d+", split[i + 2]):
                piece["index"] = int(split[i + 2])
                i += 3
            else:
                piece["index"] = 0
                i += 2

            pieces.append(piece)

        return pieces


    @staticmethod
    def gather(fragments, classifier, name, index):
        return [f for f in fragments if f["classifier"] == classifier
                                    and f[   "name"   ] == name][index]


    def find(self, resource, pieces, i=0):
        if i >= len(pieces):
            return resource
        gathered = self.gather(resource["fragments"], **pieces[i])
        return self.find(gathered, pieces, i + 1)


    def checkfragment(self, fragment, result, targetbase, **kwargs):
        with open(targetbase + ".extractor.json") as f:
            extractor = json.load(f)
        pieces = self.resolve(fragment)

        try:
            found = self.find(extractor, pieces)
        except LookupError:
            return None

        result["lines"] = {
            "from" : found["startLine"],
            "to"   : found[  "endLine"],
        }
        return result
