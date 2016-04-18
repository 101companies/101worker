import os
import json

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True
}

# this is the actual logic of the module
def count_lines(source):
    return sum(1 for line in source)

def update_file(context, f):
    # reads the content of the file (primary resource)
    source = context.get_primary_resource(f)

    loc = count_lines(source)

    context.write_derived_resource(f, loc, '.loc')

def remove_file(context, f):
    context.remove_derived_resource(f, '.loc')

def run(context, change):
    # dispatch the modified file
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

    # test data
    three_lines = StringIO.StringIO('''
    Test
    ''')

    zero_lines = StringIO.StringIO('')

    # plan gets the number of defined tests as parameter
    t.plan(2)

    # tests count lines
    t.eq_ok(3, count_lines(three_lines), 'simple lines count')
    t.eq_ok(0, count_lines(zero_lines), 'works for 0 lines')
