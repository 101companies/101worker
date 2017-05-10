import os
import json

def getLanguages():
    #datastructure for languages and their corresponding comment symbols
    languages = {'Java': {'Single': ['//'], 'Block': [{'BlockStart': '/*', 'BlockEnd': '*/'}]},
            'Python': {'Single': ['#'], 'Block': [{'BlockStart': '"""', 'BlockEnd': '"""'},{'BlockStart': "'''", 'BlockEnd': "'''"},]},
            'Haskell': {'Single': ['--'], 'Block': [{'BlockStart': '{-', 'BlockEnd': '-}'}]},
            'Ruby': {'Single': ['#'], 'Block': [{'BlockStart': '=begin', 'BlockEnd': '=end'}]},
            'CPlusPlus': {'Single': ['//'], 'Block': [{'BlockStart': '/*', 'BlockEnd': '*/'}]}}
    return languages

# this is the actual logic of the module
def extract_comments(context, f):
    languages = getLanguages()
    #init of comments array
    comments = []

    #get file & get language of file
    source = context.get_primary_resource(f)
    lang = context.get_derived_resource(f,'lang')


    #block symbols if we are actually in a block-comment
    block = False
    #number of actual array entry
    entry = 0
    globalBlockEnd = ""
    
    #check if language is in datastructure
    if languages.get(lang) != None :
        #check if languages have block/singe-line comments
        singleExists = languages[lang].get("Single") != None
        blockExists = languages[lang].get("Block") != None and languages[lang].get("Block") != []

        #iterate over all lines
       	for line in source.split('\n'):

            #positionNumber marks later, where a block has ended and where the rest of the line continues
            #lineRest is the rest of the line
            positionNumber = 0
            lineRest = line

            #firstly check for single-line comment
            for single in languages[lang].get("Single"):
                if block == False and singleExists:
                    start = line.find(single)
                    if start != -1:
                        comments.append(line[start+len(single):len(line)])
                        entry = entry+1
                        lineRest = line[0:start] #here we set the line to the rest of the line without the single line comment, 
                                                 #so that we can search for block comments in the rest
                        break

            #loop gets stopped, when a) we are already in a block and do not find a end symbol
            #                        b) we are not in a block, but do not find a start symbol
            if blockExists:
                while True:
                    #check if we are already in a block
                    if block == True:
                        blockendFound = False
                        end = lineRest.find(globalBlockEnd)
                        #if we find a block-end symbol end the block
                        if end != -1:
                            comments[entry] = comments[entry]+'\n'+lineRest[0:end+1]
                            entry = entry + 1
                            block = False
                            blockendFound = True
                            #mark number of blockend, to determine where rest of line starts
                            positionNumber = end+len(blockend)
                        #when we find a blockend, add the text to the comments
                        else:
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
                        positionNumber = -1
                        for blocksymbol in languages[lang].get("Block"):
                            blockstart = blocksymbol.get("BlockStart")
                            start = lineRest.find(blockstart)                      
                            if start != -1 and block == False:
                                blockend = blocksymbol.get("BlockEnd")
                                #note that we change here the lineRest to a shorter path, where the blockstart
                                #symbol is at the beginning
                                lineRest = lineRest[start+len(blockstart):len(lineRest)] 
                                end = lineRest.find(blockend)
                                #if blockend symbol in same line, take only this part
                                if end != -1:
                                    comments.append(lineRest[0:end])
                                    entry = entry + 1
                                    #mark number of blockend, to determine where rest of line starts
                                    positionNumber = end+len(blockend)
                                else:
                                #if no block-end symbol has been found, set block to true
                                    comments.append(lineRest[start+len(blockstart):len(lineRest)])
                                    block = True
                                    globalBlockEnd = blockend
                        #check if positionNumber is already over the length of the string and if we are in a block,  
                        #if not continue with the rest of the line...
                        if positionNumber+1 < len(lineRest) and positionNumber != -1:
                            lineRest = lineRest[positionNumber+1:len(lineRest)]
                        #...otherwise stop while loop                    
                        else:   
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
