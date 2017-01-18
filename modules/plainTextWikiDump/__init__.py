from .wiki2json import run
from .test import test

import os
import json

dir = os.path.dirname(__file__)

with open(os.path.join(dir, 'config.json')) as f:
    config = json.load(f)
