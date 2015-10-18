class Section:
	"""A page section"""

	def __init__(self, title, content):
		self.content = content
		self.title = title
		self.subsections = []

	def addSubsection(self, section):
		self.subsections.append(section)