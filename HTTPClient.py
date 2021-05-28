"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
************************************************************************
"""
import io
import ssl
import json
import time
import random
import logging
import asyncio
import aiohttp
import settings
from utils import Structure
from dataclasses import field
from types import SimpleNamespace
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse
from aiohttp.helpers import BasicAuth
from aiohttp import HttpVersion10
from aiohttp import HttpVersion11
from exceptions import FailedAIO
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

log = logging.getLogger('HTTPClient')

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
		with aiohttp.Timeout(self.timeout):
			return self.connect().close()

	async def __aiter__(self):
		with aiohttp.Timeout(self.timeout):
			return self

	async def __await__(self):
		return self.connect().__await()


class AsyncHTTPResponse(Structure):
	"""
		Data class responsible for encapsulating responses from HTTP requests.
		ClientResponse supports asynchronous context manager protocol.
	"""
	def __str__(self):
		self.summary = SimpleNamespace(**{k:v for k,v in self.__dict__.items() if k not in ['content_text']})
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
	headers           : dict = field(default=None) 
	timeout           : int = field(default=120)
	postdata          : bytes = field(default=None, repr=False)
	http_version      : str = field(default='HTTP/1.1')
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

	def __str__(self):
		return f'HTTP-Request(domain="{self.domain}", ' \
			   f'method="{self.method}")'


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

			aio_request.headers = settings.DEFAULT_REQUEST_HEADERS
		else:
			request.headers = settings.DEFAULT_REQUEST_HEADERS
		# Authentication
		if request.security_web:
			aio_request.auth = aiohttp.BasicAuth(request.auth_user, request.auth_pass)
		# Redirects
		aio_request.max_redirects = request.redirects
		# Timeout
		if not request.timeout:
			aio_request.timeout = aiohttp.ClientTimeout(**settings.DEFAULT_REQUEST_TIMEOUT)
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
				raise AsyncHTTPUnsupportedMethodException(
					"Unsupported request method"
				)
			# Request Callback
			async with request_callback(**vars(aio_request)) as async_resp:
				try:
					contents_buffer = await self.auto_decode(async_resp.text)
				except TypeError:
					contents_buffer = None
				try:
					# Response Object
					response = AsyncHTTPResponse(
						request=request,
						content_text=contents_buffer,
						version=async_resp.version,
						status=async_resp.status,
						reason=async_resp.reason,
						method=async_resp.method,
						url=async_resp.url,
						real_url=async_resp.real_url,
						connection=async_resp.connection,
						content=async_resp.content,
						cookies=async_resp.cookies,
						headers=async_resp.headers,
						raw_headers=async_resp.raw_headers,
						links=async_resp.links,
						content_type=async_resp.content_type,
						charset=async_resp.charset,
						history=async_resp.history,
						request_info=async_resp.request_info,
						release=await async_resp.release())
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
		return self.dispatch(**kwargs)

	def post(self, url, **kwargs):
		kwargs.update({"url": url, "method": "POST"})
		return self.dispatch(**kwargs)

	def head(self, url, **kwargs):
		kwargs.update({"url": url, "method": "HEAD"})
		return self.dispatch(**kwargs)

	def get_loop(self):
		return asyncio.get_event_loop()

	async def fetch(self, **kwargs):
		try:
			return await self.send_request(**kwargs)
		except aiohttp.client_exceptions.ClientConnectorError as exc:
			log.debug(f"connection {exc.host}:{exc.port} - {exc.os_error}")

	def dispatch(self, **kwargs):
		self.loop = self.get_loop()
		return self.loop.run_until_complete(self.fetch(**kwargs))

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop()
		raise AsyncLoopException('Finishing event-loop..')

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		if exc_val:
			log.warning(f'exc_type: {exc_type}')
			log.warning(f'exc_value: {exc_val}')
			log.warning(f'exc_traceback: {exc_tb}')

	def __dell__(self):
		del self

# end-of-file