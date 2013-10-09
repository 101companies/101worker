#
#	 pySesame is free software; you can redistribute it and/or modify
#	 it under the terms of the GNU General Public License as published by
#	 the Free Software Foundation; either version 2 of the License, or
#	 (at your option) any later version.
#
#	 pySesame is distributed in the hope that it will be useful,
#	 but WITHOUT ANY WARRANTY; without even the implied warranty of
#	 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	 GNU General Public License for more details.
#
#	 A copy of the full General Public License is available at
#	 http://www.gnu.org/copyleft/gpl.html and from the Free Software
#	 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
#
# 20050606 *pike 
# 	This version was modified to work with python 2>, which has
#	notable differences in the httplib module. I have kept the
#	interface the same.
#


import logging
from string import split
from urllib2 import urlopen
from urllib2 import Request
from urllib import urlencode
from xml.sax.handler import ContentHandler
from xml.sax import make_parser

query_paths = {'login':'servlets/login',
			   'logout':'servlets/logout',
			   'repositories':'servlets/listRepositories',
			   'query':'servlets/evaluateTableQuery',
			   'construct':'servlets/evaluateGraphQuery',
			   'extract':'servlets/extractRDF',
			   'uploadData':'servlets/uploadData',
			   'uploadURL':'servlets/uploadURL',
			   'clear':'servlets/clearRepository',
			   'remove':'servlets/removeStatements?',
			   }

class SesameConnection:
	"The main class for communicating with a Sesame Server."
	def __init__(self, url, path, logLevel="warning", logPath=""):
		self.hdlr = None
		self.setLogger(logLevel, logPath)
		self.url = url
		self.path = path
		self.cookie = ""
		self.resetQuery()
		self.logger.info('SesameConnection starting up...')

	def close(self):
		self.logout()
		self.logger.info('...SesameConnection closing down.')
		self.logger.removeHandler(self.hdlr)

	def setLogger(self, level, path):	 
		if self.hdlr: self.logger.removeHandler(self.hdlr)
		levelDict = {'debug':logging.DEBUG,
					 'info':logging.INFO,
					 'warning':logging.WARNING,
					 'error':logging.ERROR,
					 'critical':logging.CRITICAL}
		self.logger = logging.getLogger()
		self.hdlr = logging.FileHandler(path + 'pySesame.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		self.hdlr.setFormatter(formatter)
		self.logger.addHandler(self.hdlr)
		self.logger.setLevel(levelDict[level])

	def resetQuery(self):
		self.query = {}

	def doRequest(self, request, handler=None, post=None):
		# Sesame uses the text/plain content type for XML responses
		request.add_header("Accept", "text/plain")
		request.add_header("User-Agent", "PySesame 0.2")
		
		if self.cookie != "":
			cookie_string = "sesame_sid=%s" % self.cookie
			request.add_header("Cookie", cookie_string)

		if post != None:
			request.add_data(post)
		
		self.logger.debug(request.get_method()+":" + request.get_full_url())
			
		try:
			response = urlopen(request)
			# debug alls ok. i'd like to print 
			# the Status header, but urllib2 has already eaten it
			# and thrown its appropriate errors or followed 
			# any redirects etc
			if response.headers.has_key('Content-Length'): 
				self.logger.debug("OK: "+response.headers['Content-Length']+" bytes")
			else:
				self.logger.debug("OK")
		except Exception, error:
			self.logger.exception(error)
			raise SesameServerError(error)

		if response:
			if handler == "login":
				if not self.CookieHandler(response): 
					raise SesameServerError("No SessionID in cookie")
				# returns None on succes ....
			elif handler:
				saxparser = make_parser()
				saxparser.setContentHandler(handler)
				parsed = saxparser.parse(response)
				response.close()
				return handler.results
			else:
				results = response.readlines()
				resultString = ""
				resultString = resultString.join(results)
				return resultString

	def login(self, user, password):
		"""
		Gets your cookie.
		Returns None if successful.
		Throws an error if not
		"""
		self.resetQuery()
		self.query['user'] = user
		self.query['password'] = password
		query = urlencode(self.query)
		base = self.path + query_paths['login']
		request = Request(self.url+base)
		return self.doRequest(request, "login",query)

	def logout(self):
		"""
		Logs you out.
		Returns 'Logged out successfully' if successful.
		"""
		self.resetQuery()
		base = self.path + query_paths['logout']
		request = Request(self.url+base)
		return self.doRequest(request,None,"post")

	def repositories(self):
		"""
		Returns a list of dictionaries about available repositories.
		The dictionary keys are "id", "title", "readable" and "writeable"
		"""
		self.resetQuery()
		base = self.path + query_paths['repositories']
		query = urlencode(self.query)
		request = Request(self.url + base + query)
		handler = RepositoriesHandler()
		return self.doRequest(request, handler)
		
	def tableQuery(self, repository, queryLanguage, query,
				resultFormat="xml", serialization = "rdfxml"):
		"""
		xml format results are returned as a data structure as follows:
		* a dictionary with two keys, "header" and "tuples"
		* header is a list of string values
		* tuples is a list of lists.
		* each sub-list is like a row in the table
		* each sub-list is made up of dictionaries, wherein:
		* the key a string made from the text of the node
		* the value is the type ('uri', 'literal' or 'bNode')

		All other formats are returned as a string.		   
		"""
		self.resetQuery()
		self.query['repository'] = repository
		self.query['queryLanguage'] = queryLanguage
		self.query['resultFormat'] = resultFormat
		self.query['query'] = query
		if resultFormat == 'rdf':
			self.query['serialization'] = serialization
			handler = None
		elif resultFormat == 'html':
			handler = None
		else:
			handler = SelectQueryHandler()
		base = self.path + query_paths['query']
		request = Request(self.url+base)
		query = urlencode(self.query)
		return self.doRequest(request, handler, query)

	def graphQuery(self, repository, queryLanguage, query,
				serialization = "rdfxml"):
		"""
		Returns a string.
		"""
		self.resetQuery()
		self.query['repository'] = repository
		self.query['queryLanguage'] = queryLanguage
		self.query['query'] = query
		self.query['serialization'] = serialization
		handler = None
		# query_path *was* 'query' .. seemed wrong ..
		base = self.path + query_paths['construct']
		request = Request(self.url+base)
		query = urlencode(self.query)
		return self.doRequest(request, handler, query)
	
	def extract(self, repository, schema="no", data="no", explicitOnly="no",
				niceOutput="no", serialization="rdfxml"):
		"""
		Returns a string.
		"""
		self.resetQuery()
		self.query['repository'] = repository
		self.query['schema'] = schema
		self.query['data'] = data
		self.query['explicitOnly'] = explicitOnly
		self.query['niceOutput'] = niceOutput
		self.query['serialization'] = serialization

		base = self.path + query_paths['extract']
		query = urlencode(self.query)
		request = Request(self.url + base + '?' + query)
		return self.doRequest(request)

	def uploadData(self, repository, data = "", dataFormat="rdfxml",
				   baseURL="", format="xml", verifyData="yes"):
		"""
		Adds a string ("data") of RDF data to the repository.
		Returns 1 if successful.
		"""
		self.resetQuery()
		self.query['data'] = data
		self.query['repository'] = repository
		self.query['dataFormat'] = dataFormat
		self.query['baseURL'] = baseURL
		self.query['format'] = format
		base = self.path + query_paths['uploadData']
		request = Request(self.url+base)
		query = urlencode(self.query)
		handler = PostHandler()
		return self.doRequest(request, handler, query)

	def uploadURL(self, repository, dataURL, dataFormat="rdfxml",
				  baseURL="", format="xml", verifyData="yes"):
		"""
		Attempts to add whatever is at dataURL to the repository.
		Returns 1 if successful.
		"""
		self.resetQuery()
		self.query['url'] = dataURL
		self.query['repository'] = repository
		self.query['dataFormat'] = dataFormat
		self.query['baseURL'] = baseURL
		self.query['format'] = format
		base = self.path + query_paths['uploadURL']
		request = Request(self.url+base)
		query = urlencode(self.query)
		handler = PostHandler()
		return self.doRequest(request, handler, query)
		
	def clear(self, repository, format="xml"):
		"""
		Clears a repository.
		Returns 1 if successful.
		"""
		self.resetQuery()
		self.query['repository'] = repository
		base = self.path + query_paths['clear']
		request = Request(self.url+base)
		query = urlencode(self.query)
		handler = PostHandler()
		return self.doRequest(request, handler, query)

	def remove(self, repository, subject, predicate, object,
			   resultFormat="xml"):
		"""
		Removes statements from repository.
		Returns 1 if successful.
		"""
		self.resetQuery()
		self.query['repository'] = repository
	
		base = self.path + query_paths['remove']
		request = Request(self.url+base)
		if subject:
			self.query['subject'] = subject
		if predicate:
			self.query['predicate'] = predicate
		if object:
			self.query['object'] = object
		self.query['resultFormat'] = resultFormat
		query = urlencode(self.query)
		handler = PostHandler()
		return self.doRequest(request, handler, query)

	def CookieHandler(self, response):
		value = False
		info = response.info()
		cookies = info.getheaders("Set-Cookie")
		for cookie in cookies:
			if 'sesame_sid' in cookie:
				half = split(cookie,';')[0]
				value = split(half,'=')[-1]
				self.logger.debug('Using cookie %s' % value)
				self.cookie = value
		return value
				

class RepositoriesHandler(ContentHandler):
	"""Creates a list of dictionaries describing available servers."""
	def __init__(self):
		self.inRepository = 0
		self.inTitle = 0
		self.repository = {}
		self.results = []
	def startElement(self, name, attrs):
		if self.inRepository and name == "title":
			self.inTitle = 1
			self.title = ""
		elif name == "repository":
			self.repository['id'] = attrs.get('id', '')
			self.repository['readable'] = attrs.get('readable', '')
			self.repository['writeable'] = attrs.get('writeable', '')
			self.inRepository = 1
	def characters(self, ch):
		if self.inTitle:
			self.title = ch
	def endElement(self, name):
		if name == 'title':
			self.repository['title'] = self.title
			self.inTitle = 0
		elif name == 'repository':
			self.results.append(self.repository)
			self.repository = {}
			self.inRepository = 0
		
class SelectQueryHandler(ContentHandler):
	"""."""
	# this doesn't handle the header yet, right?
	def __init__ (self):
		self.types = ['uri', 'literal', 'bNode','null']
		self.inTuple = 0
		self.inResult = 0
		self.inHeader = 0
		self.header = []
		self.tuple = []
		self.tuples = []
	def startElement(self, name, attrs):
		if self.inTuple and name in self.types:
			self.inResult = 1
			self.value = ""
			self.type = name
		elif name == 'tuple':
			self.inTuple = 1
			self.inResult = 0
		elif name == 'columnName':
			self.inHeader = 1
	def characters(self, ch):
		if self.inResult:
			self.value=ch
			self.tuple.append({'value':self.value,'type':self.type}) 
		if self.inHeader:
			self.header.append(ch)
	def endElement(self, name):
		if name == 'tuple':
			self.tuples.append(self.tuple)
			self.tuple = []
			self.inTuple = 0
		if name in self.types:
			self.inResult = 0
		elif name == 'columnName':
			self.inHeader = 0
		elif name == 'tableQueryResult':
			self.results = {'header':self.header,
							'tuples':self.tuples}


class PostHandler(ContentHandler):
	"""Returns 1 if successful.	 Throws an exception if not."""
	def __init__(self):
		self.results = 1
		self.inMsg = 0
		self.line = ""
		self.elements = ['msg', 'line', 'column']

	def startElement(self, name, attrs):
		if name == "error":
			self.results = 0
		if name in ['status', 'notification', 'warning', 'error']:
			self.tag = name
		if name in self.elements:
			self.inMsg = 1

	def characters(self, ch):
		if self.inMsg:
			self.line += "%s: %s,  " % (self.tag, ch)

	def endElement(self, name):
		if name == "error":
			raise SesameServerError(self.line)
			self.line = ""
		if name in self.elements:
			self.inMsg = 0
			
class SesameServerError(Exception):
	pass
