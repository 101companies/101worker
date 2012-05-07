# Headline

a module to group files of a contribution per language

# Input/output behavior

The module accesses "101repo" via "101results/101repo".

The module looks up "tagging.json" files for all languages in "101repo/languages/*".

The module generates "languages.json" files for all contributions in "101repo/contributions/*".

Those generated json files associate language names as keys with file names as values.

# Example

Consider the following input "languages/Haskell/tagging.json":

<pre>
{
 "geshi" : "haskell",
 "extension" : ".hs"
}
</pre>

On these grounds Haskell source files are to be located for all contributions.

For instance, the following output "contributions/haskell/languages.json" is derived:

<pre>
{
 "Haskell" : ["Company.hs", "Cut.hs", "Main.hs", "SampleCompany.hs", "Total.hs"]
}
</pre>

File names are specified relative to the root directory of the contribution.

Only one language, i.e., "Haskell", has been inferred in this example.
