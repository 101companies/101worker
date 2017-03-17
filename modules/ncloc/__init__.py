config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'ncloc']],
        'uses': [['resource', 'lang']]
    }
}

# this is the actual logic of the module
def count_non_comment_lines(context, f):
    #datastructure for languages and their corresponding comment symbols
    languages = {'Java': {'Single': ['//'], 'Block': [{'BlockStart': '/*', 'BlockEnd': '*/'}]},
             'Python': {'Single': ['#'], 'Block': [{'BlockStart': '"""', 'BlockEnd': '"""'},{'BlockStart': "'''", 'BlockEnd': "'''"},]},
             'Haskell': {'Single': ['--'], 'Block': [{'BlockStart': '{-', 'BlockEnd': '-}'}]}}
    #get file
    source = context.get_primary_resource(f)
    #get language of file
    lang = context.get_derived_resource(f,'lang')
    
    ncloc = 0
    inBlock = False

    #check if language is in datastructure
    if languages.get(lang) != None :
        #check if langauges have block/singe-line comments
        singleExists = languages[lang].get("Single") != None
        blockExists = languages[lang].get("Block") != None

        #iterate over all lines
       	for line in source.split('\n'):

            if blockExists:
                #check if symbols are one of the given comment symbols for block comments
                for block in languages[lang].get("Block"):
                    blockStart = block["BlockStart"]
                    line = line.replace("\t","").replace(" ","").replace("\n","")
                    if line[0:len(blockStart)] == blockStart and inBlock == False:
                        inBlock = True
                        blockEnd = block["BlockEnd"]
                        line = line[len(blockStart):len(line)]
                        break
                    
                    
            
            #if we are not in a Block comment, check if it's a single line comment...            
            singleCheck = False            
            if inBlock == False:
                if singleExists:            
                    for single in languages[lang]["Single"]:
                        if len(line)>len(single):
                            if line[0:len(single)] == single:                
                                singleCheck = True
            #...if not increment sum of non comment lines of code 
            if singleCheck == False and inBlock == False:
                ncloc = ncloc + 1
       

            #check for block end symbols
            if blockExists:
                if inBlock == True:         
                    #invert line    
                    line = line[::-1]
                    line = line.replace("\t","").replace(" ","").replace("\n","")
                    #check if the first found signs are now the inverted signs of the endblock       
                    #of a comment (because we inverted the whole line before) 
                    if line[0:len(blockEnd)] == (blockEnd)[::-1] and inBlock == True:
                            inBlock = False

    return ncloc

def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        ncloc = count_non_comment_lines(context, f)

        context.write_derived_resource(f, ncloc, 'ncloc')
    except UnicodeDecodeError:
        context.write_derived_resource(f, 0, 'ncloc')

def remove_file(context, f):
    context.remove_derived_resource(f, 'ncloc')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])



import unittest
from unittest.mock import Mock
import io

class NclocTest(unittest.TestCase):

    def test_run_java(self):
        change = {
            'type': 'NEW_FILE',
            'file': 'some-file.java'
        }
        self.env = Mock()
        self.env.get_primary_resource.return_value = '//x = 5\n/*y=6*/\nprint(x)\nz=7\nw=8'
        self.env.get_derived_resource.return_value = 'Java'
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.java', 3, 'ncloc')

    def test_run_haskell(self):
        change = {
            'type': 'FILE_CHANGED',
            'file': 'some-file.hs'
        }
        self.env = Mock()
        self.env.get_primary_resource.return_value = "\t--x = 5\n\t{-y=6\nprint(x)-}\nz=7\nw=8"
        self.env.get_derived_resource.return_value = 'Haskell'
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.hs', 2, 'ncloc')

    def test_run_python(self):
        change = {
            'type': 'FILE_CHANGED',
            'file': 'some-file.py'
        }
        self.env = Mock()
        self.env.get_primary_resource.return_value = '\t#x = 5\n\t"""y=6\nprint(x)""" \nz=7\nw=8'
        self.env.get_derived_resource.return_value = 'Python'
        run(self.env, change)

        self.env.write_derived_resource.assert_called_with('some-file.py', 2, 'ncloc')


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(NclocTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
