from TAP.Simple import *
import json
import os
import shutil
import StringIO
import incremental101 as inc
from meta101          import derive
from meta101.resource import File, Json
execfile("t/dies_ok.py")
execfile("t/tempdir.py")

plan(21)


tmp                         = tempdir()
repo                        = os.path.abspath("t/derive/repo")
targets                     = os.path.join(tmp, "resources")
os.environ[   "repo101dir"] = repo
os.environ["targets101dir"] = targets
shutil.copytree("t/derive/resources", targets)


def reset(*lines):
    inc.instream  = StringIO.StringIO("".join([line + "\n" for line in lines]))
    inc.outstream = StringIO.StringIO()

def file_ok(dir, file, want, name):
    try:
        with open(os.path.join(dir, file)) as f:
            if type(want) is str:
                eq_ok(f.read(), want, name)
            else:
                eq_ok(json.load(f), want, name)
    except Exception as e:
        ok(False, "{} ({}: {})".format(name, e.__class__.__name__, e))


def derivelanguage(deriver, language, **kwargs):
    if language == "Java":
        raise ValueError("Blech")
    return language


reset()
lives_ok(lambda: derive(suffix  =".lang",
                        dump    =os.path.join(tmp, "lang.json"),
                        callback=derivelanguage,
                        getvalue="key"),
         "empty input runs ok")

file_ok(tmp, "lang.json", {"problems" : {}}, "...new, empty dump is created")


reset()
lives_ok(lambda: derive(suffix    =".lang",
                        dump      =os.path.join(tmp, "lang.json"),
                        callback  =derivelanguage,
                        getvalue  ="language",
                        entirerepo=True),
         "simple language derivation over entire repo")

file_ok(tmp, "lang.json", {"problems" : {"java" : "Blech"}},
        "...dump is modified with exceptions raised in callback")

for lang in ["perl", "python"]:
    cap = lang.capitalize()
    file_ok(targets, lang + ".lang", cap,
            "...{} derives to {}".format(lang, cap))

for lang in ["java", "other"]:
    ok(not os.path.exists(os.path.join(targets, lang + ".lang")),
       "...{} is not derived".format(lang))


with open(os.path.join(targets, "other.matches.json"), "w") as f:
    json.dump([{"metadata" : {"language" : "Other"}}], f)
with open(os.path.join(targets,  "perl.matches.json"), "w") as f:
    json.dump([{"metadata" : {"language" : "Perl 5"}}], f)

reset("D " + os.path.join(repo,    "java"),
      "D " + os.path.join(repo,    "python"),
      "M " + os.path.join(targets, "other.matches.json"))

lives_ok(lambda: derive(suffix    =".lang",
                        dump      =os.path.join(tmp, "lang.json"),
                        callback  =derivelanguage,
                        getvalue  ="language"),
         "language derivation with diff input")

file_ok(tmp, "lang.json", {"problems" : {}}, "...dump is modified correctly")

file_ok(targets, "perl.lang",  "Perl",  "...file not in diff is not touched")
file_ok(targets, "other.lang", "Other", "...modified file is re-derived")

ok(not os.path.exists(os.path.join(targets, "python.lang")),
   "...python.lang is deleted as per diff")
ok(not os.path.exists(os.path.join(targets,   "java.lang")),
   "...java.lang is still not derived")


def oninit(deriver):
    deriver.dump["handled"] = set(deriver.dump.get("handled", []))

def ondump(deriver):
    deriver.dump["handled"] = sorted(list(deriver.dump["handled"]))

def getmore(deriver, resources, **kwargs):
    return {
        "meta" : resources[0][0]["metadata"],
        "lang" : os.path.basename(resources[1]),
    }

def derivemore(deriver, value, relative, **kwargs):
    deriver.dump["handled"].add(relative)
    return (value, None if value["lang"] == "other.lang" else value["lang"])


reset()
lives_ok(lambda: derive(suffix    =[".lang.json", ".more"],
                        resources =[Json(".matches.json"), File(".lang")],
                        oninit    =oninit,
                        ondump    =ondump,
                        dump      =os.path.join(tmp, "more.json"),
                        getvalue  =getmore,
                        callback  =derivemore,
                        entirerepo=True),
         "derivation with all bells and whistles")

file_ok(tmp, "more.json", {
            "handled"  : ["other", "perl"],
            "problems" : {},
        }, "...dump result is correct")

file_ok(targets, "perl.lang.json", {
            "lang" : "perl.lang",
            "meta" : {"language" : "Perl 5"},
        }, "...perl.lang.json derived correctly")

file_ok(targets, "perl.more", "perl.lang",
           "...perl.more derived correctly")

file_ok(targets, "other.lang.json", {
            "lang" : "other.lang",
            "meta" : {"language" : "Other"},
        }, "...other.lang.json derived correctly")

ok(not os.path.exists(os.path.join(targets, "other.more")),
   "...returning None does not derive file")


reset("M " + os.path.join(targets, "other.lang"))

ex = getexcept(lambda: derive(suffix    =[".lang.json", ".more"],
                              resources =[Json(".matches.json"), File(".lang")],
                              oninit    =oninit,
                              ondump    =ondump,
                               dump      =os.path.join(tmp, "more.json"),
                              getvalue  =getmore,
                              callback  =lambda *args, **kwargs: "wrong"))
is_ok(type(ex), SystemExit, "wrong tuple size from callback raises SystemExit")
