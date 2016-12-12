from .genLinkedData import run
from .test import test

config = {
    'wantdiff': False,
    'behavior': {
        'uses': [['dump', 'wiki-links']]
    }
}
