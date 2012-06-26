# Headline

A module to match 101meta rules with 101repo

# Details

See the [Language:101meta specification](http://101companies.org/index.php/Language:101meta) for details on the constraint forms of rules. The module generates the files "matches.json" in the directory "101results/101meta". The file is a list with the entries corresponding to files with matches. Each entry names the file and enumerates all applicable metadata units where each such unit is also qualified with the rule id (i.e., the index of the rule in the list of all rules).

# Dependencies

This module assumes that rules have been gathered by module "gather101meta".

# Issues 

* This is a prototype implementation.
* See JM's code for another implementation.
