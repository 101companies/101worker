config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False,
    'behavior': {
        'creates': [],
        'uses': [['resource', 'loc']]
    }
}

from .program import run
# from .test import test
