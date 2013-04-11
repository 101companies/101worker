import re

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
    values = {
        'Contribution': 'contributions',
        'Contributor' : 'contributors',
        'Concept'     : 'concepts',
        'Technology'  : 'technologies',
        'Language'    : 'languages',
        'Theme'       : 'themes',
        'Vocabulary'  : 'vocabularies',
        'Module'      : 'modules',
        'Service'     : 'services'
    }
    return values.get(namespace,'')

def wikifyNamespace(namespace):
    values = {
        'contributions': 'Contribution',
        'contributors' : 'Contributor',
        'concepts'     : '',
        'technologies' : 'Technology',
        'languages'    : 'Language',
        'themes'       : 'Theme',
        'vocabularies' : 'Vocabulary',
        'modules'      : 'Module',
        'services'     : 'Service',
        'Namespace'    : 'Namespace'
    }
    return values.get(namespace, None)

if __name__ == '__main__':
    print remove_headline_markup("a|ab")

