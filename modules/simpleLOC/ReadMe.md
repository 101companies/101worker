# simpleLOC

##Characteristics
###config:
wantsdiff:  True
wantsfiles: True
threadsafe: True

###behavior:
creates: resource loc

###imports:
os
json

##Architecture
###init.py
Uses the source code of the files to count the number of lines of code and stores it into a derived resource.
The file also contains tests for all possibilities of change types.

##Output:
###value:
Number of lines of code in the files.
###structure:
{Number of lines}

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

