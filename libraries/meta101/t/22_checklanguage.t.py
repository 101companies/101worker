from TAP.Simple import *
import meta101

plan(4)

predicate = meta101.Predicates()
basefilejava = "t/language/Test.java"
nolanguahe = "t/language/Test.hs"

ok(    predicate.checklanguage( "Java","","","",basefilejava), "match language")
ok(not predicate.checklanguage( "python","","","",basefilejava), "mismatch language")
ok(not predicate.checklanguage( "Python","","","",nolanguahe), "mismatch language")
ok(not predicate.checklanguage( "Java","","","",nolanguahe), "mismatch language")


