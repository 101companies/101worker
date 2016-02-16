import os
import json

config = {
    'wantdiff': True
}

def count_lines(source):
    return sum(1 for line in source)

def count_loc(source):
    with open(source, 'r') as source:
        count_lines(source)

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

def remove_file(context, file):
    target = os.path.join(context['env']['targets101dir'], file + '.loc.json')
    if os.path.exists(target):
        os.remove(target)

def run(context, change):

    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])

def test():
    import TAP
    import TAP.Simple
    import StringIO

    t = TAP.Simple
    t.builder._plan = None

    three_lines = StringIO.StringIO('''
    Test
    ''')

    zero_lines = StringIO.StringIO('')

    t.plan(2)

    t.eq_ok(3, count_lines(three_lines), 'simple lines count')
    t.eq_ok(0, count_lines(zero_lines), 'works for 0 lines')
