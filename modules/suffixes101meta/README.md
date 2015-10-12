# Headline

A module for analyzing all, matched, and unmatched suffixes for 101repo

# Output

[dumps/suffixes.json](http://black42.uni-koblenz.de/production/101worker/dumps/suffixes.json)

These are the components of the dump: 

* **numbersOfSuffixes**: Suffixes of 101repo are classified and counted as follows: the number of _all_ suffixes, i.e., suffixes used by the files in the repository; the number of _matched_ suffixes, i.e., suffixes exercised in suffix constraints in 101meta rules; the number of _unmatched_ suffixes, i.e., all suffixes minus matched suffixes.
* **suffixes**: The same classification, as above, in terms of _all_, _matched_, and _unmatched_ suffixes applies, while the actual suffixes are listed and they are ordered by the number of files in the repository with the suffix in descending order. 
* **numbersBySuffix**: Again, suffixes are listed, grouped, and ordered as before, but the actual number of files in the repository with the suffix are associated with the suffix.
* **filesBySuffix**: Again, suffixes are listed, grouped, and ordered as before, but the actual files in the repository with the suffix are associated with the suffix.

# Methodology

The data can be used in these ways:

* Popularity of suffixes is immediately defined. Popularity of suffixes may be used as a proxy, for example, for popularity of languages.
* Unmatched suffixes may call for additional 101meta rules. It usually makes sense to prioritize the most frequently exercised, unmatched suffixes as a corresponding rule would reduce the number of unmatched files the quickest.
* Unmatched suffixes may also be a sign of contribution-specific conventions such that certain suffixes are only used locally. Either these specific conventions should be documented as constraint combinations of dirname and suffix, or the migration to more general conventions (i.e., renaming files to use more generally established suffixes) could be considered.
* Contributors may directly add 101meta rules or send proposals to gatekeepers@101companies.org. 101meta rules on suffixes as much as other rules could contain a "citation" element for reasons discussed in the 101meta documentation. Following common practice, 101meta rules should be placed in ".101meta" files in languages and technologies subdirectories, where possible, or in contributions subdirectories, if they are properly contribution-specific.
