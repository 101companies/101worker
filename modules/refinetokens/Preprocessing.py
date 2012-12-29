__author__ = 'martin'

import re

def isValidToken(token):
	if len(token) > 1:
		return True
	return False

def preprocess(token):
	result = []
	parts = re.split('\s|-|/|=|\"|:|;|<|>|,', token)
	for t in parts:
		if isValidToken(t):
			result.append(t)
	return result