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
import utils
import logging
import asyncio
import aiohttp
import settings
from dataclasses import dataclass
from dataclasses import field
from urllib.parse import urlencode, urlparse, urlunparse
from exceptions import AsyncLoopException
from exceptions import AsyncHTTPConnectionException
from exceptions import AsyncHTTPClientProxyException
from HTTPClient import HTTPClient

log = logging.getLogger('http-booster')

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
	def __init__(self, url, concurrent_requests, max_queue_size=0, concurrent_blocks=None, **kwargs):
		self._url = url
		self._uri = urlparse(url)
		self.b = 0
		self._max_queue_size = max_queue_size
		self._concurrent_requests = concurrent_requests
		self._concurrent_blocks = concurrent_blocks
		self._queue_block = queue.Queue(maxsize=self._max_queue_size)
		self._queue_result = queue.Queue(maxsize=self._max_queue_size)
		self._out_queue = queue.Queue(maxsize=self._max_queue_size)
		self._loop = None
		self.unfinished = [1]
		self.kwargs = kwargs
		self._finished = 0
		self.retult = {}

	def _all_http_status(self):
		"""
		Método responsável por montar um histograma de solicitações inserir um
		time para validar quantas solicitações sucesso em um periodo de tempo.
		"""
		for f in self.finished:
			try:
				response = f.result()
				if response.status in settings.HTTP_HTTP_SUCESS:
					if not min(settings.HTTP_HTTP_SUCESS) in self.retult:
						self.retult[min(settings.HTTP_HTTP_SUCESS)] = 0
					self.retult[min(settings.HTTP_HTTP_SUCESS)] += 1
				elif response.status in settings.HTTP_REDIRECTION:
					if not min(settings.HTTP_REDIRECTION) in self.retult:
						self.retult[min(settings.HTTP_REDIRECTION)] = 0
					self.retult[min(settings.HTTP_REDIRECTION)] += 1
				elif response.status in settings.HTTP_CLIENT_ERROR:
					if not min(settings.HTTP_CLIENT_ERROR) in self.retult:
						self.retult[min(settings.HTTP_CLIENT_ERROR)] = 0
					self.retult[min(settings.HTTP_CLIENT_ERROR)] += 1
				elif response.status in settings.HTTP_SERVER_ERROR:
					if not min(settings.HTTP_SERVER_ERROR) in self.retult:
						self.retult[min(settings.HTTP_SERVER_ERROR)] = 0
					self.retult[min(settings.HTTP_SERVER_ERROR)] += 1
				else:
					if not response.status in self.retult:
						self.retult[response.status] = 0
					self.retult[response.status] += 1
			except AttributeError:
				if not 000 in self.retult:
					self.retult[000] = 0
				self.retult[none_status] += 1
		return {k: v for k, v in sorted(self.retult.items(),
				key=lambda item: item[1], reverse=True)}

	def get_block_requests(self):
		for n in range(self.b,  (self.b + self._concurrent_requests)):
			try:
				request = HTTPClient()
				future = asyncio.ensure_future(request.fetch(url=self._url, **self.kwargs), loop=self._loop)
				self._queue_block.put(future)
			except asyncio.InvalidStateError as exc:
				log.error(f"Invalid internal state of {future}. bl={n} exc={exc}")
			except asyncio.CancelledError as exc:
				log.error(f"The operation has been cancelled. bl={n} exc={exc}")
			except asyncio.TimeoutError as exc:
				log.error(f"The operation has exceeded the given deadline,  bl={n} exc={exc}")

	def perform(self):
		for n in range(1, self._concurrent_blocks + 1):
			try:
				self.get_block_requests()
				log.debug(f'processed block="{n}/{self._concurrent_blocks}"')
				self.b = n + self._concurrent_requests
			except AsyncHTTPConnectionException as exc:
				log.error(f"Unexpected error when blocking requests {exc}")
			except (BrokenPipeError, ConnectionAbortedError) as exc:
				log.warning('Error writing to a closed socket')
			except (ConnectionRefusedError, ConnectionError) as exc:
				log.warning('Error trying to connect to the client')
		try:
			t0 = time.time()
 			# perform!
			while self.unfinished:
				# get new event loop!
				self._loop = asyncio.get_event_loop()
				asyncio.set_event_loop(self._loop)
				try:
					self.finished, self.unfinished = self._loop.run_until_complete(
						asyncio.wait(self._queue_block.queue,
							return_when=asyncio.FIRST_COMPLETED, timeout=30))
				except aiohttp.client_exceptions.ClientConnectorError as e:
					log.error(e)
				finally:
					self.shutdown_event_loop()
			# finished!
			tf = time.time()

			self.benchmark_time = round((tf - t0), 4)
		except AsyncLoopException as exc:
			log.error(f"Unexpected error: {exc} terminating lopp shutdown_event_loop")
			if not self._loop.is_closed():
				self.shutdown_event_loop()

	def stats(self):

		total = self._concurrent_blocks * self._concurrent_requests
		info =  f'{utils.INFO.title} Version {utils.INFO.version__} - {utils.INFO.copyright}\n'
		info += f'Benchmarking {self._url}..\n'
		info += f'{total} requests divided into {self._concurrent_blocks} '
		info += f'blocks with {self._concurrent_requests} simultaneous requests.\n'
		print(info)

		self.perform()

		content_size = utils.humanbytes(0) # somente conteudo de sucesso a
		res = f"Host: {self._uri.hostname} "
		res += f"| Port: {self._uri.port} \n" if self._uri.port else "\n"
		res += f"Protocol : {self._uri.scheme.upper()} \n"
		res += f"SSL/TLS : TLSv1.1 \n"
		res += f"Chipers : ECDHE-ECDSA-CHACHA20-POLY1305, 256, 256 \n"
		res += f"Name server TLS: {self._uri.hostname} \n"
		res += f"Path: {self._uri.path} \n"
		res += f"Document Size: {content_size}"
		res += "\n\n"

		completed_request = 0
		content_buffer  = utils.humanbytes(content_size * completed_request)
		failed_requests = 0
		benchmark_time  = 0

		res += f"Concurrent requests: {self._concurrent_requests} "
	 	res += f"Benchmark time: {self.benchmark_time} seconds\n"
		res += f"Success Requests: {completed_request}\n"
		res += f"Failed Requests: {failed_requests}\n"
		res += f"Content Buffer Size: {content_buffer} Byte's"
		res += "\n\n"
		rps = 0
		avg = 0
		amp = 0
		rate = 0
		res = f"Average requests per second: {avg} / sec (average)\n"
		res += f"Time per Request: {rps} [ms] (average on all simultaneous requests)\n"
		res += f"Request blocks: {content_buffer} Byte's"
		res += f"Content Buffer Size: {content_buffer} Byte's"

		#res = f"Tempo de processamento             : ", round((self.end - self.start), 4), "s",
		#	  "\nNumero requisições simultaneas     : ", self._concurrent_requests,
		#	  "\nNumero de blocos                   : ", self._concurrent_blocks,
		#	  "\nTamanho da fila                    : ", self._max_queue_size,
		#	  "\nNumero de requisições de sucesso   : ", self.retult[200],
		#	  "\nNúmero de requisições que falharam : ", self._out_queue.qsize(), end="\n")


	def shutdown_event_loop(self):
		if self._loop.is_running():
			self._loop.close()

# end-of-file                                          '