class Step:
	def __init__(self, action, name):
		self.action = action
		self.name   = name

class Pipeline:
	def __init__(self):	
		self.steps = []

	def addStep(self, s):
		self.steps.append(s)

	def execute(self, page):
		# TODO: page is a input for the first step
		# The output of the previous step serves as an input to the next step
		return self.steps[0].action(page)