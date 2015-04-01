#!/usr/bin/env python
import os
import meta101


pdir       = os.environ["predicates101dir"]
predicates = [os.path.join(pdir, d, "predicate.py") for d in os.listdir(pdir)]
changed    = meta101.havechanged(__file__, *predicates)


meta101.matchall("predicates", entirerepo=True)
