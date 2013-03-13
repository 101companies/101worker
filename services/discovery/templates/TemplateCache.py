import os
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache

#Bytecode cache disabled, since Github is unable to save folder rights...
#but I guess at some point, it should be reenabled
env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    #bytecode_cache=FileSystemBytecodeCache(os.path.join(os.path.dirname(__file__), 'cache'), '%s.cache')
)

def getTemplate(template):
    return env.get_template(template)
