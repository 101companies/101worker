# Headline

A module completing "matches101meta" to also cover predicates

# Details

The predicate form of constraints is treated separately so that modules may be performed after basic matching (before matching predicates), thereby allowing for modules that prepare predicate execution. For instance, fact extraction may be performed based on just basic metadata about extractors, thereby enabling predicates that may depend on extracted facts.

# Dependencies

This module assumes that the modules "gather101meta" and "matches101meta" were applied earlier. Also, matching is performed on the pulled 101repo, as available in "101results/101repo", as performed by the module "pull101repo".
