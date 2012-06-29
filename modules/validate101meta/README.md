# Headline

A module to validate files in the 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the "validator" form of metadata. The module generates ".validator.json" files in the directory "101web/contributions". That is, a ".validator.json" file is generated for every 101repo file with associated 101meta metadata for a validator. The suffix ".validator.json" is simply appended to the original file name. The actual file summarize the status of validation. The file generation is incremental in that only files will be generated, if they are actually missing or if their modification date is outdated compared to the underlying source file in 101repo. A summary of an extraction pass is dumped to the file "101web/dumps/validator.json".

# Dependencies

This module assumes that the module "matches101meta" was applied earlier.

# Issues

None.
