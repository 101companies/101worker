from .dump_pg import run
from .test import test

import json
import os

dir = os.path.dirname(__file__)

with open(os.path.join(dir, 'config.json')) as f:
    config = json.load(f)
