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
import settings
from dataclasses import dataclass
from dataclasses import field
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

	def _get_http_result(self):
		"""
		Método responsável por montar um histograma de solicitações
		inserir um time para validar quantas solicitações sucesso em
		um periodo de tempo.
		
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
				none_status = 000
				if not none_status in self.retult:
					self.retult[none_status] = 0
				self.retult[none_status] += 1
		result = {k: v for k, v in sorted(self.retult.items(),
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

	def _perform(self):
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
			self.start = time.time()
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
			self.end = time.time()
		except AsyncLoopException as exc:
			log.error(f"Unexpected error: {exc} terminating lopp shutdown_event_loop")
			if not self._loop.is_closed():
				self.shutdown_event_loop()

	def run(self):
		self._perform()
		self._get_http_result()
		print(self.retult)

		print("Processamento finalizado.\n",
			  "Tempo de processamento             : ", round((self.end - self.start), 4), "s\n",
			  "Numero requisições simultaneas     : ", self._concurrent_requests, "\n",
			  "Numero de blocos                   : ", self._concurrent_blocks, "\n",
			  "Tamanho da fila                    : ", self._max_queue_size, "\n",
			  "Numero de requisições de sucesso   : ", self._concurrent_blocks * self._concurrent_requests, "\n", #self.rees[200], "\n",
			  "Número de requisições que falharam : ", self._out_queue.qsize(), "\n", end="\n")

	def shutdown_event_loop(self):
		if self._loop.is_running():
			self._loop.close()

# end-of-file                                          '