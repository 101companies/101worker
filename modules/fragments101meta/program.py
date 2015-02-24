#!/usr/bin/env python
import meta101
# FIXME also check changes on fragments when they get moved into 101worker
meta101.matchall("fragments", entirerepo=meta101.havechanged(__file__))
