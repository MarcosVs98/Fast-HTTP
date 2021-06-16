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
from utils import Structure
from utils import get_family
from utils import str_to_tuple
from utils import str_int_to_tuple
from utils import validate_url
from HTTPClient import AsyncTCPConnector
from HTTPClient import AsyncSession
from HTTPClient import AsyncHTTPRequest
from HTTPClient import AsyncRequestTimeout
from HTTPBenchmark import HTTPBenchmark

log = logging.getLogger('command')


class CommandGroups(Structure):
	pass


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
		connector = parser.add_argument_group('connector')
		session = parser.add_argument_group('session')
		request = parser.add_argument_group('request')
		benchmark = parser.add_argument_group('benchmark')
		timeout = parser.add_argument_group('timeout')

		request.add_argument('url', help="URL", type=validate_url)
		request.add_argument("-m", "--method", help="HTTP method", default='get', type=str)
		request.add_argument("-ar", "--allow_redirects", help='Allow redirects', type=bool,
							   default=settings.ALLOW_REDIRECTS)
		request.add_argument("-mr", "--redirects", help="Maximum number of redirects",
							   default=settings.MAX_REDIRECTS, type=int)
		request.add_argument("-k", "--postdata",
							   help="data to be sent via post", type=json.dumps)
		request.add_argument("-H", "--header", action='store', help="add header line",
							   default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		request.add_argument("-PH", "--proxy_headers", action='store', help="add proxy header line",
							   default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		request.add_argument("-pU", "--proxy_user", type=str,
							   help="Add Basic Proxy Authentication, [user]", default=None)
		request.add_argument("-pP", "--proxy_pass", type=str,
							   help="Add Basic Proxy Authentication, [pass]", default=None)
		request.add_argument("-S", "--verify_ssl", help="Disable SSL ceertificate",
							   default=settings.VERIFY_SSL, type=bool)
		request.add_argument("-E", "--sslcontext", help="Specify optional client certificate chain and private key",
							   default=settings.DEFAULT_SSL_CONTEXT, type=str)
		request.add_argument("-X", "--proxy",
							   help="Proxyserver and port number proxy:server", type=str)
		connector.add_argument("-cs", "--connector_ssl", help="SSL validation mode.", type=str,
							   default=settings.VERIFY_SSL)
		connector.add_argument("-cf", "--fingerprint",
							   help="Fingerprint helper for checking SSL certificates by SHA256 digest.", type=str,
							   default=settings.SSL_CERTIFICATE_VALIDATION)
		connector.add_argument("-cds", "--use_dns_cache",
							   help="use internal cache for DNS lookups", type=int,
							   default=settings.USE_DNS_CACHE)
		connector.add_argument("-tt", "--ttl_dns_cache",
							   help="Expire after some seconds the DNS entries", type=int,
							   default=settings.TTL_DNS_CACHE)
		connector.add_argument("-fm", "--family", help="TCP socket family", type=get_family,
							   default=settings.TCP_SOCKET_FAMILY.get(4, 0))
		connector.add_argument("-cE", "--connector_ssl_context",
							   help="Specify optional client certificate chain and private key [connection]",
							   default=settings.DEFAULT_SSL_CONTEXT, type=str)
		connector.add_argument("-cA", "--local_addr",
							   help="Tuple of (local_host, local_port) used to [connection]",
							   default=settings.DEFAULT_ADDRESS, type=tuple)
		connector.add_argument("-cR", "--resolver", help="Custom resolvers allow you to resolve hostnames",
							   default=settings.RESOLVE_HOSTNAME, type=bool)
		connector.add_argument("-cF", "--force_close",
							   help="close underlying sockets after connection releasing (optional).",
							   default=settings.CLOSE_ALL_SOCKETS)
		connector.add_argument("-cL", "--limit", help="Total number simultaneous connections",
							   default=settings.LIMIT_CONNECTIONS, type=int)
		connector.add_argument("-cH", "--limit_per_host", help="Limit simultaneous connections to the same endpoint",
							   default=settings.LIMIT_REQUESTS_PER_HOST, type=int)
		connector.add_argument("-cC", "--enable_cleanup_closed",
							   help="Aborts underlining transport after 2 seconds. It is off by default.",
							   default=settings.SHUTDOWN_TRANSPORT, type=bool)
		session.add_argument("-sC", "--cookies", action='store',
							   help="add cookie line",type=json.dumps)
		session.add_argument("-sH", "--headers", action='store', help="add header line",
							   default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		session.add_argument("-sK", "--skip_auto_headers", action='store', help="add header line",
							   default=settings.DEFAULT_REQUEST_HEADERS, type=json.dumps)
		session.add_argument("-sAu", "--auth", default=None, type=str_to_tuple)
		session.add_argument("-sV", "--version",
							   help="HTTP Version", default=(1, 1), type=str_int_to_tuple)
		session.add_argument("-sJ", "--json_serialize", help="Python’s standard json module for serialization.",
							   default=json.dumps, type=json.dumps)
		session.add_argument("-sM", "--conn_timeout",
							   help="add header line", default=None, type=float)
		session.add_argument("-sR", "--raise_for_status", help="call raise for status for all answers not ok",
							   default=False, type=bool)
		session.add_argument("-sO", "--connector_owner", help="Should connector be closed on session closing",
							   default=settings.CONNECTOR_OWNER, type=bool)
		session.add_argument("-sD", "--auto_decompress", help="Should the body response be automatically decompressed",
							   default=settings.AUTO_DESCOMPRESS, type=bool)
		session.add_argument("-sB", "--read_bufsize", help="Size of the read buffer",
							   default=settings.READ_BUFSIZE, type=int)
		session.add_argument("-sQ", "--requote_redirect_url",
			help="To disable re-quote system set requote_redirect_url attribute", default=bool)
		session.add_argument("-sT", "--trust_env",
							   help="Get proxies information from HTTP_PROXY / HTTPS_PROXY environment variables",
							 default=bool)
		session.add_argument("-sF", "--trace_configs",
							   help="Get proxies information from HTTP_PROXY / HTTPS_PROXY environment variables",
							   default=bool)
		benchmark.add_argument("-T", "--telnet", help="Telnet console (enabled by default)",
							   default=settings.TELNETCONSOLE_ENABLED, type=bool)
		benchmark.add_argument("-lp", "--limit_per_ip", help="Limit simultaneous connections to the same ip",
							   default=settings.LIMIT_REQUESTS_PER_IP, type=int)
		benchmark.add_argument("-c", "--concurrency", help="Number of simultaneous requests",
							   default=settings.CONCURRENT_REQUESTS, type=int)
		benchmark.add_argument("-b", "--block", help="Number of request blocks",
							   default=settings.CONCURRENT_BLOCKS, type=int)
		benchmark.add_argument("-B", "--outbound_address", help="Address to bind to when making outgoing connections",
							   default=settings.DEFAULT_ADDRESS, type=str)
		benchmark.add_argument("-pp", "--public_proxy",
							   help="Public proxies list", type=str)
		timeout.add_argument("-d", "--total", help="Maximum delay on request [start]",
							   default=settings.AUTOTHROTTLE_MAX_DELAY, type=float)
		timeout.add_argument("-s", "--connect", help="Delay at the start of the request [connect]",
							   default=settings.AUTOTHROTTLE_START_DELAY, type=float)
		timeout.add_argument("-sd", "--sock_connect", help="Delay on socket request [socket]",
							   default=settings.AUTOTHROTTLE_SOCK_DELAY, type=float)
		timeout.add_argument("-rd", "--sock_read", help="Delay for reading request [read]",
							   default=settings.AUTOTHROTTLE_READ_DELAY, type=float)
		benchmark.add_argument("-R", "--roundrobin", help="Distribute http requests via network interface",
							   default=settings.ROUNDROBIN_ACTIVE, type=bool)
		benchmark.add_argument("-mp", "--list_proxy",
							   help="list of proxies separated by uri and authentication, in txt format", type=str)
		args = parser.parse_args()

		self.arg_groups = CommandGroups()

		for group in parser._action_groups:
			group_dict = { a.dest.replace(f"{group.title}_", "") : getattr(args, a.dest, None) for a in group._group_actions }
			self.arg_groups[group.title] = argparse.Namespace(**group_dict)

	def execute(self):
		try:
			# create timeout
			timeout =  AsyncRequestTimeout(**vars(self.arg_groups.timeout))
			#create connector
			connector = AsyncTCPConnector(**vars(self.arg_groups.connector))
			# set session args
			self.arg_groups.session.connector = connector
			# crate session
			session = AsyncSession(**vars(self.arg_groups.session))
			# set request timeout
			self.arg_groups.request.timeout = timeout
			# crate request
			request = AsyncHTTPRequest(**vars(self.arg_groups.request))
			# create benchmark
			benchmark = HTTPBenchmark(
				url=request.url,
				method=request.method,
				concurrent_requests=self.arg_groups.benchmark.concurrency,
				concurrent_blocks=self.arg_groups.benchmark.block)
			try:
				benchmark.perform()
			except KeyboardInterrupt:
				log.warning('CTRL+C Detected!')
		except Exception as e:
			log.error(e)

c = Command()

c.execute()

# end-of-file