# Headline

A module to match 101meta rules against 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the constraint forms of rules.  The module generates ".matches.json" files in the directory "101web/contributions". Each generated file holds the all applicable metadata units for the corresponding file from the repository. Each unit is qualified with the contributing rule id (i.e., the index of the rule in the list of all rules). A summary of the matches is dumped to the file "101web/dumps/matches.json".

# Dependencies

This module assumes that rules have been gathered by module "gather101meta".

# Issues 

* This is a prototype implementation.
* See JM's code for another implementation.
