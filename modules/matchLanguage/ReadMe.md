# matchLanguage

##Characteristics
###config:
wantsdiff:  True
wantsfiles: True
threadsafe: True

###behavior:
creates: resource lang

###imports:
os
json

##Architecture
###init.py
Extracts the file suffix and writes the corresponding language into a derived resource.
Also contains tests to cover all possibilities of change types.

##Output:
###value:
All comments of the language of the file
###structure:
{language}

##Usage:
Run & test module with standard commands (bin/run_module, bin/test)

##Metadata:
###Author:
Marcel Michels
###Creation:
context: PP16/17
date: SS 17
###Features:

###Technology:

