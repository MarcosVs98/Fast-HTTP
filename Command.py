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

		parser.add_argument("-rpd", "--max_requests_per_domain", help="Number of requests per domain",
		                    default=settings.CONCURRENT_REQUESTS_PER_DOMAIN, type=int)
		parser.add_argument("-rpi", "--max_requests_per_ip", help="Number of requests per ip",
		                    default=settings.CONCURRENT_REQUESTS_PER_IP, type=int)
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
		#print(self.args)

		# proxy-list https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
		# https://github.com/clarketm/proxy-list

		# logging.basicConfig(**settings.LOGGING_CONFIG['console_color_debug'])
		# Beleza ficou legal
		#  ab -c 50 -n 1000 https://api.myip.com/
		# ab -c 50 -n 100 https://croquistands.com.br/
		# ab -c 50 -n 100 https://api.myip.com/
		# ab -c 50 -n 100 http://127.0.0.1:8000/api/?method=xpto.get

		# Teste unitario
		# request = HTTPClient()
		# response = request.get('http://127.0.0.1:8000/api/?method=foobar.get&format=json')
		# response = request.get('https://internacional.com.br/')
		# print(response)
		# print(response)

		# Teste assincrono
		# ab -c 50 -n 100 http://127.0.0.1:8000/api/?method=xpto.get
		#url = 'https://www.internacional.com.br/associe-se'
		#url = 'http://127.0.0.1:8000/api/?method=xpto.get'
		#url = 'http://127.0.0.1:8000/api/?method=xpto.get'
		#url = 'https://api.myip.com/'
		#url = 'http://0.0.0.0:9000/'
		# url = 'https://croquistands.com.br/'
		# url = 'https://diaxcapital.com.br/'
		# url ='https://reqres.in/api/users?page=1'


		try:
			assincrone_res = HTTPBenchmark(url='http://0.0.0.0:9000/', method='get', concurrent_requests=25, concurrent_blocks=100)
			assincrone_res.run()

		except Exception as e:
			print(e)


#c = Command()
#c.execute()

#from HTTPClient import HTTPClient

#r = HTTPClient()
#resp = r.get('https://www.python.org/')

#print(resp.links)

#print(resp.raw_headers)

# end-of-file