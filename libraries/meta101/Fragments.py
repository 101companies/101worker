import os
import json
import subprocess
import warnings
import kludge101
from   .Phase     import Phase
from   .Matches   import Matches
from   .util      import tolist


class Fragments(Phase):
    suffix = ".fragments.json"


    def __init__(self, *args):
        super(Fragments, self).__init__(*args)
        self.locators = set()


    def dump(self):
        dump = super(Fragments, self).dump()
        dump["locators"] = list(self.locators)
        return dump


    def applicable(self, rule):
        return "fragment" in rule


    def findlocator(self, matchespath):
        with open(matchespath) as f:
            matches = json.load(f)

        for match in matches:
            if "locator" in match["metadata"]:
                return match["metadata"]["locator"]

        raise ValueError("locator not found")


    def runlocator(self, locator, fragment, rule, filename, tempin, tempout):
        args     = tolist(rule["args"]) if "args" in rule else []
        command  = [locator] + args + [filename, tempin, tempout]

        with open(tempin, 'w') as f:
            if type(fragment) is str:
                f.write(str)
            else:
                json.dump(fragment, f)

        subprocess.check_call(command)

        with open(tempout) as f:
            return json.load(f)


    def checkfragment(self, fragment, rule, relative,
                      filename, result, targetbase, **kwargs):
        # XXX: temporary files are dumb, it'd be much better if locators just
        #      took their input via stdin and output their results via stdout
        temppath = os.path.join(os.environ["temps101dir"],
                                relative.replace("/", "-"))
        tempin   = temppath + ".in"
        tempout  = temppath + ".out"

        try:
            found   = self.findlocator(targetbase + Matches.suffix)
            # FIXME: move locators into 101worker
            locator = kludge101.checkpath(found)
            if not locator:
                raise RuntimeError("foiled code injection: {}".format(found))
            self.locators.add(locator)

            result["lines"] = self.runlocator(locator, fragment, rule,
                                              filename, tempin, tempout)
        except Exception as e:
            self.failures.append({"error" : str(e), "rule" : rule})
        finally:
            for f in [tempin, tempout]:
                if os.path.exists(f):
                    try:
                        os.unlink(f)
                    except Exception as e:
                        warnings.warn("Can't unlink {}: {}".format(f, e))

        return "lines" in result
