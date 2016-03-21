from .program import handleRule

def test():
    import TAP
    import TAP.Simple
    import StringIO

    t = TAP.Simple
    t.builder._plan = None

    # test data
    rule = {
        'metadata': 'a'
    }

    result_rule = {
        'rule': {
            'metadata': ['a']
        },
        'filename': 'file.py'
    }

    rule2 = {
        'metadata': ['a']
    }

    result_rule2 = {
        'rule': {
            'metadata': ['a']
        },
        'filename': 'file.py'
    }

    zero_lines = StringIO.StringIO('')

    # plan gets the number of defined tests as parameter
    t.plan(2)

    # tests count lines
    t.eq_ok(result_rule, handleRule(rule, 'file.py'), 'handleRule')
    t.eq_ok(result_rule2, handleRule(rule2, 'file.py'), 'handleRule if metadata is a list')
