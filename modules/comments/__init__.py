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

            #positionNumber marks later, where a block has ended and where the rest of the line continues
            #lineRest is the rest of the line
            positionNumber = 0
            lineRest = line
                
            #loop gets stopped, when a) we are already in a block and do not find a end symbol
            #                        b) we are not in a block, but do not find a start symbol
            while True and blockExists:
                #check if we are already in a block
                if block == True:
                    blockendFound = False
                    for blockend in languages[lang].get("BlockEnd"):
                        end = lineRest.find(blockend)
                        #if we find a block-end symbol end the block
                        if end != -1:
                            comments[entry] = comments[entry]+'\n'+lineRest[0:end+1]
                            entry = entry + 1
                            block = False
                            blockendFound = True
                            #mark number of blockend, to determine where rest of line starts
                            positionNumber = end+len(blockend)
                            break
                    #when we find a blockend, add the text to the comments
                    if blockendFound == False:
                        comments[entry] = comments[entry]+'\n'+lineRest     
                        #check if positionNumber is already over the length of the string, if not continue with
                        #the rest of the line...
                    if positionNumber+1 < len(lineRest) and blockendFound == True:
                        lineRest = lineRest[positionNumber+1:len(lineRest)]        
                    #...otherwise stop while loop                        
                    else:   
                        break
                #if not in a block, try to find blockstart symbol                
                else:
                    for blockstart in languages[lang].get("BlockStart"):
                        start = lineRest.find(blockstart)
                        blockendFound = False                        
                        if start != -1 and block == False:
                            blockendFound = False
                            #try to find block-end symbol in same line
                            for blockend in languages[lang].get("BlockEnd"):
                                #note that we change here the lineRest to a shorter path, where the blockstart
                                #symbol is at the beginning
                                lineRest = lineRest[start:len(lineRest)] 
                                end = lineRest.find(blockend)
                                #if blockend symbol in same line, take only this part
                                if end != -1:
                                    comments.append(lineRest[len(blockstart):end])
                                    entry = entry + 1
                                    blockendFound = True
                                    #mark number of blockend, to determine where rest of line starts
                                    positionNumber = end+len(blockend)
                                    break
                            #if no block-end symbol has been found, set block to true
                            if blockendFound == False:
                                comments.append(lineRest[start+len(blockstart):len(lineRest)])
                                block = True
                    #check if positionNumber is already over the length of the string and if we are in a block,  
                    #if not continue with the rest of the line...
                    if positionNumber+1 < len(lineRest) and blockendFound == True:
                        lineRest = lineRest[positionNumber+1:len(lineRest)]        
                    #...otherwise stop while loop                    
                    else:   
                        break

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
