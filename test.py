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
import argparse
from argparse import RawTextHelpFormatter


def validate_url(uri):
	if not all((uri.scheme, uri.netloc, uri.path)):
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
							formatter_class=RawTextHelpFormatter)
		parser.add_argument('url', help="uRL", type=url_validator)

		parser.add_argument("-n", "--concurrent", help="Number of requests to perform",
							default=1, type=int)
		parser.add_argument("-c", "--concurrent", help="Number of simultaneous requests",
							default=[settings], type=int)
		parser.add_argument("-b", "--block", help="Number of request blocks",
							default=[setting], type=int)
		parser.add_argument("-t", "--timeout", help="Number of request blocks",
							default=[setting], type=int)
		parser.add_argument("-b", "--bind_address", help="Address to bind to when making outgoing connections",
							default=[setting], type=int)
		parser.add_argument("-p", "--postdata", help="data to be sent via post",
							default=[setting], type=int)
		parser.add_argument("-H", "--header", action='store', help="add header line",
							default=[setting], type=str)
		parser.add_argument("-C", "--cookie", action='store', help="add cookie line",
							default=[setting], type=str)
		parser.add_argument("-P", "--proxy", help="Proxyserver and port number proxy:server",
							default=[setting], type=int)
		parser.add_argument("-S", "--ssl_disable", help="Disable SSL ceertificate",
							default=[setting], type=bool)
		parser.add_argument("-E", "--certfile", help="Specify optional client certificate chain and private key",
							default=[settings], type=str)
		self.args = parser.parse_args()

	def run(self):
		pass

# end-of-file