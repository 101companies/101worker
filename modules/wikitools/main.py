import pprint # Used for formatting the output for viewing, not necessary for most code
from wikitools import wiki, api, page
from document import Section

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

doc = page2sections(wikidata)
pprint.pprint(doc)
