from .genLinkedData import run
from .test import test

config = {
    'wantdiff': False,
    'behavior': {
        'creates': [['dump', 'ontology.ttl']]
    }
}
