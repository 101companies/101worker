import os
import json

def count_loc(source):
    with open(source, 'r') as source:
        return sum(1 for line in source)

def save_data(target, data):
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))

    with open(target, 'w') as f:
        json.dump(data, f)

def update_file(context, file):
    source = os.path.join(context['env']['repo101dir'], file)
    target = os.path.join(context['env']['targets101dir'], file + '.loc.json')
    loc = count_loc(source)
    save_data(target, loc)

def run(context, change):

    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        # DELETED
        pass
