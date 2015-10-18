__author__ = 'martin'

import re

def isValidToken(token):
	if not token: return False

	#currently, the only criteria is that it's length is bigger than 1
	if len(token) > 1:
		return True

	return False

def preProcess(token):
	result = []
	parts = re.split('\s|-|/|=|\"|:|;|<|>|,|\(|\)|\[|\]|\'', token)
	for t in parts:
		if isValidToken(t):
			result.append(t)
	return result