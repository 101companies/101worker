from .wiki2json import run
from .test import test

config = {
    'wantdiff': False,
    'behavior': {
        'creates': [['dump', 'wiki']],
        'uses': [['dump', 'pages']]
    }
}
