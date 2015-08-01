from kafka import KafkaConsumer
import sys
import json
import time

sys.path.append('modules')

import languageExtractor.program as lang
import wiki2tagclouds.program as tagclouds

def get_config():
    pass

# To consume messages
consumer = KafkaConsumer("pages",
                         group_id="my_group",
                         metadata_broker_list=["localhost:9092"],
                         auto_offset_reset='smallest')

for message in consumer:
    data = json.loads(message.value)

    lang.main(data)
    tagclouds.main(data)
    time.sleep(0.01)
