# Headline

A module to generate GeSHi-based HTML files for 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the "geshi" form of metadata. The module generates ".geshi.html" files in the directory "101web/contributions". That is, a ".geshi.html" file is generated for every 101repo file with associated 101meta metadata for a geshi code. The suffix ".geshi.html" is simply appended to the original file name. The file generation is incremental in that only files will be generated, if they are actually missing or if their modification date is outdated compared to the underlying source file in 101repo.  A summary of the generation pass is dumped to the file "101web/dumps/geshi.json".

# Dependencies

This module assumes that the module "matches101meta" was applied earlier.

# Issues 

As priorities (dominators) will be supported by the module "matches101meta", this module will start to generate less HTML. As of now, this does not appear to be a problem though.
