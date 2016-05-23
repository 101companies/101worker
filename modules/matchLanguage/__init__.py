#!/usr/bin/env python

# migration code:
# import json
# data = json.load(open('rules.json'))
#
# rules = data['results']['rules']
#
# result = {}
# for rule in rules:
#     metadata = rule['rule']['metadata']
#     for metadata in metadata:
#         lang = metadata.get('language', None)
#         if lang:
#             result[rule['rule']['suffix'][1:]] = lang
# print json.dumps(result, indent=4)

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'lang']],
    }
}

langs = {
    'py': 'Python',
    'sqldeployment': 'SQL',
    'pro': 'Prolog',
    'aj': 'AspectJ',
    'ini': 'Settings',
    'cs': 'CSharp',
    'txt': 'Plain Text',
    'xml': 'XML',
    'rsc': 'Rascal',
    'xq': 'XQuery',
    'java': 'Java',
    'xmi': 'XMI',
    'zip': 'Zip',
    'scala': 'Scala',
    'hpp': 'CPlusPlus',
    'jar': 'JAR',
    'properties': 'Settings',
    'gif': 'Graphics Interchange Format',
    'json': 'JSON',
    'html': 'HTML',
    'sqlcmdvars': 'SQL',
    'rb': 'Ruby',
    'php4': 'PHP',
    'php5': 'PHP',
    'xhtml': 'XHTML',
    'prefs': 'Settings',
    'config': 'Config',
    'css': 'CSS',
    'sqlsettings': 'SQL',
    'fs': 'FSharp',
    'xsd': 'XSD',
    'hs': 'Haskell',
    'sh': 'Shell_Script',
    'js': 'JavaScript',
    'cpp': 'CPlusPlus',
    'sql': 'SQL',
    '101meta': '101meta',
    'ecore': 'Ecore',
    'wsdl': 'WSDL',
    'php': 'PHP',
    'class': 'Java_bytecode',
    'png': 'Portable Network Graphic',
    'md': 'Plain Text',
    'bat': 'Shell_Script',
    'mf': 'Java_manifest_file',
    'launch': 'Launch_file',
    'atl': 'ATL',
    'st': 'Smalltalk',
    'cob': 'Cobol',
    'pl': 'Perl',
    'erb': 'Ruby',
    'erl': 'Erlang',
    'sqlpermissions': 'SQL',
    'ru': 'Ruby'
}

def get_lang(resource):
    suffix = resource.split('.')[-1]
    return langs.get(suffix, 'unkown')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE' or change['type'] == 'FILE_CHANGED':
        context.write_derived_resource(change['file'], get_lang(change['file']), 'lang')

    else:
        context.remove_derived_resource(change['file'], 'lang')

import unittest
from unittest.mock import Mock

class TestMatchLanguage(unittest.TestCase):

    def test_get_lang(self):
        for ext in langs.keys():
            self.assertEqual(get_lang('file.' + ext), langs[ext])

    def test_run_new_file(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.py'
        }
        env = Mock()
        run(env, change)

        env.write_derived_resource.assert_called_with('some-file.py', 'Python', 'lang')

    def test_run_changed_file(self):
        change = {
            'type': 'FILE_CHANGED',
            'file': 'some-file.py'
        }
        env = Mock()
        run(env, change)

        env.write_derived_resource.assert_called_with('some-file.py', 'Python', 'lang')

    def test_run_removed_file(self):
        change = {
            'type': 'DELETED_FILE',
            'file': 'some-file.py'
        }
        env = Mock()
        run(env, change)

        env.remove_derived_resource.assert_called_with('some-file.py', 'lang')

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatchLanguage)
    unittest.TextTestRunner(verbosity=2).run(suite)
