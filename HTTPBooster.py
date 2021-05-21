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
import random
import logging
import asyncio
import aiohttp
import settings
from aiohttp.helpers import BasicAuth
from types import SimpleNamespace
from queue import Queue
from utils import Structure
from dataclasses import dataclass
from dataclasses import field
from urllib.parse import urlencode, urlparse
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
from HTTPClient import HTTPClient


class HTTPBooster():
	"""
		Classe responsável por realizar solicitações simulataneas.
		Receber uma lista de objetos e manda brasa com thread pool
	"""

	def __init__(self, concurrent_requests, max_queue_size=0, concurrent_blocks=None, **kwargs):

		self._max_queue_size = max_queue_size
		self._concurrent_requests = concurrent_requests
		self._concurrent_blocks = concurrent_blocks
		self._queue_block = queue.Queue(maxsize=self.max_queue_size)
		self._queue_result = queue.Queue(maxsize=self.max_queue_size)
		self._out_queue = queue.Queue(maxsize=self.max_queue_size)
		self._loop = None
		self._urls = None
		self._fragment = False
		self.kwargs = kwargs

	def get_concurrent_block(self, n):

		for c, url in enumerate(self.urls, n):
			try:
				self._add_fragment(url)
				request = HTTPClient()
				future = asyncio.ensure_future(request.fetch(url=url, **self.kwargs), loop=self.loop)
				self.queue_block.put(future)

			except asyncio.InvalidStateError as exc:
				log.error(f"Invalid internal state of {future}. exc={exc}")
			except asyncio.CancelledError as exc:
				log.error(f"The operation has been cancelled. exc={exc}")
			except asyncio.TimeoutError as exc:
				log.error(f"The operation has exceeded the given deadline, exc={exc}")
			except AsyncLoopException as exc:
				log.error(f"Unexpected error when blocking requests {exc}")
				break

	async def rnd_sleep(self, t):
		# sleep for T seconds on average
		await asyncio.sleep(t * 1 * 2)

	def quick_response(self):
		try:
			self.loop = self.get_event_loop()
			# asyncio.set_event_loop(self.loop)
			# self.loop.set_debug(True)

			finished, pendings = self.loop.run_until_complete(
				asyncio.wait(self.queue_block.queue, return_when=asyncio.FIRST_COMPLETED))

			# for f in finished:
			#	result = f.result()
			# print(result)
			#	#ime.sleep(0.1)

			self.finished = len(finished) + len(pendings)
			#	self.queue_result.put(result)
			#	#self.queue_result.put(f.result())

			# print(finished)

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

	def _add_fragment(self, url):
		if self._fragment:
			if url.endswith('/'):
				url += '?'
			elif not url.endswith('?'):
				url += '&'
			url += "#count={c}".format(c=c)
		return url


	def run(self):
		bl = 1
		start = time.time()

		for nb in range(self.fake_block_size):
			self.urls = [self.kwargs['url'] for _ in range(self.concurrent_requests)]
			self.recover_block(bl)
			bl = bl + len(self.urls)
			self.quick_response()

		end = time.time()
		print("Processamento finalizado.\n",
			  "Tempo de processamento             : ", round((end - start), 4), "s\n",
			  "Numero requisições simultaneas     : ", self.concurrent_requests, "\n",
			  "Numero de blocos                   : ", self.fake_block_size, "\n",
			  "Tamanho da fila                    : ", self.max_queue_size, "\n",
			  "Numero de requisições de sucesso   : ", self.finished, "\n",
			  "Número de requisições que falharam : ", self.out_queue.qsize(), "\n", end="\n")

	def get_event_loop(self):
		return asyncio.get_event_loop()

	def shutdown_event_loop(self):
		if self.loop.is_running():
			self.loop.close()
		return


def main():
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
	url = 'https://www.internacional.com.br/associe-se'
	url = 'http://127.0.0.1:8000/api/?method=xpto.get'
	url = 'http://127.0.0.1:8000/api/?method=xpto.get'
	# url = 'https://api.myip.com/'
	assincrone_res = HTTPBooster(url=url, method='get', concurrent_requests=24)
	assincrone_res.run()


if __name__ == '__main__':
	main()

# end-of-file


"""
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking api.myip.com (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        cloudflare
Server Hostname:        api.myip.com
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-ECDSA-CHACHA20-POLY1305,256,256
Server Temp Key:        X25519 253 bits
TLS Server Name:        api.myip.com

Document Path:          /
Document Length:        52 bytes

Concurrency Level:      24
Time taken for tests:   148.077 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      10314014 bytes
HTML transferred:       520000 bytes
Requests per second:    67.53 [#/sec] (mean)
Time per request:       355.384 [ms] (mean)
Time per request:       14.808 [ms] (mean, across all concurrent requests)
Transfer rate:          68.02 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       89  194 1436.5    112   31739
Processing:   144  160  26.9    157     908
Waiting:      141  157  26.9    154     904
Total:        242  354 1436.7    269   31895

Percentage of the requests served within a certain time (ms)
  50%    269
  66%    273
  75%    275
  80%    277
  90%    282
  95%    287
  98%    300
  99%    604
 100%  31895 (longest request)



Este é o ApacheBench, Versão 2.3 <$ Revisão: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/

Licenciado para The Apache Software Foundation, http://www.apache.org/

Fast-HTTP Versão 1.0
Benchmarking api.myip.com

10000 requests divided into 417 blocks with 24 simultaneous requests

.....
40/417 blocks completed with 960 requests
80/417 blocks completed with 960 requests
120/417 blocks completed with 960 requests
160/417 blocks completed with 960 requests
200/417 blocks completed with 960 requests
240/417 blocks completed with 960 requests
280/417 blocks completed with 960 requests
320/417 blocks completed with 960 requests
360/417 blocks completed with 960 requests
400/417 blocks completed with 960 requests
417/417 blocks completed with 408 requests


Software de servidor: cloudflare
Nome do host do servidor: api.myip.com
Porta do servidor: 443
Protocolo SSL / TLS: TLSv1.2, ECDHE-ECDSA-CHACHA20-POLY1305,256,256
Chave temporária do servidor: X25519 253 bits
Nome do servidor TLS: api.myip.com
Caminho do documento: /
Comprimento do documento: 52 bytes

Nível de simultaneidade: 24
Tempo gasto para testes: 148,077 segundos
Pedidos completos: 10.000
Pedidos com falha: 0
Total transferido: 10314014 bytes
HTML transferido: 5.20000 bytes

Solicitações por segundo: 67,53 [# / seg] (média)
Tempo por solicitação: 355,384 [ms] (média)
Tempo por solicitação: 14,808 [ms] (média, em todas as solicitações simultâneas)
Taxa de transferência: 68,02 [Kbytes / s] recebidos
Tempos de conexão (ms)
              mínimo médio [+/- dp] mediano máximo
Conecte-se: 89 194 1436,5 112 31739
Processamento: 144 160 26,9 157 908
Em espera: 141 157 26,9 154 904
Total: 242 354 1436,7 269 31895
Porcentagem das solicitações atendidas dentro de um determinado tempo (ms)
  50% 269
  66% 273
  75% 275
  80% 277
  90% 282
  95% 287
  98% 300
  99% 604
 100% 31895 (solicitação mais longa)

"""