gatherSourceDirectoryMatchingRules
==================================
This module gather information from different files to generates a set of rules.
These rules will be used later by different modules to derive properties of files 
and directories according to their path name. For instance a rule will indicatesµ
that files with a suffix ".java" is a java source file.

Input
-----
This module reads all files that contain in a form or another some pattern marching
rule against file path.

### TeTaLa files 
TeTaLa files describe meta information about technologies. 
See http://101companies.org/index.php/Language:TeTaLa

### LaTaLa files 
LaTaLa files describe meta information about software languages. 
See http://101companies.org/index.php/Language:LaTaLa

'''
File: languages/Haskell/.latala ->

{
 "geshi" : "haskell",
 "extension" : ".hs",
 "locator" : "../../technologies/HsFragmentLocator/locator.py"
}
'''

### Additional files


'''
File: technologies/
'''

[
 { 
  "extension" : ".g",
  "geshi" : "text",
  "role" : "input"
 },
 { 
  "extension" : ".tokens",
  "geshi" : "text",
  "role" : "output"
 },
 {
  "pattern" : "@Lexer.java",
  "role" : "output"
 },
 {
  "pattern" : "@Parser.java",
  "role" : "output"
 },
 {
  "pattern" : "antlr-@.jar",
  "role" : "support"
 }
]

Output
------
The module generates the rule file in json format. The name of the output file 
is defined by the variable "$sourceDirectoryMatchingRules" in Makefile.vars

Status
------

