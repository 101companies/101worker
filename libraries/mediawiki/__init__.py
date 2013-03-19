import re

def remove_headline_markup(text):

    replacements = [
        (r"(=+)([^=]+)\1", "\g<2>"),
        (r'\n', ''),
        (r'\[\[([^\]\]]+)\]\]', '\g<1>')

    ]
    for r in replacements:
        text = re.sub(r[0], r[1], text)

    return text.strip()

