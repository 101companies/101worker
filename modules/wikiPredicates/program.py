import json
import itertools
import collections

with open('wiki.json') as f:
    data = json.load(f)

pages = data['wiki']['pages']

keys = [page.items() for page in pages]

keys = list(itertools.chain(*keys))

keys = [key for key in keys if key[0] not in ('n', 'p', 'internal_links', 'headline')]

def denormalizePageTitles(item):
    key = item[0]
    values = item[1]

    def normalizePageTitle(value):
        if isinstance(value, dict):
            if value['p']:
                return value['p'] + ':' + value['n']
            else:
                return value['n']
        else:
            return value

    if values:
        values = [normalizePageTitle(value) for value in values]

    return (key, values)

# here we have all namespaces and titles merged
keys = [denormalizePageTitles(key) for key in keys]

# now merging all keys into a large dict

def addKeyToDict(acc, val):
    if acc.has_key(val[0]):
        items = acc[val[0]]
        if isinstance(items, set):
            for i in val[1]:
                items.add(i)
            acc[val[0]] = items
    else:
        acc[val[0]] = set(val[1])
    return acc

keys = reduce(addKeyToDict, keys, {})

keys = { key:sorted(list(value)) for (key, value) in keys.iteritems() }

with open('wiki-predicates.json', 'w') as f:
    json.dump(keys, f, indent=4, sort_keys=True)
