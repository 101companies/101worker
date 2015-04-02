
# This source code aims to test follow code blocks of the extractor:
#	- ast.If
#	- ast.ClassDef
#	- ast.Assign

class Greeting:
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print "Destruktor gestartet"
    def SayHello(self):
        print "Guten Tag", self.name
    def ifBlock(self):
    	execute = true
    	if(execute):
    		print name
    	else:
    		x = 12
    		y = 4
    		z = x +y
    	