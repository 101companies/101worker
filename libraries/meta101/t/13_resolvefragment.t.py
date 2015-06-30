from TAP.Simple        import *
from meta101.Fragments import Fragments
execfile("t/dies_ok.py")

plan(9)
resolve = Fragments.resolve


dies_ok(lambda: resolve(""), "empty uri dies")
dies_ok(lambda: resolve("wrong"), "wrong number of pieces dies")
dies_ok(lambda: resolve("no/pe/-1"), "negative indices don't work")


eq_ok(resolve("method/companies101.Company.prototype.cut"),
      [{
          "classifier" : "method",
          "name"       : "companies101.Company.prototype.cut",
          "index"      : 0,
      }], "uri with a single piece and no index")

eq_ok(resolve("class/Cut/method/cut"),
      [{
          "classifier" : "class",
          "name"       : "Cut",
          "index"      : 0,
      }, {
          "classifier" : "method",
          "name"       : "cut",
          "index"      : 0,
      }], "uri with two pieces and no indices")

eq_ok(resolve("predicate/cut/5"),
      [{
          "classifier" : "predicate",
          "name"       : "cut",
          "index"      : 5,
      }], "uri with a single piece and index")

eq_ok(resolve("predicate/cut/5/some/thing"),
      [{
          "classifier" : "predicate",
          "name"       : "cut",
          "index"      : 5,
      }, {
          "classifier" : "some",
          "name"       : "thing",
          "index"      : 0,
      }], "uri with two pieces and first index")

eq_ok(resolve("predicate/cut/some/thing/123"),
      [{
          "classifier" : "predicate",
          "name"       : "cut",
          "index"      : 0,
      }, {
          "classifier" : "some",
          "name"       : "thing",
          "index"      : 123,
      }], "uri with two pieces and second index")

eq_ok(resolve("predicate/cut/99/some/thing/000"),
      [{
          "classifier" : "predicate",
          "name"       : "cut",
          "index"      : 99,
      }, {
          "classifier" : "some",
          "name"       : "thing",
          "index"      : 0,
      }], "uri with two pieces and both indices")
