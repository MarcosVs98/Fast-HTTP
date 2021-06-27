"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import sys
from fasthttp.FastHTTPCommand import FastHTTPCommand

# HTTPClient
from fasthttp.HTTPClient import AsyncTCPConnector
from fasthttp.HTTPClient import AsyncSession
from fasthttp.HTTPClient import AsyncHTTPRequest
from fasthttp.HTTPClient import AsyncRequestTimeout
from fasthttp.HTTPClient import AsyncHTTPClient

# HTTPBenchmark
from fasthttp.HTTPBenchmark import HTTPBenchmark

# Exceptions
from fasthttp.exceptions import BenchmarkingFailed
from fasthttp.exceptions import AsyncHTTPClientException
from fasthttp.exceptions import AsyncHTTPClientEmptyResponseException
from fasthttp.exceptions import AsyncHTTPClientTimeoutException
from fasthttp.exceptions import AsyncHTTPClientTooManyRedirectsException
from fasthttp.exceptions import AsyncHTTPClientResolveHostException
from fasthttp.exceptions import AsyncHTTPUnsupportedMethodException
from fasthttp.exceptions import AsyncLoopException
from fasthttp.exceptions import AsyncHTTPTimeoutException
from fasthttp.exceptions import AsyncHTTPCertificateException
from fasthttp.exceptions import AsyncHTTPConnectionException
from fasthttp.exceptions import AsyncHTTPClientProxyException
from fasthttp.exceptions import AsyncHTTPClientError
from fasthttp.exceptions import BenchmarkingFailed

if len(sys.argv) > 1:
	command = FastHTTPCommand()
	command.execute()
	sys.exit()

# end-of-file