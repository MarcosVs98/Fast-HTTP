"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
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


class BenchmarkingFailed(AsyncHTTPClientException):
	pass

# end-of-file