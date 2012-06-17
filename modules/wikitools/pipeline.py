# -*- coding: utf-8 -*-

class Step:
	def __init__(self, action, name):
		self.action = action
		self.name   = name

class Pipeline:
	def __init__(self):	
		self.steps = []

	def addStep(self, s):
		self.steps.append(s)

	def execute(self, page, idx = 0):
		# The output of the previous step serves as an input to the next step
		print "Executing step: " + self.steps[idx].name
		res = self.steps[idx].action(page)
		if idx < (len(self.steps) - 1):
			return self.execute(res, idx+1)
		else:
			return res
