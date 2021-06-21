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
from FastHTTPCommand import FastHTTPCommand

# HTTPClient
from HTTPClient import AsyncTCPConnector
from HTTPClient import AsyncSession
from HTTPClient import AsyncHTTPRequest
from HTTPClient import AsyncRequestTimeout

# HTTPBenchmark
from HTTPBenchmark import HTTPBenchmark

# Exceptions
from exceptions import BenchmarkingFailed
from exceptions import AsyncHTTPClientException
from exceptions import AsyncHTTPClientEmptyResponseException
from exceptions import AsyncHTTPClientTimeoutException
from exceptions import AsyncHTTPClientTooManyRedirectsException
from exceptions import AsyncHTTPClientResolveHostException
from exceptions import AsyncHTTPUnsupportedMethodException
from exceptions import AsyncLoopException
from exceptions import AsyncHTTPTimeoutException
from exceptions import AsyncHTTPCertificateException
from exceptions import AsyncHTTPConnectionException
from exceptions import AsyncHTTPClientProxyException
from exceptions import AsyncHTTPClientError
from exceptions import BenchmarkingFailed

if sys.argv[1]:
	command = FastHTTPCommand()
	command.execute()
	sys.exit()

# end-of-file