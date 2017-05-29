class Node:

	def __init__(self, token):
		
		self.index = token['index']
		self.pos = token['pos']
		self.word = token['word']
		self.originalText = token['originalText']
		self.characterOffsetEnd = token['characterOffsetEnd']
		self.characterOffsetBegin = token['characterOffsetBegin']
		self.after = token['after']
		self.before = token['before']