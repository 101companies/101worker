# commentExtractor

##Characteristics
###config:
wantsdiff:  True
wantsfiles: True
threadsafe: True

###behavior:
creates: resource comments
uses: resource lang

###imports:
os
json

##Architecture
###init.py
Uses the source code of the file and its corresponding language provided by module matchlanguage
to extract the comments of the file and store them in a derived resource
###program.py
Does the work of the module, by iterating line by line and checking if a there is a comment symbol
and if it is acutally in a block. The comment symbols are actually saved in the file, too.
Note: In a multiline commment, all lines get connected with a \n
###test.py
Standard tests for all languages provided in the comment symbol datastructure in program.py. It tests
all single and multi line comments, and it has also a extended test, where it takes a look, if the
program ignores a blockstart in a single line comment

##Output:
###value:
All comments of the language of the file
###structure:
{"comments":["comment1","comment2",...]

##Usage:
Run & test module with standard commands (bin/run_module, bin/test)

##Metadata:
###Author:
Andre Emmerichs
###Creation:
context: PP16/17
date: WS 16/17
###Features:

###Technology:

