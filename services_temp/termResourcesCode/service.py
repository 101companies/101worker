import urllib2
import json
import HTMLParser
from BeautifulSoup import BeautifulSoup
from django.http import HttpResponse

def serveCode(request, term, resName, cat, resIndex, codeIndex, format):

  termURL = 'http://worker.101companies.org/services/termResources/' + term + '.json'
  resData = json.load(urllib2.urlopen(termURL))

  res = filter(lambda r: r['name'] == resName, resData)[0]
  fullURL = res[cat][resIndex]['full']
  resURL = fullURL.split('#')[0]
  resCSSID = fullURL.split('#')[1]

  soup = BeautifulSoup(urllib2.urlopen(resURL).read())
  node = soup.find(id=resCSSID)
  codes = node.findAllNext('pre', {'class' : 'programlisting'})
  rawcode = codes[codeIndex]
  h = HTMLParser.HTMLParser()
  result = json.dumps({'code': h.unescape(rawcode.contents[0])})

  if format == 'jsonp':
    result = request.GET.get('callback', 'callback') + '(' + result + ')'
  return HttpResponse(result, content_type='application/javascript' if isJsonp else 'text/json')


def routes():
    return [
        ('/termResourcesCode/(?P<term>.+)/(?P<resName>.+)/(?P<cat>.+)#(?P<resIndex>.+)/(?P<codeIndex>.+)\.(?P<format>.+)', serveCode)
    ]

serveCode(0, 'Fold', 'RWH', 'primary', 0, 0, 0)
