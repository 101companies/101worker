import re
import json
import os

def remove_headline_markup(text):

    replacements = [
        (r"(=+)([^=]+)\1", "\g<2>"),
        (r'\n', ''),
        (r'\[\[([^\]\]]+)\]\]', '\g<1>'),
        (r'([a-zA-Z0-9_]+)\|([a-zA-Z0-9_]+)', '\g<2>')

    ]
    for r in replacements:
        text = re.sub(r[0], r[1], text)

    return text.strip()

def dewikifyNamespace(namespace):
    values = json.load(open(os.path.join(os.path.dirname(__file__), 'Mappings.json')))['dewikify']
    return values.get(namespace,'')

def wikifyNamespace(namespace):
    values = json.load(open(os.path.join(os.path.dirname(__file__), 'Mappings.json')))['wikify']
    return values.get(namespace, None)

if __name__ == '__main__':
    print remove_headline_markup("a|ab")

