"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""

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


class AsyncHTTPClientException(Exception):
	pass


class AsyncHTTPClientEmptyResponseException(AsyncHTTPClientException):
	pass


class AsyncHTTPClientTimeoutException(AsyncHTTPClientException):
	pass


class AsyncHTTPClientTooManyRedirectsException(AsyncHTTPClientException):
	pass


class AsyncHTTPClientResolveHostException(AsyncHTTPClientException):
	pass


class AsyncHTTPUnsupportedMethodException(AsyncHTTPClientException):
	pass


class AsyncLoopException(Exception):
	pass


class AsyncHTTPTimeoutException(AsyncHTTPClientException):
	pass


class AsyncHTTPCertificateException(AsyncHTTPClientException):
	pass


class AsyncHTTPConnectionException(AsyncHTTPClientException):
	pass


class AsyncHTTPClientProxyException(AsyncHTTPClientException):
	pass


class AsyncHTTPClientError(AsyncHTTPClientException):
	pass

# end-of-file