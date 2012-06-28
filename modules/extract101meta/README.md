# Headline

A module to extract facts from 101repo files

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the "extractor" form of metadata. The module generates ".extractor.json" files in the directory "101web/contributions". That is, a ".extractor.json" file is generated for every 101repo file with associated 101meta metadata for an extractor. The suffix ".extractor.json" is simply appended to the original file name. The file generation is incremental in that only files will be generated, if they are actually missing or if their modification date is outdated compared to the underlying source file in 101repo. A summary of an extraction pass is dumped to the file "101web/dumps/extractor.json".

# Dependencies

This module assumes that files have been matched by the module "match101meta".

# Issues

None.
