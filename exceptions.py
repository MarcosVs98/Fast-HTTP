class FailedAIO(Exception):
	"""
		Um wrapper de todas as exceções possíveis durante uma solicitação 
	"""
	code, message, loop, raised = 0, '', '', ''

	def __init__(self, *, raised='', message='', code='', url='', loop=''):
		self.raised  = raised
		self.message = message
		self.code    = code
		self.loop    = loop

# end-of-file #