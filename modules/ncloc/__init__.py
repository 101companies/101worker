import os
import json

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
    languages = {'Java': {'Single': ['//'], 'BlockStart': ['/*'], 'BlockEnd': ['*/']},
		 'Python': {'Single': ['#'], 'BlockStart': ["'''"], 'BlockEnd': ["'''"]},
		 'Haskell': {'Single': ['--'], 'BlockStart': ["{-"], 'BlockEnd': ["-}"]}}
    #get file
    source = context.get_primary_resource(f)
    #get language of file
    lang = context.get_derived_resource(f,'lang')
    
    ncloc = 0
    block = False
    lineNumber = 0
    blockLineBegin = -1 # only needed when block start and end symbol are equal
    
    #check if language is in datastructure
    if languages.get(lang) != None :
        #check if langauges have block/singe-line comments
        singleExists = languages[lang].get("Single") != None
        blockExists = languages[lang].get("BlockStart") != None

        if blockExists:
            equalBlockSymbols = languages[lang].get("BlockStart") == languages[lang].get("BlockEnd")
        #iterate over all lines
       	for line in source.split('\n'):
            lineNumber = lineNumber +1

            if blockExists:
                #check if symbols are one of the given comment symbols for block comments
                for blockstart in languages[lang].get("BlockStart"):
                    line = line.replace("\t","").replace(" ","").replace("\n","")
                    if line[0:len(blockstart)] == blockstart and block == False:
                        block = True
                        #set marker for blockLineBegin, if block symbols are equal, to prevent reading of
                        #block start as block end later
                        if equalBlockSymbols:
                            if len((line)) == len(blockstart):
                                blockLineBegin = lineNumber
                    
                    
            
            #if we are not in a Block comment, check if it's a single line comment...            
            singleCheck = False            
            if block == False:
                if singleExists:            
                    for single in languages[lang]["Single"]:
                        if len(line)>len(single):
                            if line[0:len(single)] == single:                
                                singleCheck = True
            #...if not increment sum of non comment lines of code 
            if singleCheck == False and block == False:
                ncloc = ncloc + 1
       

            #check for block end symbols
            if blockExists:
                for blockend in languages[lang]["BlockEnd"]:           
                    #invert line    
                    line = line[::-1]
                    #check if the first found signs are now the inverted signs of the endblock       
                    #of a comment (because we inverted the whole line before) 
                    if line[0:len(blockend)] == (blockend)[::-1] and block == True:
                        #if block start and end sign are equal, take care that you do not read  
                        #a block-start as a block-end                         
                        if equalBlockSymbols:
                            if not blockLineBegin == lineNumber:
                                block = False
                        else:
                            block = False

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
