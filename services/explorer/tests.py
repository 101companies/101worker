from django.test import TestCase, Client
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json


# Basic Test MixIn
# All test cases inherit at least TestBase and TestCase.
class TestBase(object):

	# (manual) SetUp() replacement for cases which rely on json_content.
	def get_json(self):
		self.response = self.client.get(
			self.url, 
			{ 'format': 'json', 'validate': 'true' })
		self.assertEquals(self.response.status_code, 200)
		self.json_content = json.loads(self.response.content)

	# Tests how many members exist (return status_code 200).
	# Asserts zero failures.
	def something_exists(self, something):
		self.get_json()
		broken = 0
		for thing in self.json_content[something]:
			try:
				thing_response = self.client.get(
					thing['resource'],
					{ 'format': 'json', 'validate': 'true' })
				self.assertEquals(thing_response.status_code, 200)
				thing_json_content = json.loads(thing_response.content)
				self.assertEquals(thing_json_content['name'], thing['name'])
			except:
				broken += 1
		self.assertIs(broken, 0)

	# Tests basic json template used and response.
	def test_json(self):
		self.get_json()
		self.assertEquals(self.response.templates, [])
		self.assertEquals(self.json_content['name'], self.name)

	# Tests whether wiki_url is valid and conforms to respective wiki url.
	def test_wiki(self):
		self.get_json()
		self.assertEquals(
			self.json_content['wiki'], 
			'http://101companies.org/wiki/' 
				+ self.json_content['namespace']
				+ self.wiki)
		validate = URLValidator()
		valid_wiki_url = True
		try:
			validate(self.json_content['wiki'])
		except ValidationError, e:
			valid_wiki_url = False
		self.assertTrue(valid_wiki_url)

	# Tests basic html template used and response.
	def test_html(self):
		with self.assertTemplateUsed(self.template + '.html'):
			html_response = self.client.get(
				self.url, 
				{ 'format': 'html', 'validate': 'true' })
		self.assertEquals(html_response.status_code, 200)

	# Tests basic rdf template used and response.
	def test_rdf(self):
		with self.assertTemplateUsed(self.template + '.rdf'):
			rdf_response = self.client.get(
				self.url, 
				{ 'format': 'rdf', 'validate': 'true' })
		self.assertEquals(rdf_response.status_code, 200)

	# Tests basic ttl template used and response.
	def test_ttl(self):
		with self.assertTemplateUsed(self.template + '.ttl'):
			ttl_response = self.client.get(
				self.url, 
				{ 'format': 'ttl', 'validate': 'true' })
		self.assertEquals(ttl_response.status_code, 200)


# Tests whether the content (of a fragment) contains certain keywords in a given order.
class TestContent(object):
	def test_content_in_order(self):
		self.get_json()
		contentstring = self.json_content['content']
		for content in self.content_contains:
			index = contentstring.find(content)
			self.assertTrue(index > -1)
			contentstring = contentstring[index:]


# Tests whether github url exists and is valid.
class TestGithub(object):
	def test_github_exists(self):
		self.get_json()
		self.assertTrue('https://github.com/' in self.json_content['github'])
		validate = URLValidator()
		valid_github_url = True
		try:
			validate(self.json_content['github'])
		except ValidationError:
			valid_github_url = False
		self.assertTrue(valid_github_url)


# Applied something_exits test for namespaces.
class TestNamespace(object):
	def test_members_exist(self):
		self.something_exists('members')


# Applied something_exists test for folders.
class TestFolder(object):
	def test_folders_exist(self):
		self.something_exists('folders')

	def test_files_exist(self):
		self.something_exists('files')


# Applied something_exists test for fragments.
class TestFragment(object):
	def test_members_exist(self):
		self.something_exists('fragments')



# Root Namespace Test

class AllNamespacesTest(TestBase, TestNamespace, TestCase):
	template = 'root'
	url = '/discovery'
	name = 'Namespace'
	wiki = ':Namespace'



# Contribution - HaskellStarter - Type Company Tests

class ContributionNamespacesTest(TestBase, TestNamespace, TestCase):
	template = 'namespace'
	name = 'contributions'
	url = '/discovery/contributions'
	wiki = ':Contribution'

class HaskellStarterNamespaceMemberTest(TestBase, TestFolder, TestCase):
	template = 'folder'
	name = 'haskellStarter'
	url = '/discovery/contributions/haskellStarter'
	wiki = ':haskellStarter'

class HaskellStarterNamespaceMemberPathTest(TestBase, TestFolder, TestGithub, TestCase):
	template = 'folder'
	name = 'src'
	url = '/discovery/contributions/haskellStarter/src'
	wiki = ':haskellStarter'

class HaskellStarterNamespaceMemberFileTest(TestBase, TestFragment, TestGithub, TestCase):
	template = 'folder'
	name = 'Main.hs'
	url = '/discovery/contributions/haskellStarter/src/Main.hs'
	wiki = ':haskellStarter'

class HaskellStarterCompanyFragmentTest(TestBase, TestFragment, TestGithub, TestContent, TestCase):
	template = 'fragment'
	name = 'Company'
	url = '/discovery/contributions/haskellStarter/src/Main.hs/type/Company'
	wiki = ':haskellStarter'
	content_contains = ['type', 'Company', '=']



# Language - Java - Class HelloWorld Tests

class LanguageNamespacesTest(TestBase, TestNamespace, TestCase):
	template = 'namespace'
	name = 'languages'
	url = '/discovery/languages'
	wiki = ':Language'

class JavaNamespaceMemberTest(TestBase, TestFolder, TestCase):
	template = 'folder'
	name = 'Java'
	url = '/discovery/languages/Java'
	wiki = ':Java'

class JavaNamespaceMemberPathTest(TestBase, TestFolder, TestGithub, TestCase):
	template = 'folder'
	name = 'sample'
	url = '/discovery/languages/Java/sample'
	wiki = ':Java'

class JavaNamespaceMemberFileTest(TestBase, TestFragment, TestGithub, TestCase):
	template = 'folder'
	name = 'helloWorld.java'
	url = '/discovery/languages/Java/sample/helloWorld.java'
	wiki = ':Java'

class JavaHelloWorldFragmentTest(TestBase, TestFragment, TestGithub, TestContent, TestCase):
	template = 'fragment'
	name = 'HelloWorld'
	url = '/discovery/languages/Java/sample/helloWorld.java/class/HelloWorld'
	wiki = ':Java'
	content_contains = ['class', 'HelloWorld', '{', '}']
