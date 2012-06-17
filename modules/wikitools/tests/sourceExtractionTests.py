import unittest
import re

class SourceExtractionTestCase(unittest.TestCase):
	def runTest(self):
		inp = '<syntaxhighlight lang="javascript">{ "suffix" : ".java", "metadata" : { "language" : "Java" } }</syntaxhighlight>'
		pattern = '<syntaxhighlight\slang=(".*?")>(.*?)<\/syntaxhighlight>'; 
		m = re.search(pattern, inp)
		m.group(1) == "javascript", 'lang attribute is not handled properly'

if __name__ == "__main__":
	unittest.main()