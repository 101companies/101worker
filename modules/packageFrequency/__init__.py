config = {
    'wantdiff': False,
    'wantsfiles': True,
    'threadsafe': False
}

def run(context, change):
    f = change['file']

    lang = context.get_derived_resource(f, '.lang')
    if lang == 'Java':
        dump = context.read_dump('packageFrequency')
        if dump is None:
            dump = {}

        facts = context.get_derived_resource(f, '.extractor')

        for i in facts['imports']:
            if not i in dump:
                dump[i] = 1
            else:
                dump[i] += 1

        context.write_dump('packageFrequency', dump)
