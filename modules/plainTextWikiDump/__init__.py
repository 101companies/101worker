from .wiki2json import run
from .test import test

config = {
    'wantdiff': False,
    'behavior': {
        'creates': [['dump', 'wiki-content']],
        'uses': [['dump', 'raw-wiki']]
    }
}
