import os
import json

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True,
    'behavior': {
        'creates': [['resource', 'comments']],
        'uses': [['resource', 'lang']]
    }
}

# this is the actual logic of the module
def extract_comments(context, f):
    #datastructure for languages and their corresponding comment symbols
    languages = {'Java': {'Single': ['//'], 'BlockStart': ['/*'], 'BlockEnd': ['*/']},
		 'Python': {'Single': ['#'], 'BlockStart': ["'''"], 'BlockEnd': ["'''"]},
		 'Haskell': {'Single': ['--'], 'BlockStart': ["{-"], 'BlockEnd': ["-}"]}}
    #init of comments array
    comments = []

    #get file & get language of file
    source = context.get_primary_resource(f)
    lang = context.get_derived_resource(f,'lang')


    #block symbols if we are actually in a block-comment
    block = False
    #number of actual array entry
    entry = 0
    
    #check if language is in datastructure
    if languages.get(lang) != None :
        #check if languages have block/singe-line comments
        singleExists = languages[lang].get("Single") != None
        blockExists = languages[lang].get("BlockStart") != None

        #iterate over all lines
       	for line in source.split('\n'):

            if blockExists:
                #check if we are already in a block
                if block == True:
                    blockendFound = False
                    for blockend in languages[lang].get("BlockEnd"):
                        end = line.find(blockend)
                        #if we find a block-end symbol end the block
                        if end != -1:
                            comments[entry] = comments[entry]+'\n'+line[0:end+1]
                            entry = entry + 1
                            block = False
                            blockendFound = True
                            break
                    if blockendFound == False:
                        comments[entry] = comments[entry]+'\n'+line     
                #if we are not in a block, try to find a start-symbol
                else:
                    for blockstart in languages[lang].get("BlockStart"):
                        start = line.find(blockstart)
                        if start != -1 and block == False:
                            blockendFound = False
                            #try to find block-end symbol in same line
                            for blockend in languages[lang].get("BlockEnd"):
                                end = line[start+len(blockstart):len(line)].find(blockend)
                                if end != -1:
                                    comments.append(line[start+len(blockstart):end+1])
                                    entry = entry + 1
                                    blockendFound = True
                                    break
                            #if no block-end symbol has been found, set block to true
                            if blockendFound == False:
                                comments.append(line[start+len(blockstart):len(line)])
                                block = True

            #check for single-line comment
            for single in languages[lang].get("Single"):
            	if block == False and singleExists:
            	    start = line.find(single) 
            	    if line.find(single) != -1:
            	        comments.append(line[start+len(single):len(line)])
            	        entry = entry + 1
            	        break

    result = {'comments':comments}
    return result

def update_file(context, f):
    # reads the content of the file (primary resource)
    try:
        comments = extract_comments(context, f)

        context.write_derived_resource(f, comments, 'comments')
    except UnicodeDecodeError:
        context.write_derived_resource(f, {'comments':[]}, 'comments')

def remove_file(context, f):
    context.remove_derived_resource(f, 'comments')

def run(context, change):
    # dispatch the modified file
    if change['type'] == 'NEW_FILE':
        update_file(context, change['file'])

    elif change['type'] == 'FILE_CHANGED':
        update_file(context, change['file'])

    else:
        remove_file(context, change['file'])
