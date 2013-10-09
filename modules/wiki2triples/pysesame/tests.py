
# py_sesame tests.py 
#
# this is a testsuite as used by python's unittest module
# it runs a dozen of tests, catches exceptions, and prints reports
#
# if the test fails it doesn't necessarily mean Sesame is broken,
# it only means the test failed. please check out the purpose
# of the test and the nature of the failure. usually, Sesame
# returned a result in a slightly different format then the test
# expected; e.g. rdf/xml with some extra whitespace, which is 
# harmless.

import unittest
import pySesame

# CONFIG ---------------------
# select an *empty* test database, plain rdf sail
# on which the user has read and write access

url 		= 'http://localhost:8080'
path 		= '/sesame/'
user 		= 'yourusername'
password 	= 'youruserpassword'
repository 	= 'yourrepositoryid'


# ----------------------------

#20050628 *pike moved data out of the file
#20050628 *pike added serql tests

#import some example data
from tests_data import w3c, w3cRemoved, w3cResult, postURL
from tests_data import serqlSQuery, serqlCQuery, rdqlQuery, rdqlQueryResult
from tests_data import rdqlQueryRDF, serqlCQueryRDF, postcon


class AnonymousCase(unittest.TestCase):

	def setUp(self):
		self.connection = pySesame.SesameConnection(url, path, 'debug')
	def tearDown(self):
		self.connection.close()
		
	def testRepositories(self):
		# This assumes that the server has no repositories
		# accessible to anonymous.	You can probably ignore it.
		assert self.connection.repositories() == [], \
			   'There seem to be repositories available for the anonymous user.'

	def testLogin(self):
		assert self.connection.login(user, password) == None, \
			   'Login error.'

	def testLogout(self):
		correct = 'Logged out successfully'
		self.connection.login(user, password)
		assert self.connection.logout() == correct, \
			   'Logout error.'


class TestUserCase(unittest.TestCase):

	def setUp(self):
		self.connection = pySesame.SesameConnection(url, path, 'debug')
		self.connection.login(user, password)

	def tearDown(self):
		self.connection.clear(repository)
		self.connection.logout()
		self.connection.close()

	def testRepositories(self):
		repos = self.connection.repositories()
		ok = True
		for repo in repos:
			if repo["id"]==repository:
				ok = ok and repo["writeable"]
				ok = ok and repo["readable"]
		assert ok, 'Repository %s is not readable or writable'%repository

	def testClearRepository(self):
		assert self.connection.clear(repository) == 1, \
			   'Error in clear.'

	def testUploadBadData(self):
		self.assertRaises(pySesame.SesameServerError,
						  self.connection.uploadData, postcon[:100]) 

	def testUploadData(self):
		assert self.connection.uploadData(repository, postcon) == 1, \
			   'Error in upload.'
		self.connection.clear(repository)

	def testUploadURL(self):
		assert self.connection.uploadURL(repository, postURL) == 1, \
			   'Error in URL load.'

	def testExtract(self):
		"This is rather sensitive to the formatting of the result."
		self.connection.clear(repository)
		self.connection.uploadData(repository, w3c)
		assert self.connection.extract(repository, 'on', 'on') == w3cResult, \
			   'Error in RDF extract.'

	def testRDQLtable(self):
		self.connection.clear(repository)
		self.connection.uploadData(repository, postcon)
		assert self.connection.tableQuery(repository, 'RDQL', rdqlQuery) == \
			   rdqlQueryResult, 'Error in RDQL table query.'

	def testRDQLrdf(self):
		self.connection.clear(repository)
		self.connection.uploadData(repository, postcon)
		assert self.connection.tableQuery(repository, 'RDQL', rdqlQuery, \
			'rdf', 'rdfxml') == rdqlQueryRDF, \
			'RDQL Query, RDF output does not return expected results'

	def testSeRQLselect(self):
		self.connection.clear(repository)
		self.connection.uploadData(repository, postcon)
		assert self.connection.tableQuery(repository, 'SeRQL', serqlSQuery) == \
			rdqlQueryResult, 'SeRQL select query does not return expected results'
	
	
	def testSeRQLconstruct(self):
		self.connection.clear(repository)
		self.connection.uploadData(repository, postcon)
		assert self.connection.graphQuery(repository, 'SeRQL', serqlCQuery, \
			'rdfxml') == serqlCQueryRDF, \
			'SeRQL Construct query, RDF format does not return expected results'
	
	def testRemove(self):
		self.connection.clear(repository)
		self.connection.uploadData(repository, w3c)
		self.connection.remove(repository, '<http://www.w3.org/>', \
							   '<http://purl.org/dc/elements/1.1/title>', \
							   '"World Wide Web Consortium"')
		assert self.connection.extract(repository, 'on', 'on') == \
			   w3cRemoved, 'Remove does not return expected results'
		
if __name__ == "__main__":
	unittest.main()		   
