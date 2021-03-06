"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
************************************************************************
"""
import ssl
import json
import time
import socket
import random
import logging
import asyncio
import aiohttp
import fasthttp.settings
from dataclasses import field
from types import SimpleNamespace
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse, urlunparse
from aiohttp.helpers import BasicAuth
from aiohttp import HttpVersion10
from aiohttp import HttpVersion11
from fasthttp.utils import Structure
from fasthttp.exceptions import AsyncHTTPClientException
from fasthttp.exceptions import AsyncHTTPClientResolveHostException
from fasthttp.exceptions import AsyncHTTPUnsupportedMethodException
from fasthttp.exceptions import AsyncLoopException
from fasthttp.exceptions import AsyncHTTPTimeoutException
from fasthttp.exceptions import AsyncHTTPCertificateException
from fasthttp.exceptions import AsyncHTTPClientProxyException
from fasthttp.exceptions import AsyncHTTPClientError

log = logging.getLogger('AsyncHTTPClient')


@dataclass
class AsyncTCPConnector(Structure):
	"""
	https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp-client-reference-connectors
	"""
	ssl                   : bool = field(default=fasthttp.settings.VERIFY_SSL)
	fingerprint           : bytes = field(default=None, repr=False) 
	use_dns_cache         : bool = field(default=fasthttp.settings.USE_DNS_CACHE)
	ttl_dns_cache         : int = field(default=fasthttp.settings.TTL_DNS_CACHE)
	family                : int = field(default=socket.AF_INET)
	ssl_context           : str = field(default=None)
	local_addr            : tuple = field(default=None)
	resolver              : aiohttp.AsyncResolver = field(default=None)
	force_close           : bool = field(default=False)
	limit                 : int = field(default=fasthttp.settings.LIMIT_CONNECTIONS)
	limit_per_host        : int = field(default=fasthttp.settings.LIMIT_REQUESTS_PER_HOST)
	enable_cleanup_closed : bool = field(default=False)
	loop                  : str = field(default=None)

	def __call__(self, *args, **kwargs):
		try:
			return aiohttp.TCPConnector(**self.__dict__)
		except aiohttp.ClientConnectorError as e:
			log.error(e)


@dataclass
class AsyncSession(Structure):
	"""
	Class responsible for setting up an interface for making HTTP requests.
	The session encapsulates a set of connections supporting keepalives by default.
	"""
	connector            : aiohttp.BaseConnector = field(default=AsyncTCPConnector())
	loop                 : str = field(default=None)
	cookies              : dict = field(default=None)
	headers              : dict = field(default=None)
	skip_auto_headers    : str = field(default=None)
	auth                 : aiohttp.BasicAuth = field(default=None)
	version              : aiohttp.HttpVersion = field(default=None)
	json_serialize       : dict = field(default=json.dumps)
	cookie_jar           : aiohttp.DummyCookieJar = field(default=None)
	conn_timeout         : float = field(default=None)
	raise_for_status     : bool = field(default=False)
	connector_owner      : bool = field(default=True)
	auto_decompress      : bool = field(default=True)
	read_bufsize         : int = field(default=2 ** 16)
	requote_redirect_url : bool = field(default=False)
	trust_env            : bool = field(default=False)
	trace_configs        : bool = field(default=None)

	@property
	def connection(self):
		self.connector = self.connector()
		return aiohttp.ClientSession(**self.__dict__)

	async def __aenter__(self):
		return self.connect

	async def __aexit__(self, exc_type, exc, tb):
		with aiohttp.Timeout(self.timeout):
			return self.connection.close()

	async def __aiter__(self):
		with aiohttp.Timeout(self.timeout):
			return self

	async def __await__(self):
		return self.connection.__await()


class AsyncHTTPResponse(Structure):
	"""
		Data class responsible for encapsulating responses from HTTP requests.
		ClientResponse supports asynchronous context manager protocol.
	"""
	def __str__(self):
		self.summary = SimpleNamespace(**{ k:v for k,v in self.__dict__.items() if k != 'content_text'})
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
class AsyncRequestTimeout(Structure):
	"""
	Data class responsible for representing
	the fields of an aiohttp.Timeout
	"""
	total        : float = field(default=fasthttp.settings.AUTOTHROTTLE_MAX_DELAY)
	connect      : float = field(default=fasthttp.settings.AUTOTHROTTLE_START_DELAY)
	sock_connect : float = field(default=fasthttp.settings.AUTOTHROTTLE_SOCK_DELAY)
	sock_read    : float = field(default=fasthttp.settings.AUTOTHROTTLE_SOCK_DELAY)


@dataclass
class AsyncHTTPRequest(Structure):
	"""
	Data class responsible for representing
	the fields of an HTTP request.
	"""
	url               : str 
	method            : str
	header            : dict = field(default=None)
	timeout           : int = field(default=AsyncRequestTimeout)
	security_web      : bool = field(default=False)
	postdata          : bytes = field(default=None, repr=False)
	http_version      : str = field(default='HTTP/1.1')
	auth_user         : str = field(default=None)
	auth_pass         : str = field(default=None)
	allow_redirects   : bool = field(default=True)
	redirects         : int = field(default=30)
	proxy             : str = field(default=None)
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
		elif name == 'proxy':
			proxy_uri = urlparse(value)
			self.__dict__['scheme'] = proxy_uri.scheme
			self.__dict__['proxy_host'] = proxy_uri.hostname
			self.__dict__['proxy_port'] = proxy_uri.port
		self.__dict__[name] = value

	def __str__(self):
		return f'HTTP-Request(domain="{self.domain}", ' \
			   f'method="{self.method}")'


class AsyncHTTPClient():
	"""
	Class responsible for executing asynchronous HTTP requests
	and return response objects.
	"""
	def __init__(self):
		self._loop = None

	async def auto_decode(self, content):
		for enc in ['ascii', 'utf8', 'iso-8859-1', 'cp-1252']:
			try:
				return enc, await content(enc)
			except UnicodeDecodeError:
				pass

	async def _open_socket_callback(self, args):
		purpose, family, socktype, proto, raddr, laddr = args
		s = socket.socket(family, socktype, proto)
		try:
			if ((laddr is not None) and (family == socket.AF_INET)):
				s.bind(laddr)
		except (OSError, AsyncHTTPClientResolveHostException) as e:
			log.debug(f"Cannot bind local address '{laddr}' to socket '{s}': {e}")
		s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		log.debug(f'Open Socket: {s}')
		return await s

	async def send_request(self, request=None, session=None, **kwargs):
		"""
		method responsible for handling an HTTP request.
		"""
		if request is None:
			request = AsyncHTTPRequest(**kwargs)

		log.debug(f'HTTP Client Request: {request}')
		# AIO Request
		async_request = SimpleNamespace()

		# Initialize Async Session
		if isinstance(session, AsyncSession):
			async_session = session
		else:
			async_session = AsyncSession()
		# URL
		uri = urlparse(request.url)
		# validate if it is a valid url
		if not all((uri.scheme, uri.netloc, uri.path)):
			raise aiohttp.InvalidURL(
			   "URL used for fetching is malformed, e.g. it does not contain host part")
		async_request.url = uri.geturl()

		# Request Headers
		if request.header is not None:
			if not isinstance(request.header, (list, tuple, dict)):
				raise AsyncHTTPClientException(f'Invalid request headers')
			if not all(isinstance(i, (list, tuple, str)) for i in request.header):
				raise AsyncHTTPClientException(f'Invalid request headers')
			if not all(len(i) == 2 for i in request.header.items()):
				raise AsyncHTTPClientException(f'Invalid request headers')
			rawheaders = [f'{k}: {v}' for k, v in request.header.items()]

			async_request.headers = fasthttp.settings.DEFAULT_REQUEST_HEADERS
		else:
			request.headers = fasthttp.settings.DEFAULT_REQUEST_HEADERS
		# Authentication
		if request.security_web:
			async_request.auth = aiohttp.BasicAuth(request.auth_user, request.auth_pass)
		# Redirects
		async_request.max_redirects = request.redirects
		# Timeout
		if not request.timeout:
			async_request.timeout = aiohttp.ClientTimeout(**request.timeout())
		# HTTP Proxy
		if request.proxy:
			try:
				if not request.proxy_headers:
					async_request.proxy_headers = request.headers
				else:
					async_request.proxy_headers = request.proxy_headers
				if request.proxy_user and request.proxy_pass:
					async_request.proxy_auth = aiohttp.BasicAuth(request.proxy_user, request.proxy_pass)
				async_request.proxy = request.proxy
				log.debug(f'Proxy Server Enabled: address="{request.proxy_host}" port="{request.proxy_port}"')
			except aiohttp.ClientProxyConnectionError as e:
				log.error(f"failed to connect to a proxy: {e}")
			except aiohttp.ClientConnectorError as e:
				raise AsyncHTTPClientProxyException(e)

		# HTTP Protocol Version
		if request.http_version == 'HTTP/1.0':
			async_session.version = aiohttp.HttpVersion10
		elif request.http_version == 'HTTP/1.1':
			async_session.version = aiohttp.HttpVersion10
		else:
			raise AsyncHTTPClientException(f'Unsuported HTTP Protocol Version: "{request.http_version}"')

		# Certificates / SSL
		if request.verify_ssl and request.sslcontext:
			# Path of the example certificates '/path/to/ca-bundle.crt'
			async_request.ssl = ssl.create_default_context(request.sslcontext)
		# Validate ssl
		async_request.verify_ssl = request.verify_ssl
		# Raises exception if response status is> = 400.
		async_request.raise_for_status = request.raise_for_status

		# Cliente async session!
		async with AsyncSession(**vars(async_session)).connection as client:
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
			t0 = time.time()

			# Request Callback
			async with request_callback(**vars(async_request)) as async_response:
				try:
					encoding, contents_text = await self.auto_decode(async_response.text)
				except TypeError:
					contents_text = None
					encoding = None
				try:
					# Response Object
					response = AsyncHTTPResponse(
						request=request,
						content_text=contents_text,
						version=async_response.version,
						status=async_response.status,
						reason=async_response.reason,
						method=async_response.method,
						url=async_response.url,
						real_url=async_response.real_url,
						connection=async_response.connection,
						elapsed=round(time.time() - t0, 3),
						content=async_response.content,
						content_length=len(contents_text),
						encoding=encoding,
						cookies=async_response.cookies,
						headers=async_response.headers,
						raw_headers=async_response.raw_headers,
						links=async_response.links,
						content_type=async_response.content_type,
						charset=async_response.charset,
						history=async_response.history,
						request_info=async_response.request_info,
						release=await async_response.release())
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

	async def fetch(self, **kwargs):
		try:
			return await self.send_request(**kwargs)
		except aiohttp.ClientError as exc:
			log.debug(f"connection error {exc.host}:{exc.port} - {exc.os_error}")
			return  (exc._conn_key, exc._os_error)
		
	def dispatch(self, **kwargs):
		self.loop = asyncio.get_event_loop()
		return self.loop.run_until_complete(self.fetch(**kwargs))

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop.close()
		raise AsyncLoopException('finishing event-loop..')

	async def __aenter__(self, **kwargs):
		return await self.fetch(**kwargs)

	async def __aexit__(self, typ, value, tb):
		if exc_val:
			log.warning(f'exc_type: {exc_type}')
			log.warning(f'exc_value: {exc_val}')
			log.warning(f'exc_traceback: {exc_tb}')
		self.close_loop()

	def __dell__(self):
		del self

# end-of-file
