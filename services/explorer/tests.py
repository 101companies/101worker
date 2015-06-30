from django.test import TestCase, Client
import json

class TestMixin(object):

	def test_json(self):
		response = self.client.get(self.url, { 'format': 'json', 'validate': 'true' })

		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.templates, [])

		json_content = json.loads(response.content)
		self.assertEquals(json_content['name'], self.name)
		

	def test_html(self):
		with self.assertTemplateUsed(self.template + '.html'):
			response = self.client.get(self.url, { 'format': 'html', 'validate': 'true' })

		# self.assertTrue(len(response.context['members']) > 0)
		self.assertEquals(response.status_code, 200)

	def test_rdf(self):
		with self.assertTemplateUsed(self.template + '.rdf'):
			response = self.client.get(self.url, { 'format': 'rdf', 'validate': 'true' })

		self.assertEquals(response.status_code, 200)

	def test_ttl(self):
		with self.assertTemplateUsed(self.template + '.ttl'):
			response = self.client.get(self.url, { 'format': 'ttl', 'validate': 'true' })

		self.assertEquals(response.status_code, 200)

class AllNamespacesTest(TestCase, TestMixin):

	template = 'root'
	url = '/discovery'
	name = 'Namespace'

class SingleNamespacesTest(TestCase, TestMixin):

	template = 'namespace'
	name = 'contributions'
	url = '/discovery/contributions'

class NamespaceMemberTest(TestCase, TestMixin):

	template = 'folder'
	name = 'haskellStarter'
	url = '/discovery/contributions/haskellStarter'

class NamespaceMemberPathTest(TestCase, TestMixin):

	template = 'folder'
	name = 'src'
	url = '/discovery/contributions/haskellStarter/src'

class FragmentTest(TestCase, TestMixin):

	template = 'fragment'
	name = 'Company'
	url = '/discovery/contributions/haskellStarter/src/Main.hs/type/Company'

# class AllNamespacesTest(TestCase):

# 	def test_json(self):
# 		response = self.client.get('/discovery/', { 'format': 'json', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)
# 		self.assertEquals(response.templates, [])

# 		json_content = json.loads(response.content)
# 		self.assertEquals(json_content['name'], 'Namespace')
		

# 	def test_html(self):
# 		with self.assertTemplateUsed('root.html'):
# 			response = self.client.get('/discovery/', { 'format': 'html', 'validate': 'true' })

# 		self.assertTrue(len(response.context['members']) > 0)

# 	def test_rdf(self):
# 		with self.assertTemplateUsed('root.rdf'):
# 			response = self.client.get('/discovery/', { 'format': 'rdf', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)

# 	def test_ttl(self):
# 		with self.assertTemplateUsed('root.ttl'):
# 			response = self.client.get('/discovery/', { 'format': 'ttl', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)

# class SingleNamespacesTest(TestCase):

# 	def test_json(self):
# 		response = self.client.get('/discovery/contributions', { 'format': 'json', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)
# 		self.assertEquals(response.templates, [])

# 		json_content = json.loads(response.content)
# 		self.assertEquals(json_content['name'], 'contributions')
		

# 	def test_html(self):
# 		with self.assertTemplateUsed('namespace.html'):
# 			response = self.client.get('/discovery/contributions', { 'format': 'html', 'validate': 'true' })

# 		self.assertTrue(len(response.context['members']) > 0)

# 	def test_rdf(self):
# 		with self.assertTemplateUsed('namespace.rdf'):
# 			response = self.client.get('/discovery/contributions', { 'format': 'rdf', 'validate': 'true' })


# 	def test_ttl(self):
# 		with self.assertTemplateUsed('namespace.ttl'):
# 			response = self.client.get('/discovery/contributions', { 'format': 'ttl', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)

# class NamespaceMemberTest(TestCase):

# 	def test_json(self):
# 		response = self.client.get('/discovery/contributions/haskellStarter/', { 'format': 'json', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)
# 		self.assertEquals(response.templates, [])

# 		json_content = json.loads(response.content)
# 		self.assertEquals(json_content['name'], 'haskellStarter')
		

# 	def test_html(self):
# 		with self.assertTemplateUsed('folder.html'):
# 			response = self.client.get('/discovery/contributions/haskellStarter/', { 'format': 'html', 'validate': 'true' })

# 		self.assertTrue(len(response.context['files']) > 0)
# 		self.assertTrue(len(response.context['folders']) > 0	)

# 	def test_rdf(self):
# 		with self.assertTemplateUsed('folder.rdf'):
# 			response = self.client.get('/discovery/contributions/haskellStarter/', { 'format': 'rdf', 'validate': 'true' })

# class NamespaceMemberPathTest(TestCase):

# 	def test_json(self):
# 		response = self.client.get('/discovery/contributions/haskellStarter/src', { 'format': 'json', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)
# 		self.assertEquals(response.templates, [])

# 		json_content = json.loads(response.content)
# 		self.assertEquals(json_content['name'], 'src')
# 		self.assertEquals(json_content['github'], "https://github.com/101companies/101haskell/tree/master/contributions/haskellStarter/src")
		

# 	def test_html(self):
# 		with self.assertTemplateUsed('folder.html'):
# 			response = self.client.get('/discovery/contributions/haskellStarter/src', { 'format': 'html', 'validate': 'true' })

# 		self.assertTrue(len(response.context['files']) > 0)
# 		self.assertEquals(response.status_code, 200)

# 	def test_rdf(self):
# 		with self.assertTemplateUsed('folder.rdf'):
# 			response = self.client.get('/discovery/contributions/haskellStarter/src', { 'format': 'rdf', 'validate': 'true' })

# 		self.assertEquals(response.status_code, 200)

