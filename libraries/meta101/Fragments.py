"""
Fragments 101rules matches phase.
"""
import re
import json
from   .Phase import Phase


class Fragments(Phase):
    """
    The fragments 101rules matches phase - see Phase. The suffix for this
    phase is ``.fragments.json''.
    """
    suffix = ".fragments.json"


    def applicable(self, rule):
        """
        Returns true if the given rule contains a fragment key.
        """
        return "fragment" in rule


    def keys(self):
        """
        Adds a fragment key to the end of the regular phase's keys.
        """
        return super(Fragments, self).keys() + ["fragment"]


    @staticmethod
    def resolve(uri):
        """
        Resolves the given fragment URI. See fragments documentation on 101docs
        for info about how this URI is built, or tell Martin to write it if it
        isn't there yet.
        """
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
        """
        Attempts to gets the fragment with the given classifier, name and index
        form the given list of fragments. Raises a KeyError if there's no such
        fragment.
        """
        return [f for f in fragments if f["classifier"] == classifier
                                    and f[   "name"   ] == name][index]


    def find(self, resource, pieces, i=0):
        """
        Attempts to find a fragment recursively from the given extractor and
        resolved URI pieces.
        """
        if i >= len(pieces):
            return resource
        gathered = self.gather(resource["fragments"], **pieces[i])
        return self.find(gathered, pieces, i + 1)


    def checkfragment(self, fragment, result, targetbase, **kwargs):
        """
        Checks if the given fragment exists. If it does, it adds the starting
        and ending lines to the result.
        """
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
