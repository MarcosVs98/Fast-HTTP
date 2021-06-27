"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import ssl
import time
import queue
import timeit
import logging
import asyncio
import aiohttp
import fasthttp.utils
import fasthttp.settings
from uuid import uuid4
from dataclasses import field
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse
from fasthttp.utils import get_tls_info
from fasthttp.utils import Structure
from fasthttp.HTTPClient import AsyncHTTPClient
from fasthttp.HTTPClient import AsyncHTTPRequest
from fasthttp.HTTPClient import AsyncSession
from fasthttp.exceptions import AsyncLoopException
from fasthttp.exceptions import AsyncHTTPConnectionException
from fasthttp.exceptions import AsyncHTTPClientProxyException
from fasthttp.exceptions import BenchmarkingFailed

log = logging.getLogger('http-benchmark')


@dataclass
class BlockResponse(Structure):
	"""
	Data class responsible for encapsulating
	block response.
	"""
	ssid   : str = field(default=uuid4())
	block  : tuple = field(default=())

	def __str__(self):
		return f'<BlockResponse(sid={self.ssid})>'


@dataclass
class BenchmarkResponse(Structure):
	"""
	Data class responsible for encapsulating
	all benchmark results.
	"""
	success       : int = field(default=0)
	failed        : int = field(default=0)
	total_time    : int = field(default=0)
	blocks        : tuple = field(default=())

	def __str__(self):
		return f'<FastHTTP-Benchmark[success={self.success}, ' \
			   f'total_time={round(self.total_time, 3)}]>'


class HTTPBenchmark():
	"""
	*****************************************************************
	class responsible for performing the AsyncHTTPClient benchmark
	*****************************************************************
	*                       ┬────┬────┬───┬                         *
	*                       |    |    |   |                         *
	*                       |    QUEUE    |                         *
	*                       |    |    |   |                         *
	*                       └────└────└───┘                         *
	*                              ||                               *
	*                       ┬──────┘└───────┬                       *
	*                       | Request Block |                       *
	*                       └───────┬───────┘                       *
	*                               |                               *
	*      ┬────────────────────────└────────────────────────┬      *
	*      |        ┬───────────────┬───────────────┬        |      *
	*      |   ┬────└────┬     ┬────└────┬     ┬────└────┬   |      *
	*      |   |    |    |     |    |    |     |    |    |   |      *
	*      |   v    v    v     v    v    v     v    v    v   |      *
	*      |   ┬─────────┬     ┬─────────┬     ┬─────────┬   |      *
	*      |   | #target |     | #target |     | #target |   |      *
	*      |   └─────────┘     └─────────┘     └─────────┘   |      *
	*      |   |    |    |     |    |    |     |    |    |   |      *
	*      |   v    v    v     v    v    v     v    v    v   |      *
	*      |   ┬─────────┬     ┬─────────┬     ┬─────────┬   |      *
	*      |   |#Response|     |#Response|     |#Response|   |      *
	*      |   └─────────┘     └─────────┘     └─────────┘   |      *
	*      |   |    |    |     |    |    |     |    |    |   |      *
	*      |   v    v    v     v    v    v     v    v    v   |      *
	*      └───────────────────────┬┬────────────────────────┘      *
	*                              ||                               *
	*                    ┬─────────┘└──────────┬                    *
	*                    |    Response block   |                    *
	*                    └─────────────────────┘                    *
	*****************************************************************
	params>
	*****************************************************************
	"""
	def __init__(self, concurrent_blocks, concurrent_requests, request=None, session=None, **kwargs):

		if not isinstance(request, AsyncHTTPRequest):
			self._request = AsyncHTTPRequest(**kwargs)
		else:
			self._request = request
		if not isinstance(session, AsyncSession):
			self._session = AsyncSession()
		else:
			self._session = session
		self._uri = urlparse(self._request.url)
		self._asynchronous_requests = concurrent_requests
		self._asynchronous_blocks = concurrent_blocks
		self._max_queue_size = int(concurrent_blocks * concurrent_requests)
		self._response_block = queue.Queue(maxsize=self._max_queue_size)
		self._loop = None
		self._unfinished = [1]
		self._http_status = {}
		self.blocks = 0

	def _all_http_status(self, finisheds):
		"""
		method responsible for assembling a request histogram inserting a
		time to validate how many successful requests in a period of time..
		"""
		for f in finisheds:
			try:
				response = f.result()
				if response.status in fasthttp.settings.HTTP_HTTP_SUCESS:
					if not min(fasthttp.settings.HTTP_HTTP_SUCESS) in self._http_status:
						self._http_status[min(fasthttp.settings.HTTP_HTTP_SUCESS)] = 0
					self._http_status[min(fasthttp.settings.HTTP_HTTP_SUCESS)] += 1
				elif response.status in fasthttp.settings.HTTP_REDIRECTION:
					if not min(fasthttp.settings.HTTP_REDIRECTION) in self._http_status:
						self._http_status[min(fasthttp.settings.HTTP_REDIRECTION)] = 0
					self._http_status[min(fasthttp.settings.HTTP_REDIRECTION)] += 1
				elif response.status in fasthttp.settings.HTTP_CLIENT_ERROR:
					if not min(fasthttp.settings.HTTP_CLIENT_ERROR) in self._http_status:
						self._http_status[min(fasthttp.settings.HTTP_CLIENT_ERROR)] = 0
					self._http_status[min(fasthttp.settings.HTTP_CLIENT_ERROR)] += 1
				elif response.status in fasthttp.settings.HTTP_SERVER_ERROR:
					if not min(fasthttp.settings.HTTP_SERVER_ERROR) in self._http_status:
						self._http_status[min(fasthttp.settings.HTTP_SERVER_ERROR)] = 0
					self._http_status[min(fasthttp.settings.HTTP_SERVER_ERROR)] += 1
				else:
					if not response.status in self._http_status:
						self._http_status[response.status] = 0
					self._http_status[response.status] += 1
			except AttributeError:
				if not fasthttp.settings.HTTP_CLIENT_DEFAULT_ERROR in self._http_status:
					self._http_status[fasthttp.settings.HTTP_CLIENT_DEFAULT_ERROR] = 0
				self._http_status[fasthttp.settings.HTTP_CLIENT_DEFAULT_ERROR] += 1
		return {k: v for k, v in sorted(self._http_status.items(),
				key=lambda item: item[1], reverse=True)}

	def get_block_requests(self):

		request_block = queue.Queue(maxsize=self._asynchronous_requests)

		for n in range(0, self._asynchronous_requests):
			try:
				async_request = AsyncHTTPClient()
				future = asyncio.ensure_future(async_request.fetch(request=self._request), loop=self._loop)
				request_block.put(future)
			except asyncio.InvalidStateError as exc:
				log.error(f"Invalid internal state of {future}. bl={n} exc={exc}")
			except asyncio.CancelledError as exc:
				log.error(f"The operation has been cancelled. bl={n} exc={exc}")
			except asyncio.TimeoutError as exc:
				log.error(f"The operation has exceeded the given deadline,  bl={n} exc={exc}")
		return request_block

	def perform(self, debug_stats=False):
		t0 = timeit.default_timer()
		for n in range(1, self._asynchronous_blocks + 1):
			try:
				request_block = self.get_block_requests()
				self.blocks = n + self._asynchronous_requests
				log.debug(f'processed block=(r={n * self._asynchronous_requests}, b={n})')
			except AsyncHTTPConnectionException as exc:
				log.error(f"Unexpected error when blocking requests {exc}")
			except (BrokenPipeError, ConnectionAbortedError) as exc:
				log.warning('Error writing to a closed socket')
			except (ConnectionRefusedError, ConnectionError) as exc:
				log.warning('Error trying to connect to the client')
			try:
				# perform!
				while self._unfinished:
					# get new event loop!
					self._loop = asyncio.get_event_loop()
					asyncio.set_event_loop(self._loop)
					try:
						finished, self._unfinished = self._loop.run_until_complete(
							asyncio.wait(request_block.queue,
								return_when=asyncio.FIRST_COMPLETED, timeout=30))
					except aiohttp.client_exceptions.ClientConnectorError as e:
						log.error(e)
					finally:
						self.shutdown_event_loop()
				# block finished!
				self._all_http_status(finished)
				self._response_block.put(finished)
				self._unfinished = True

			except AsyncLoopException as exc:
				log.error(f"Unexpected error: {exc} terminating lopp shutdown_event_loop")
				if not self._loop.is_closed():
					self.shutdown_event_loop()
		tf = timeit.default_timer()
		# Calc time of benchmarking
		self.benchmark_time = round((tf - t0), 5)
		# finished all requests!
		# Show results
		if debug_stats:
			self.print_stats()

	def get_responses(self):
		if not self._response_block.empty():
			return BenchmarkResponse(
				success=self._http_status.get(200, 0),
				failed=sum(self._http_status.values()) - self._http_status.get(200, 0),
				total_time=self.benchmark_time,
				blocks=(BlockResponse(ssid=f"{n}-{uuid4()}", block=(response.result() for response in responses))
				      for n, responses in enumerate(self._response_block.queue, 1)))
		raise BenchmarkingFailed("No response objects were generated...")

	def print_stats(self):
		responses = self._response_block.get()
		for s in list(responses):
			try:
				response = s.result()
				if isinstance(response, tuple):
					connection_key, error = response
					return print(error)
				if response.content_length > 0:
					sample = response
					break
			except AttributeError as e:
				continue

		tls_info = get_tls_info(self._request.url)
		server = sample.headers.get('server', 'Unknown')
		nrequests = self._asynchronous_blocks * self._asynchronous_requests
		info =  f'{fasthttp.utils.INFO.title} Version {fasthttp.utils.INFO.version} - {fasthttp.utils.INFO.copyright}\n'
		info += f'Benchmarking {self._request.url}\n\n'
		info += f'{nrequests} requests divided into {self._asynchronous_blocks} '
		info += f'blocks with {self._asynchronous_requests} simultaneous requests.\n'
		print(info)

		document_size = fasthttp.utils.humanbytes(sample.content_length)
		info =  f"* host: {self._uri.hostname} "
		info += f"| port: {self._uri.port} \n" if self._uri.port else "\n"
		info += f"* server: {server} \n"
		info += f"* method: {self._request.method.upper()} \n"
		info += f"* scheme : {self._uri.scheme.upper()} \n"
		info += f"* SSL/TLS : {tls_info.tls_version} \n"
		info += f"* chipers {tls_info.tls_protocol}\n"
		info += f"* name server TLS: {self._uri.hostname} \n"
		info += f"* path: {self._uri.path} \n"
		info += f"* document size: {document_size}'s\n\n"

		completed_request = self._http_status.get(200, 0)
		content_buffer  = fasthttp.utils.humanbytes(
			sample.content_length * completed_request)
		failed_requests = sum(self._http_status.values()) - completed_request

		info += f"* TCP connections: {self._session.connector.limit} \n"
		info += f"* máx. requests per hostname: {self._session.connector.limit_per_host} \n"
		info += f"* TTL dns cache: {self._session.connector.ttl_dns_cache} \n"
		info += f"* concurrent requests: {self._asynchronous_requests} \n"
		info += f"* qtd. request block: {self._asynchronous_blocks} \n\n"
		try:
			rps = round(self.benchmark_time / completed_request , 7)
		except ZeroDivisionError:
			rps = 0
		try:
			avg = round(1.0 / rps)
		except ZeroDivisionError:
			avg = 0
		info += f"* total requests: {self._asynchronous_blocks * self._asynchronous_requests} \n"
		info += f"* benchmark time: {self.benchmark_time} seconds\n"
		info += f"* success requests: {completed_request}\n"
		info += f"* failed requests: {failed_requests}\n"
		info += f"* total buffer size: {content_buffer}'s \n"
		info += f"* average requests per second: {avg} / sec (average)\n"
		info += f"* time per request: {rps} [ms] (average on all simultaneous requests)\n"
		print(info)

	def shutdown_event_loop(self):
		if self._loop.is_running():
			self._loop.close()

	def __enter__(self):
		self.perform()
		return self.get_responses()

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_val:
			log.warning(f'exc_type: {exc_type}')
			log.warning(f'exc_value: {exc_val}')
			log.warning(f'exc_traceback: {exc_tb}')
		self.shutdown_event_loop()

	def __repr__(self):
		return f'<FastHTTP-Benchmark (max_size={self._max_queue_size})>'


# end-of-file