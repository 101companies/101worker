#!/usr/bin/env python

import os

# set environment variable that our test is to be ran
# (is skipped for normal testing as it takes a long time)
os.environ["TEST_ALL_EXPLORER_ENTITIES"] = "1"

manage_py = os.path.join(os.environ["worker101dir"], "services", "manage.py")
os.system("python " + manage_py + " test explorer.testAllExplorerEntities")
