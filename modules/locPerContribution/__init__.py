config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False,
    'behavior': {
        'creates': [['dump', 'locPerContribution']],
        'uses': [['resource', 'loc']],
    },
    'visualization': True
}

from .program import run
from .test import test
from .visualization import visualize
