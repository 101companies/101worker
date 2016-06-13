from .mongo2json import run
from .test import test

config = {
    'wantdiff': False,
    'behavior': {
        'creates': [['dump', 'raw-wiki']]
    }
}
