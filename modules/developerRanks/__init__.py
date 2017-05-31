from collections import Counter


config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False,
    'behavior': {
        'uses': [['dump', 'wiki-links']],
        'creates': [['dump', 'developerRanks']]
    },
    'visualisation': True
}

from .program import run
from .visualisation import createImage












