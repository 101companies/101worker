# Headline

A module to generate GeSHi files for all of 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the "geshi" form of metadata. The module generates ".html" files in the directory "101results/101meta/geshi". That is, a ".html" file is generated for every 101repo file with associated 101meta metadata for the geshi code. The suffix ".html" is simply appended to the original file name. The file generation is incremental in that only files will be generated, if they are actually missing or if their modification date is outdated compared to the underlying source file in 101repo.

# Dependencies

This module assumes that files have been matched by the module "match101meta".

# Issues 

* As priorities (dominators) will be supported by the module "match101meta", this module will start to generate less HTML. As of now, this does not appear to be a problem though.
