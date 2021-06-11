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
import logging
from urllib.parse import urlparse
from HTTPClient import AsyncTCPConnector
from HTTPClient import AsyncSession
from HTTPClient import AsyncHTTPRequest
from HTTPBenchmark import HTTPBenchmark

log = logging.getLogger('command')

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
		parser.add_argument("-au", "--auth_user",
							help="Add Basic Authentication, [user]", default=None, type=str)
		parser.add_argument("-ap", "--auth_pass",
							help="Add Basic Authentication, [pass]", default=None, type=str)
		parser.add_argument("-rph", "--max_requests_per_host", help="Number of requests per host",
		                    default=settings.LIMIT_REQUESTS_PER_HOST, type=int)
		parser.add_argument("-rpi", "--max_requests_per_ip", help="Number of requests per ip [round-robin]",
		                    default=settings.LIMIT_REQUESTS_PER_IP, type=int)
		parser.add_argument("-d", "--max_delay", help="Maximum delay on request [start]",
		                    default=settings.AUTOTHROTTLE_MAX_DELAY, type=float)
		parser.add_argument("-s", "--start_delay", help="Delay at the start of the request [connect]",
		                    default=settings.AUTOTHROTTLE_START_DELAY, type=float)
		parser.add_argument("-sd", "--sock_delay", help="Delay on socket request [socket]",
		                    default=settings.AUTOTHROTTLE_SOCK_DELAY, type=float)
		parser.add_argument("-rd", "--read_delay", help="Delay for reading request [read]",
		                    default=settings.AUTOTHROTTLE_READ_DELAY, type=float)
		parser.add_argument("-T", "--telnet", help="Telnet console (enabled by default)",
							default=settings.TELNETCONSOLE_ENABLED, type=bool)
		parser.add_argument("-0", "--http1.0",
							help="Use HTTP 1.0", type=int)
		parser.add_argument("-1", "--http1.1",
							help="Use HTTP 1.1", type=int)
		parser.add_argument("-R", "--roundrobin", help="Distribute http requests via network interface",
		                    default=settings.ROUNDROBIN_ACTIVE, type=bool)
		parser.add_argument("-mr", "--maxredirects", help="Maximum number of redirects",
								default=settings.MAX_REDIRECTS, type=int)
		parser.add_argument("-c", "--concurrency", help="Number of simultaneous requests",
		                    default=settings.CONCURRENT_REQUESTS, type=int)
		parser.add_argument("-b", "--block", help="Number of request blocks",
		                    default=settings.CONCURRENT_BLOCKS, type=int)
		#parser.add_argument("-t", "--timeout", help="Request timeout",
		#                    default=settings.DEFAULT_REQUEST_TIMEOUT, type=int)
		parser.add_argument("-B", "--bind_address", help="Address to bind to when making outgoing connections",
		                    default=settings.DEFAULT_ADDRESS, type=str)
		parser.add_argument("-d", "--postdata",
		                    help="data to be sent via post", type=json.dumps)
		parser.add_argument("-H", "--header", action='store', help="add header line",
		                    default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		parser.add_argument("-PH", "--proxy_header", action='store', help="add proxy header line",
							default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		parser.add_argument("-C", "--cookie", action='store',
		                    help="add cookie line",type=json.dumps)
		parser.add_argument("-pU", "--proxy_user", type=str,
							help="Add Basic Proxy Authentication, [user]", default=None)
		parser.add_argument("-pP", "--proxy_pass", type=str,
							help="Add Basic Proxy Authentication, [pass]", default=None)
		parser.add_argument("-X", "--proxy",
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

			if self.args.roundrobin:
				# optar pelo algoritimo de round robin
				pass

			if self.args.verify_ssl:
				pass

			if self.args.public_proxy:
				# implementar a abertura da lista de proxies
				pass

			if self.args.list_proxy:
				# apresentar listagem de proxies adiquirida
				pass

			if self.args.proxy:
				pass

			if self.args.telnet:
				# abrir interface de redes
				pass


			self.args.timeout= {
				'total': self.args.max_delay,
				'connect': self.args.start_delay,
				'sock_connect': self.args.sock_delay,
				'sock_read': self.args.read_delay
			}

			connector = AsyncTCPConnector(
				ssl=self.args.verify_ssl,
				fingerprint = None
				use_dns_cache = None
				ttl_dns_cache = None
				family = None
				ssl_context = None
				local_addr = None
				resolver = None
				force_close = None
				limit = None
				limit_per_host=self.args.max_requests_per_host
				enable_cleanup_closed = None
				loop = None
			)

			# Crate session
			session = AsyncSession(
				loop=None,
				cookies=self.args.cookie,
				headers=self.args.header,
				skip_auto_headers=None,
				auth=None,
				version=None,
				json_serialize=None,
				cookie_jar=None,
				conn_timeout=None,
				raise_for_status=None,
				connector_owner=None,
				auto_decompress=None,
				read_bufsize=None,
				requote_redirect_url=None,
				trust_env=None,
				trace_configs=None,
			)

			# Crate request
			request = AsyncHTTPRequest(
				url=self.args.url,
				method=self.args.method,
				headers=self.args.header,
				timeout=self.args.timeout,
				security_web=None,
				postdata=self.args.postdata,
				http_version=None,
				auth_user=self.args.auth_user,
				auth_pass=self.args.auth_pass,
				allow_redirects=None,
				redirects=self.args.maxredirects,
				proxy=self.proxy,
				proxy_user=self.args.proxy_user,
				proxy_pass=self.args.proxy_user,
				outbound_address=self.args.bind_address,
				verify_ssl=self.args.verify_ssl,
				sslcontext=self.args.certfile,
				proxy_headers=self.args.proxy_header,
				raise_for_status=None
			)

			benchmark = HTTPBenchmark(
				url=self.args.url,
				method=self.args.method,
				concurrent_requests=self.args.concurrency,
				concurrent_blocks=self.args.block)
			benchmark.perform()

		except Exception as e:
			print(e)

c = Command()
print(c.args)
c.execute()

# end-of-file