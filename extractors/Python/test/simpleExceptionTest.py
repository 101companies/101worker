
# This source code aims to test follow code blocks of the extractor:
#	- ast.Assign
#	- ast.FunctionDef
#	- Import
# 	- ast.If
#   - ast.ImportFrom

#Apparently the code doesn't list the variables in the except part

import sys
from syb import *
def analyse(x) :
	result = "jop"
	length = len(x)
	if length == 0:
		return result
	else:
		res = "Jop" + analyse(x[1:length])	
		return res
try:
    f = open('myfile.txt')
    s = f.readline()
    i = analyse(s)
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    str = "sth"
except ValueError:
    print "Could not convert data to an integer."
except:
    err = "sth"
    concat =  "Unexpected %s error: %i" % (err, 21) 
    print concat
    raise