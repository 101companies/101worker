# This source code aims to test follow code blocks of the extractor:
#	- ast.FunctionDef
#	- ast.Assign
#	- ast.If



import sys

def add(x, y):
	result = 0
	if(x > y):
		result = x - y
	else:
		result = y - x;
	return result
	
num1 = 12
num2 = 14

sum = add(num1, num2)
print sum