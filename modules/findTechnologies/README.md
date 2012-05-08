# Headline

a module to associate contributions with technology-related information

# Input/output behavior

The module reads TeTaLa files for all technologies from
"101results/101repo/technologies/*". The module writes
"technologies.json" files for all contributions to
"101results/contributions/*". The generated json files associate
technology names as keys with file names and additional metadata as
values.

# Example

Consider the following input "101results/101repo/technologies/ANTLR/tagging.json":

<pre>
{
 "input" : {
  "extension" : ".g"
 },
 "output" : {
  "extension" : ".tokens",
  "pattern" : [
   "@Lexer.java",
   "@Parser.java"
  ]
 },
 "support" : {
  "pattern" : "antlr-@.jar"
 }
}
</pre>

On these grounds, the module can determine the use of the technology
ANTLR within contributions. In particular, input files can be
distinguished from output files. Also, .jar files can be associated
with the technology; see the key "support. Relevant files are
specified either by extension (see the key "input") or by file-name
pattern (see the keys "output" and "support"); the "@" character may
match with any sequences of file-name characters.

Consider the following output "101results/contributions/antlrAcceptor/technologies.json":

<pre>
{
 "Haskell" : {
  "geshi" : "haskell",
  "extension" : ".hs",   
  "file" : ["Company.hs", "Cut.hs", "Main.hs", "SampleCompany.hs", "Total.hs"]
 }
}
</pre>

File names are specified relative to the root directory of the contribution.

Only one language, i.e., "Haskell", has been inferred in this example.
