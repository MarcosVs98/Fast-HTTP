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
from HTTPBenchmark import HTTPBenchmark

def validate_url(url):
	uri = urlparse(url)
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
		                   formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('url', help="URL", type=validate_url)

		parser.add_argument("-m", "--method", help="HTTP method",
		                    default='get', type=str)
		parser.add_argument("-rph", "--max_requests_per_host", help="Number of requests per host",
		                    default=settings.LIMIT_REQUESTS_PER_HOST, type=int)
		parser.add_argument("-rpi", "--max_requests_per_ip", help="Number of requests per ip",
		                    default=settings.LIMIT_REQUESTS_PER_IP, type=int)
		parser.add_argument("-d", "--max_delay", help="Maximum delay on request",
		                    default=settings.AUTOTHROTTLE_MAX_DELAY, type=float)
		parser.add_argument("-s", "--start_delay", help="Delay at the start of the request",
		                    default=settings.AUTOTHROTTLE_START_DELAY, type=float)
		parser.add_argument("-sd", "--sock_delay", help="Delay on socket request",
		                    default=settings.AUTOTHROTTLE_SOCK_DELAY, type=float)
		parser.add_argument("-rd", "--read_delay", help="Delay for reading request",
		                    default=settings.AUTOTHROTTLE_READ_DELAY, type=float)
		parser.add_argument("-T", "--telnet", help="Telnet console (enabled by default)",
		                    default=settings.TELNETCONSOLE_ENABLED, type=bool)
		parser.add_argument("-R", "--roundrobin", help="Distribute http requests via network interface",
		                    default=settings.ROUNDROBIN_ACTIVE, type=bool)
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
		parser.add_argument("-pp", "--public_proxy",
							help="Public proxies list", type=str)
		parser.add_argument("-mp", "--list_proxy",
							help="list of proxies separated by uri and authentication, in txt format", type=str)
		parser.add_argument("-S", "--verify_ssl", help="Disable SSL ceertificate",
		                    default=settings.VERIFY_SSL, type=bool)
		parser.add_argument("-E", "--certfile",
		                    help="Specify optional client certificate chain and private key",
                            type=str)
		self.args = parser.parse_args()

	def execute(self):
		try:
			assincrone_res = HTTPBenchmark(url=self.args.url, method=self.args.method, concurrent_requests=self.args.concurrent, concurrent_blocks=self.args.block)
			assincrone_res.perform()

		except Exception as e:
			print(e)

c = Command()
c.execute()

# end-of-file