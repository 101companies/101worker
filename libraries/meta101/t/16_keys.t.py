from TAP.Simple import *
import meta101

plan(3)


eq_ok(meta101.Matches().keys(), [
          "suffix",
          "filename",
          "basename",
          "dirname",
          "content",
      ], "matches keys")

eq_ok(meta101.Predicates().keys(), [
          "suffix",
          "filename",
          "basename",
          "dirname",
          "content",
          "language",
          "predicate",
      ], "predicates keys")

eq_ok(meta101.Fragments().keys(), [
          "suffix",
          "filename",
          "basename",
          "dirname",
          "content",
          "fragment",
      ], "fragments keys")
