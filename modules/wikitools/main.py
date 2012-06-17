import pprint # Used for formatting the output for viewing, not necessary for most code
from wikitools import wiki, api, page
import re
from document import Section
from pipeline import Pipeline, Step

site = wiki.Wiki('http://101companies.org/api.php')
params = {'action':'query',
    'titles':'Language:101meta'
}
req = api.APIRequest(site, params)
res = req.query(querycontinue=True)
pprint.pprint(res)

wikipage = page.Page(site, title='Language:101meta')
wikidata = wikipage.getWikiText(True).decode('utf-8', 'replace')
#pprint.pprint(wikidata)

def page2sections(page):
	l = page.split("==")
	l.pop(0)
	#print len(l[::2])
	#print len(l[1::2])
	zipped = zip(l[::2], l[1::2])
	doc = []
	for s in zipped:
	 	title = s[0].strip()
	 	print title
	 	content  = s[1].strip()
	 	if title.startswith('='):
	 		sec = doc[-1]
	 		sec.addSubsection(Section(title.replace('= ',''), content))
	 	else:
	 		doc.append(Section(title, content))

	return doc		

def extractSourceFragments(page):
	for section in page.sections:
		#for every section extract the source code fragments into a separate file
		pattern = '<syntaxhighlight\slang=(".*?")>(.*)<\/syntaxhighlight>'; 
		m = re.search(pattern, section.content)
		lang = m.group(1)
		source = m.group(2)
		pass

def main():
	pileline = Pipeline()
	step1 = Step(page2sections, "Extract sections from the page")
	pileline.addStep(step1)

	doc = pileline.execute(wikidata)
	pprint.pprint(doc)

if __name__ == "__main__":
	main()


