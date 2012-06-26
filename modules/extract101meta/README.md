# Headline

A module to extract files for 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the "extractor" form of metadata. The module generates ".json" files in the directory "101results/101meta/facts". That is, a ".json" file is generated for every 101repo file with associated 101meta metadata for an extractor. The suffix ".json" is simply appended to the original file name. The file generation is incremental in that only files will be generated, if they are actually missing or if their modification date is outdated compared to the underlying source file in 101repo.

# Dependencies

This module assumes that files have been matched by the module "match101meta".

# Issues

None.

