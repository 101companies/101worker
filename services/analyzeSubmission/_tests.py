"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
import os

# import requests
# import json

# data = open('input.json').read()

# headers = {'content-type': 'application/json'}

# r = requests.post("http://localhost/services/analyzeSubmission", data=data, headers=headers)

# print r.text


class SimpleTest(TestCase):

	def setUp(self):
		self.c = Client()

	def test_request(self):
		with open('analyzeSubmission/input.json', 'r') as f:
			data = f.read()

		response = self.c.post('/analyzeSubmission', data, content_type='application/json')
		print response.templates
		print response.content
		print response.status_code


