import os

from . import wiki2json

def test():
    pass
    # import TAP
    # import TAP.Simple
    # import StringIO
    #
    # t = TAP.Simple
    # t.builder._plan = None
    #
    # t.plan(7)
    #
    # dumps101dir = '/some/test/dir'
    #
    # properties = [
    #     "101project",
    #     "101contribution",
    #     "Implementation",
    #     "Model",
    #     "101system",
    #     "101contributor",
    #     "101project",
    #     "http://google.de",
    #     "~SomethingNotMentioned",
    #     "RelatesTo::@contributor",
    #     "InstanceOf::Namespace:101"
    # ]
    #
    # result = wiki2json.extract_properties(properties)
    #
    # t.eq_ok(len(result['InstanceOf']), 1, 'finds 1 instanceOf')
    # t.eq_ok(result['InstanceOf'][0]['n'], '101', 'splits namespace and title')
    # t.eq_ok(result['InstanceOf'][0]['p'], 'Namespace', 'splits title and namesspace')
    #
    # t.eq_ok(len(result['mentions']), 8, 'finds 8 mentions')
    # t.is_ok('http://google.de' in result['mentions'], True, 'finds google in links')
    #
    # t.eq_ok(len(result['mentionsNot']), 1, 'finds one mentionsNot')
    # t.eq_ok(result['mentionsNot'][0]['n'], 'SomethingNotMentioned', 'finds no wrong mentions')
