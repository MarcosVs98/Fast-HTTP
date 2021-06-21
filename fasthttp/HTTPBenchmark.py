"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import time
import ssl
import queue
import logging
import asyncio
import aiohttp
import fasthttp.utils
import fasthttp.settings
from dataclasses import field
from dataclasses import dataclass
from fasthttp.utils import get_tls_info
from fasthttp.utils import Structure
from urllib.parse import urlencode, urlparse, urlunparse
from fasthttp.HTTPClient import AsyncHTTPClient
from fasthttp.exceptions import AsyncLoopException
from fasthttp.exceptions import AsyncHTTPConnectionException
from fasthttp.exceptions import AsyncHTTPClientProxyException
from fasthttp.exceptions import BenchmarkingFailed

log = logging.getLogger('http-benchmark')


@dataclass
class BenchmarkResponse(Structure):
	"""
	Data class responsible for encapsulating
	all benchmark results.
	"""
	success             : int = field(default=0)
	failed              : int = field(default=0)
	total_time          : int = field(default=0)
	blocks              : tuple

	def __repr__(self):
		return (f'< FastHTTP-Benchmark[success={self.success},'
		        f'total_time={round(self.total_time, 3)}]>')


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
	def __init__(self, request, concurrent_requests, max_queue_size=0, concurrent_blocks=None):
		self._request = request
		self._uri = urlparse(request.url)
		self.blocks = 0
		self._asynchronous_requests = concurrent_requests
		self._asynchronous_blocks = concurrent_blocks
		self._response_block = queue.Queue(maxsize=max_queue_size)
		self._loop = None
		self._unfinished = [1]
		self._http_status = {}

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

	def perform(self):
		t0 = time.time()
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
		tf = time.time()
		# Calc time of benchmarking
		self.benchmark_time = round((tf - t0), 5)
		# finished all requests!
		# Show results
		self.print_stats()

	def get_responses(self):
		if not self._response_block.empty():
			return BenchmarkResponse(
				success=self._http_status.get(200, 0),
				failed=sum(self._http_status.values()) - self._http_status.get(200, 0),
				total_time=self.benchmark_time,
				blocks=(responses for responses in self._response_block.get()))
			return list(self._response_block.queue)
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
		info =  f'{utils.INFO.title} Version {utils.INFO.version} - {utils.INFO.copyright}\n'
		info += f'Benchmarking {self._request.url}\n\n'
		info += f'{nrequests} requests divided into {self._asynchronous_blocks} '
		info += f'blocks with {self._asynchronous_requests} simultaneous requests.\n'
		print(info)

		document_size = utils.humanbytes(sample.content_length)
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
		content_buffer  = utils.humanbytes(
			sample.content_length * completed_request)
		failed_requests = sum(self._http_status.values()) - completed_request

		info += f"* TCP connections: {self._asynchronous_requests} \n"
		info += f"* máx. requests per IP: {self._asynchronous_requests} \n"
		info += f"* máx. requests per hostname: {self._asynchronous_requests} \n"
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
		info += f"* content buffer size: {content_buffer}'s \n"
		info += f"* average requests per second: {avg} / sec (average)\n"
		info += f"* time per request: {rps} [ms] (average on all simultaneous requests)\n"
		print(info)

	def shutdown_event_loop(self):
		if self._loop.is_running():
			self._loop.close()

# end-of-file