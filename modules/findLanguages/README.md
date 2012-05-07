# Headline

a module to group files of a contribution per language

# Input/output behavior

The module reads "tagging.json" files for all languages from "101results/101repo/languages/*".

The module writes "languages.json" files for all contributions to "101results/contributions/*".

Those generated json files associate language names as keys with file names as values.

# Example

Consider the following input "101results/101repo/languages/Haskell/tagging.json":

<pre>
{
 "geshi" : "haskell",
 "extension" : ".hs"
}
</pre>

On these grounds Haskell source files are to be located for all contributions.

For instance, the following output "101results/contributions/haskell/languages.json" is derived:

<pre>
{
 "Haskell" : ["Company.hs", "Cut.hs", "Main.hs", "SampleCompany.hs", "Total.hs"]
}
</pre>

File names are specified relative to the root directory of the contribution.

Only one language, i.e., "Haskell", has been inferred in this example.
