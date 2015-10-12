"""
Basic 101rules matches phase.
"""
from .Phase import Phase


class Matches(Phase):
    """
    The basic 101rules matches phase - see Phase. The suffix for this phase is
    ``.matches.json''.
    """
    suffix = ".matches.json"


    def applicable(self, rule):
        """
        Returns true if the given rule does not have any fast predicates,
        predicates or fragment rules.
        """
        # XXX probably better to use a whitelist approach
        return all(key not in rule for key in
                  ("fpredicate", "predicate", "fragment"))
