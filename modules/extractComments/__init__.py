config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'comments']],
        'uses': [['resource', 'lang']]
    }
}

from .program import run
from .test import test
