# ncloc

##Characteristics
###config:
wantsdiff:  True
wantsfiles: True
threadsafe: True

###behavior:
creates: resource ncoc
uses: resource lang

###imports:
None

##Architecture
###init.py
Contains program and test functions. The program takes the language of the file, finds the corresponding
comment symbols in a language datastructure. 

Then it iterates over every single line and checks if it is in a single-line or in a block comment.
If we are not in a comment, it increments the ncloc value by 1.

Limitations:

The program only recognizes the start of a comment at the beginning of a line, and the end of a comment at the 
end of a line.


##Output:
###value:
Contains the number of lines of code, which are not only comments
###structure:
{Integer} 

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

