"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import json
import sys
import argparse
import settings
from urllib.parse import urlparse

def validate_url(url):
	uri = urlparse(url)
	if not all((uri.scheme, uri.netloc)):
		raise argparse.ArgumentTypeError(
			"URL used for fetching is malformed, e.g. it does not contain host part")
	return uri.geturl()

class Command():
	"""
	Class responsible for implementing a command pattern.
	ref: https://en.wikipedia.org/wiki/Command_pattern.
	"""
	def __init__(self):
		self.add_options()

	def add_options(self):
		parser = argparse.ArgumentParser(description="Fast-HTTP [options] [http[s]://]hostname[:port]/path",
							formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('url', help="uRL", type=validate_url)

		parser.add_argument("-n", "--requests", help="Number of requests to perform",
							default=settings.CONCURRENT_REQUESTS, type=int)
		parser.add_argument("-c", "--concurrent", help="Number of simultaneous requests",
							default=settings.CONCURRENT_REQUESTS, type=int)
		parser.add_argument("-b", "--block", help="Number of request blocks",
							default=settings.CONCURRENT_BLOCKS, type=int)
		parser.add_argument("-t", "--timeout", help="Number of request blocks",
							default=settings.DEFAULT_REQUEST_TIMEOUT, type=int)
		parser.add_argument("-B", "--bind_address", help="Address to bind to when making outgoing connections",
							default=settings.DEFAULT_ADDRESS, type=str)
		parser.add_argument("-p", "--postdata",
							help="data to be sent via post", type=json.dumps)
		parser.add_argument("-H", "--header", action='store', help="add header line",
							default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		parser.add_argument("-C", "--cookie", action='store',
							help="add cookie line",type=json.dumps)
		parser.add_argument("-P", "--proxy",
							help="Proxyserver and port number proxy:server", type=str)
		parser.add_argument("-S", "--verify_ssl", help="Disable SSL ceertificate",
							default=settings.VERIFY_SSL, type=bool)
		parser.add_argument("-E", "--certfile",
							help="Specify optional client certificate chain and private key",
							type=str)
		self.args = parser.parse_args()

	def run(self):
		print(self.args)

c = Command()
c.run()
# end-of-file