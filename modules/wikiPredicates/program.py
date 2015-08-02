import json
import itertools
import collections
import storm
from pymongo import MongoClient

def normalizePageTitle(value):
    if isinstance(value, dict):
        if value['p']:
            return value['p'] + ':' + value['n']
        else:
            return value['n']
    else:
        return value

OUTPUT_FILE = '/home/kevin/worker/101worker/modules/wikiPredicates/wiki-predicates.json'

def normalizePageTitles(predicates):
    return map(normalizePageTitle, predicates)

class WikiPredicatesBolt(storm.BasicBolt):

    def __init__(self):
        storm.BasicBolt.__init__(self)
        self.client = MongoClient()
        self.db = self.client['wiki_predicates']
        self.collection = self.db['predicates']
        self.collection.drop()
        with open(OUTPUT_FILE, 'w') as f:
            json.dump({}, f)

    def create_dump(self):
        result = {}
        for page in self.collection.find():
            for (key, value) in page['metadata'].items():
                if result.has_key(key):
                    result[key].extend(value)
                else:
                    result[key] = value

        with open(OUTPUT_FILE, 'w') as f:
            json.dump(result, f, indent=4, sort_keys=True)

    def process(self, tup):
        action = tup.values[0]
        data = tup.values[4]

        title = normalizePageTitle(data)
        metadata = { key: normalizePageTitles(value) for (key, value) in data.items() if key not in ['n', 'p', 'headline', 'internal_links', 'subresources', '_id'] }

        result = {
            'name': title,
            'metadata': metadata,
            '_id': data['_id']
        }
        if action == 'created':
            self.collection.insert_one(result)

        elif action == 'updated':
            self.collection.update({ '_id': result['_id'] }, { '$set': result }, upsert=False)

        else:
            self.collection.remove(result['_id'])

        self.create_dump()

WikiPredicatesBolt().run()
