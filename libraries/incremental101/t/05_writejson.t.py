from TAP.Simple import *
import incremental101 as inc

plan(2)


def dies_ok(code, message=None):
    try:
        code()
    except Exception as e:
        exception = e
    else:
        exception = None
    ok(exception, message)


# only writejson is tested here, writefile is patched out
def monkeypatch(*args):
    global called
    called = list(args)

inc.writefile = monkeypatch


inc.writejson("path", {
    "list"   : [1, 2, 3],
    "string" : "string!",
    "float"  : 0.23,
    "other"  : {
        "True"  : True,
        "False" : False,
        "None"  : None,
    },
})

want = """{
    "float" : 0.23,
    "list" : [
        1,
        2,
        3
    ],
    "other" : {
        "False" : false,
        "None" : null,
        "True" : true
    },
    "string" : "string!"
}
"""

eq_ok(called, ["path", want], "data fit for json serializes correctly")


dies_ok(lambda: inc.writejson("whatever", [1, 2, set("not", "json")]),
        "serialize a set (which doesn't exist in json) dies")
