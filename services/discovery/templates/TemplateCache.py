import os
from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache


env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    bytecode_cache= FileSystemBytecodeCache(os.path.join(os.path.dirname(__file__), 'cache'), '%s.cache')
)

def getTemplate(template):
    return env.get_template(template)
