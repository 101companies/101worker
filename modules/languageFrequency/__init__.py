from collections import Counter

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}

def run(env):
    wiki_dump = env.read_dump('wiki101dump')

    pages = wiki_dump['wiki']['pages']

    contributions = filter(lambda p: 'Contribution' == p.get('p', ''), pages)

    uses = [p.get('Uses', []) for p in contributions]
    uses = [p for use in uses for p in use]

    uses = list(filter(lambda u: u['p'] == 'Language', uses))

    uses = [use['n'].replace('_', ' ') for use in uses]

    lcounts = Counter(uses)

    env.write_dump('languageFrequency', lcounts)
