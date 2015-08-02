from kafka import SimpleProducer, KafkaClient
from pymongo import MongoClient
import random
import json
from bson import json_util

client = MongoClient()
db = client['wiki_development']
pages = db['pages']

kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

while True:
    page = pages.find().limit(1).skip(random.randint(0, pages.count()))
    page = list(page)[0]

    event = {
        'action': 'created',
        'page': page
    }
    print 'added page:', page['title']

    producer.send_messages(b'101wiki', json.dumps(event, default=json_util.default))

    raw_input()
