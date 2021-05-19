"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import io
import ssl
import json
import time
import types
import random
import logging
import asyncio
import aiohttp
from queue import Queue
from entities import Structure
from dataclasses import dataclass
from dataclasses import field
from aiohttp.helpers import BasicAuth
from urllib.parse import urlencode, urlparse

# exceptions
from exceptions import FailedAIO
from types import SimpleNamespace

# settings
from settings import DEFAULT_REQUEST_HEADERS
from settings import DEFAULT_REQUEST_TIMEOUT
from settings import CONCURRENT_BLOCKS
from settings import CONCURRENT_REQUESTS


log = logging.getLogger('HTTPClient')


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


@dataclass
class ClientSession(Structure):
	"""
	Class responsible for setting up an interface for making HTTP requests.
	The session encapsulates a set of connections supporting keepalives by default.
	"""
	#connector            : aiohttp.BaseConnector = field(default=None)
	loop                 : str = field(default=None)
	cookies              : dict = field(default=None)
	headers              : dict = field(default=None)
	skip_auto_headers    : str = field(default=None)
	auth                 : aiohttp.BasicAuth = field(default=None)
	json_serialize       : dict = field(default=json.dumps)
	cookie_jar           : aiohttp.DummyCookieJar = field(default=None)
	conn_timeout         : float = field(default=10)
	timeout              : int = field(default=30)
	raise_for_status     : bool = field(default=False)
	connector_owner      : bool = field(default=True)
	auto_decompress      : bool = field(default=True)
	read_bufsize         : int = field(default=2 ** 16)
	requote_redirect_url : bool = field(default=True)
	trust_env            : bool = field(default=False)
	trace_configs        : bool = field(default=False)

	def connect(self):
		self.connection = aiohttp.ClientSession()
		return self.connection

	async def __aenter__(self):
		return self.connect()

	async def __aexit__(self, exc_type, exc, tb):
		return self.connect().close()

	async def __aiter__(self):
		with aiohttp.Timeout(self.timeout):
			return self

	async def __await__(self):
		return self.connect().__await()


class AssyncHTTPResponse(Structure):
	"""
		Data class responsible for encapsulating responses from HTTP requests.
		ClientResponse supports asynchronous context manager protocol.
	"""
	def __str__(self):
		self.summary = SimpleNamespace(**
			{k:v for k,v in self.__dict__.items() if k not in ['content_text']})
		return (f'<FHTTP Response [{self.summary.status} '
				f'{self.summary.reason if not self.summary.status == 200 else "OK"}]>')

	def request_info(self):
		return str(self.__dict__.items())

	def __repr__(self):
		return __str__()

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass


@dataclass
class HTTPRequest(Structure):
	"""
	Data class responsible for representing
	the fields of an HTTP request.
	"""
	url               : str 
	method            : str
	domain            : str = field(default=None)
	scheme            : str = field(default=None)
	headers           : dict = field(default=None) 
	timeout           : int = field(default=120)
	postdata          : bytes = field(default=None, repr=False)
	http_version      : str = field(default='HTTP/1.1')
	security_web      : bool = field(default=False) 
	auth_user         : str = field(default=None)
	auth_pass         : str = field(default=None)
	follow_redirects  : bool = field(default=True)
	redirects         : int = field(default=30)
	proxy_host        : str = field(default=None)
	proxy_port        : int = field(default=0)
	proxy_user        : str = field(default=None)
	proxy_pass        : str = field(default=None)
	outbound_address  : str = field(default=None)
	verify_ssl        : bool = field(default=False)
	sslcontext        : str = field(default=None)
	proxy_headers     : dict = field(default=None) 
	raise_for_status  : bool = field(default=False)

	def __post_init__(self):
		self.method = self.method.upper()
		uri = urlparse(self.url)
		self.domain = uri.netloc
		self.scheme = uri.scheme

	def __setattr__(self, name, value):
		if name == 'url':
			uri = urlparse(value)
			self.__dict__['domain'] = uri.netloc
			self.__dict__['scheme'] = uri.scheme
		self.__dict__[name] = value


class HTTPClient():
	"""
	Class responsible for executing asynchronous HTTP requests
	and return response objects.
	"""
	def __init__(self):
		self._loop = None

	async def auto_decode(self, content):
		for enc in ['ascii', 'utf8', 'iso-8859-1', 'cp-1252']:
			try:
				return await content(enc)
			except UnicodeDecodeError:
				pass

	async def send_request(self, request=None, **kwargs):
		"""
		method responsible for handling an HTTP request.
		"""
		if request is None:
			request = HTTPRequest(**kwargs)

		log.debug(f'HTTP Client Request: {request}')
		# AIO Request
		aio_request = SimpleNamespace()

		# URL
		uri = urlparse(request.url)
		# validate if it is a valid url
		if not all((uri.scheme, uri.netloc, uri.path)):
			raise aiohttp.InvalidURL(
			   "URL used for fetching is malformed, e.g. it does not contain host part")
		aio_request.url = uri.geturl()

		# Request Headers
		if request.headers is not None:
			if not isinstance(request.headers, (list, tuple)):
				raise AsyncHTTPClientException(f'Invalid request headers')
			if not all(isinstance(i, (tuple, list)) for i in request.headers):
				raise AsyncHTTPClientException(f'Invalid request headers')
			if not all(len(i) == 2 for i in request.headers):
				raise AsyncHTTPClientException(f'Invalid request headers')
			rawheaders = [f'{k}: {v}' for k, v in request.headers]
			# ajustar
			aio_request.headers = DEFAULT_REQUEST_HEADERS
		else:
			request.headers = DEFAULT_REQUEST_HEADERS
		# Authentication
		if request.security_web:
			aio_request.auth = aiohttp.BasicAuth(request.auth_user, request.auth_pass)
		# Redirects
		aio_request.max_redirects = request.redirects
		# Timeout
		if not request.timeout:
			aio_request.timeout = aiohttp.ClientTimeout(**DEFAULT_REQUEST_TIMEOUT)
		# HTTP Proxy
		if request.proxy_user and request.proxy_pass:
			try:
				if not request.proxy_headers:
					aio_request.proxy_headers = request.headers
				else:
					aio_request.proxy_headers = request.proxy_headers
				aio_request.proxy = aiohttp.BasicAuth(request.proxy_user, request.proxy_pass)
				log.debug(f'Proxy Server Enabled: address="{request.proxy_host}" port="{request.proxy_port}"')
			except aiohttp.ClientProxyConnectionError as e:
				log.error(f"failed to connect to a proxy: {e}")
			except aiohttp.ClientConnectorError as e:
				raise AsyncHTTPClientProxyException(e)

		# Certificates / SSL
		if request.verify_ssl and request.sslcontext:
			# Path of the example certificates '/path/to/ca-bundle.crt'
			aio_request.ssl = ssl.create_default_context(request.sslcontext)
		# Validate ssl
		aio_request.verify_ssl = request.verify_ssl
		# Raises exception if response status is> = 400.
		aio_request.raise_for_status = request.raise_for_status
		# Cliente async session!
		async with ClientSession().connect() as client:
			# HTTP Method
			if request.method == 'GET':
				request_callback = client.get
			elif request.method == 'POST':
				request_callback = client.post
			elif request.method == 'PUT':
				request_callback = client.put
			elif request.method == 'HEAD':
				request_callback = client.head
			else:
				raise AsyncHTTPUnsupportedMethodException("Unsupported request method")
			# Request Callback
			async with request_callback(**vars(aio_request)) as assync_resp:
				try:
					contents_buffer = await self.auto_decode(assync_resp.text)
				except TypeError:
					contents_buffer = None

				try:
					# Response Object
					response = AssyncHTTPResponse(
						request=request,
						content_text=contents_buffer,
						version=assync_resp.version,
						status=assync_resp.status,
						reason=assync_resp.reason,
						method=assync_resp.method,
						url=assync_resp.url,
						real_url=assync_resp.real_url,
						connection=assync_resp.connection,
						content=assync_resp.content,
						cookies=assync_resp.cookies,
						headers=assync_resp.headers,
						raw_headers=assync_resp.raw_headers,
						links=assync_resp.links,
						content_type=assync_resp.content_type,
						charset=assync_resp.charset,
						history=assync_resp.history,
						request_info=assync_resp.request_info,
						release=await assync_resp.release())
				except aiohttp.ServerTimeoutError as e:
					raise AsyncHTTPTimeoutException(f"Confirmation time exceeded : {e}")

				except aiohttp.ClientOSError as e:
					raise AsyncHTTPCertificateException(f"Untrusted SSL certificate error : {e}")

				except aiohttp.ClientError as e:
					raise AsyncHTTPClientError(f"Unexpected error while making request: {e}")

				log.debug(f'HTTP Server Response: {response}')
				return response
		log.debug("Async request failed...")
		raise AsyncHTTPClientError(f"Unexpected error while making request: {e}")

	def get(self, url, **kwargs):
		kwargs.update({"url": url, "method": "GET"})
		return self.prepare_request(**kwargs)

	def post(self, url, **kwargs):
		kwargs.update({"url": url, "method": "POST"})
		return self.prepare_request(**kwargs)

	def head(self, url, **kwargs):
		kwargs.update({"url": url, "method": "HEAD"})
		return self.prepare_request(**kwargs)

	def get_loop(self):
		return asyncio.get_event_loop()

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop()
		raise AsyncLoopException('Finishing event-loop..')

	async def fetch(self, **kwargs):
		return await self.send_request(**kwargs)

	def prepare_request(self, **kwargs):
		self.loop = self.get_loop()
		return self.loop.run_until_complete(self.fetch(**kwargs))

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		if exc_val:
			log.warning(f'exc_type: {exc_type}')
			log.warning(f'exc_value: {exc_val}')
			log.warning(f'exc_traceback: {exc_tb}')
	
	def __dell__(self):
		del self



class HTTPBoost():
	"""
		Classe responsável por realizar solicitações simulataneas.
		Receber uma lista de objetos e manda brasa com thread pool
	"""
	def __init__(self, concurrent_requests, max_queue_size=0, concurrent_blocks=None, **kwargs): 

		self.max_queue_size      = max_queue_size
		self.concurrent_requests = concurrent_requests
		self.queue_block         = Queue(maxsize=self.max_queue_size)
		self.queue_result        = Queue(maxsize=self.max_queue_size)
		self.out_queue           = Queue(maxsize=self.max_queue_size)
		self.concurrent_blocks   = concurrent_blocks
		self.fake_block_size     = CONCURRENT_BLOCKS
		self.loop                = None        # AJUSTAR
		self.urls                = []          # AJUSTAR
		self.kwargs = kwargs                   # AJUSTAR




	def recover_block(self, bl):

		for c, url in enumerate(self.urls, bl):
			try:
				self.kwargs['url'] = url + f'&count={c}'
				request  = HTTPClient()
				future   = asyncio.ensure_future(request.fetch(**self.kwargs), loop=self.loop)
				self.queue_block.put(future)

			except Exception as exc:
				try:
					code = exc.code
				except AttributeError:
					code = ''
					raised_exc = FailedAIO(code=code, message=exc, url=url, raised=exc.__class__.__name__)
				else:
					raised_exc = None
					print("Erro inesperado {}".format(exc))
					break

	async def rnd_sleep(self, t):
		# sleep for T seconds on average
		await asyncio.sleep(t * 1 * 2)

	def quick_response(self):
		try:
			self.loop = self.get_event_loop()
			#asyncio.set_event_loop(self.loop)
			#self.loop.set_debug(True)

			finished, pendings = self.loop.run_until_complete(
				asyncio.wait(self.queue_block.queue,
							 return_when=asyncio.FIRST_COMPLETED))

			#for f in finished:
			#	#result = f.result()
			#	#ime.sleep(0.1)
			self.finished = len(finished) + len(pendings)
			#	self.queue_result.put(result)
			#	#self.queue_result.put(f.result())

			#print(finished)

			'''
			while not self.queue_block.empty():
				#while True:
				try:

					task = self.queue_block.get(block=True)


					self.queue_block.task_done()

					if not task.cancelled():
						self.queue_result.put(task.result())

				except Exception as e:
					try:

						self.loop.run_until_complete(self.loop.shutdown_asyncgens())
					finally:
						task.done()
						self.out_queue.put(task)
					continue

             '''
		except Exception as err:
			print("Erro inesperado :{} finalizando lopp shutdown_event_loop".format(err))
			if not self.loop.is_closed():
				self.shutdown_event_loop()
        

	def run(self):
		data = self.kwargs['url']

		if self.urls:
			pass

		bl = 1
		start = time.time()
		for nb in range(self.fake_block_size):
			self.urls = [data for _ in range(self.concurrent_requests)]
			self.recover_block(bl)
			bl = bl + len(self.urls)
			self.quick_response()

		#await self.queue_block.join()

		end = time.time()

		print("Processamento finalizado.")
		print("Tempo de processamento             : ", round((end - start),4),"s")
		print("Numero requisições simultaneas     : ", self.concurrent_requests)
		print("Numero de blocos                   : ", self.fake_block_size)
		print("Tamanho da fila                    : " ,self.max_queue_size)
		print("Numero de conexões api(japronto)   : ", 200)
		print("Numero de requisições de sucesso   : ", self.finished)
		print("Número de requisições que falharam : ", self.out_queue.qsize())


	def get_event_loop(self):
		return asyncio.get_event_loop()

	def shutdown_event_loop(self):
		if self.loop.is_running():
			self.loop.close()
			return
		#raise Exception('Encerramento do loop falhou.')



def main():
	# Teste unitario
	#request = HTTPClient()
	#response = request.get('http://127.0.0.1:8000/api/?method=foobar.get&format=json')
	#response = request.get('https://internacional.com.br/')
	#print(response)
	
	#print(response)

	# Teste assincrono
	assincrone_res = HTTPBoost(url='http://127.0.0.1:8000/api/?method=xpto.get&format=json', method='get', concurrent_requests=10)
	#assincrone_res = HTTPBoost(url='https://internacional.com.br/', method='get',concurrent_requests=150)
	assincrone_res.run()

if __name__ == '__main__':
	main()

#end-of-file
