import os
from jinja2 import Template

#TODO usefulness is limited since there are multiple processes - also hacky

_cache = {}

def _reload(path, template):
    mTime = os.path.getmtime(path)
    t = Template(''.join(open(path, 'r').readlines()))
    _cache[template] = {
        'mTime':mTime,
        'template':t
    }

def _ensureValidity(template):
    if not template in _cache:
        _reload(os.path.join(os.path.dirname(__file__), template), template)
    else:
        path = os.path.join(os.path.dirname(__file__), template)
        mTime = os.path.getmtime(path)
        if mTime > _cache[template]['mTime']:
            _reload(path, template)

def getTemplate(template):
    _ensureValidity(template)
    return _cache[template]['template']
