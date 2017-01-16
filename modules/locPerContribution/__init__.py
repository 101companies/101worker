config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False,
    'behavior': {
        'creates': [['dump', 'locPerContribution']],
        'uses': [['resource', 'loc']],
    },
    'visualisation': True
}

from .program import run
from .test import test
from .visualisation import createImage
