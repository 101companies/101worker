import os
import json

config = {
    'wantdiff': True,
    'threadsafe': True
}

def count_lines(source):
    return sum(1 for line in source)

def save_data(context, f, data):
    context.write_derived_resource(f, data, '.loc')

def update_file(context, f):
    source = context.get_primary_resource(f)
    loc = count_lines(source)
    save_data(context, f, loc)

def remove_file(context, f):
    context.remove_derived_resource(f, '.loc')

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
