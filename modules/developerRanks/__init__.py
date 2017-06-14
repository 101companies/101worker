from collections import Counter


config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False,
    'behavior': {
        'uses': [['dump', 'wiki-links']],
        'creates': [['dump', 'developerRanks']]
    },
    'visualization': True
}

from .program import run
from .visualization import visualize












