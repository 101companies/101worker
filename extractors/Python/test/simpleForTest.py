
# This source code aims to test follow code blocks of the extractor:
#	- ast.Assign
#	- ast.For



import sys

nums = range(10)
result = 0
for x in nums:
	inLoop = 42
	result += x
	

print result