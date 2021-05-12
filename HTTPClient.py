import io
import json
import time
import logging
import asyncio
import aiohttp
import random
from queue import Queue
from entities import dict_response
from exceptions import FailedAIO
from entities import ClientResponse
from settings import DEFAULT_REQUEST_HEADERS
from settings import DEFAULT_REQUEST_TIMEOUT
from settings import CONCURRENT_BLOCKS
from settings import CONCURRENT_REQUESTS

from entities import HTTPRedirectHistoryItem
from entities import SHTTPRequest
from entities import SClientSession, ClientResponse


log = logging.getLogger('HTTPClient')


class HTTPClientException(Exception):
	pass

class HTTPClientEmptyResponseException(HTTPClientException):
	pass

class HTTPClientTimeoutException(HTTPClientException):
	pass

class HTTPClientTooManyRedirectsException(HTTPClientException):
	pass

class HTTPClientResolveHostException(HTTPClientException):
	pass



class ClientSession:
	"""
		Classe responsável por montar interface para realização de solicitações HTTP. 
		A sessão encapsula um conjunto de conexões suportando keepalives por padrão.   
	"""

	def _init__(self, **kwargs):
		self.connect(**kwargs)

	def connect(self, **kwargs):
		kwargs.update({
			"skip_auto_headers"    : None, 
			"auth"                 : None, 
			"json_serialize"       : json.dumps, 
			"cookie_jar"           : None, 

			"conn_timeout"         : None,   
			"raise_for_status"     : True, 
			"connector_owner"      : True, 
			"auto_decompress"      : True, 
			"requote_redirect_url" : False, 
			"trust_env"            : False, 
			"trace_configs"        : None
		})


		return aiohttp.ClientSession(**kwargs)

	async def aenter__(self):
		return self.session

	async def aexit__(self, exc_type, exc, tb):
		return self.connect().close()

	async def aiter__(self):
		return self

	async def await__(self):
		return self.connect().__await()





class HTTPRequest():
	"""
		Classe responsavel por executar solicitações HTTP assíncronas 
		e retornar objetos de resposta.
	"""
	def __init__(self):
		self._response = None
		self._loop = None
  
	async def send_request(self, request=None, *args, **kwargs):

		if request is None:
			request = SHTTPRequest(**kwargs)

		log.debug(f'HTTP Client Request: {request}')

		contents_buffer = io.BytesIO()
		
		## request Headers
		if request.headers is not None:
			if not isinstance(request.headers, (list, tuple)):
				raise WGHTTPClientException(f'Invalid request headers')
			if not all(isinstance(i, (tuple, list)) for i in request.headers):
				raise WGHTTPClientException(f'Invalid request headers')
			if not all(len(i) == 2 for i in request.headers):
				raise WGHTTPClientException(f'Invalid request headers')
			rawheaders = [f'{k}: {v}' for k, v in request.headers]
		else:
			request.headers = DEFAULT_REQUEST_HEADERS

		# Timeout
		if not request.timeout:
			request.timeout = aiohttp.ClientTimeout(**DEFAULT_REQUEST_TIMEOUT)

		# Local Address

		# Open Socket Callback

		# HTTP Proxy
		#if request.proxy_user and request.proxy_pass:
		#	print(f'Proxy Server Enabled: address="{request.proxy_host}" port="{request.proxy_port}"')
		#	request.proxy_auth = aiohttp.BasicAuth(request.proxy_user, request.proxy_pass)

		# Certificados / SSL
		if request.verify_ssl and request.sslcontext:
			# Path dos certificados exemplo '/path/to/ca-bundle.crt'
			self.ssl.create_default_context(cafile=self.sslcontext)
		try:
			# Cliente Aio Session!
			async with ClientSession().connect() as client:
				# HTTP Method
				if request.method == 'GET':
					# keep or remove ? 
					kwargs.pop('method', None)
					kwargs.pop('sslcontext', None)
					async with client.get(**kwargs) as resp:
						self.response = ClientResponse(**await dict_response(resp))
				elif request.method == 'POST':
					async with client.post(self.url,**kwargs) as resp:
						self.response = ClientResponse(**await dict_response(resp))
				elif request.method == 'PUT':
					async with client.put(self.url,**kwargs) as resp:
						self.response = ClientResponse(**await dict_response(resp))
				elif request.method == 'HEAD':
					async with client.head(self.url,**kwargs) as resp:
						self.response = ClientResponse(**await dict_response(resp))
				else:
					raise aiohttp.errors.ClientRequestError("Método de requisição não suportado")
			log.debug(f'HTTP Server Response: {self.response}')
			# return response
			return self.response

		except aiohttp.ClientError as exc:
			print(f'HTTP Server Response: {response}')
			raise aiohttp.ClientError('Falha ao conectar à interface.')

	def get(self, url, **kwargs):
		kwargs.update({'url': url, 'method': 'GET'})
		return self.prepare_request(**kwargs)

	def post(self, url, **kwargs):
		kwargs.update({'url': url, 'method': 'POST'})
		return self.prepare_request(**kwargs)

	def head(self, url, **kwargs):
		kwargs.update({'url': url, 'method': 'HEAD'})
		return self.prepare_request(**kwargs)

	def get_loop(self):
		return asyncio.get_event_loop()

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop()
		raise Exception('Encerramento do loop falhou.')

	async def fetch(self, **kwargs):
		return await self.send_request(**kwargs)

	def prepare_request(self, **kwargs):
		self.loop = self.get_loop()
		return self.loop.run_until_complete(self.fetch(**kwargs))

	def __repr__(self):
		return (f'http-client ('
		        f'{self.response.status} '
		        f'{self.response.reason})')

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass



request = HTTPRequest()
print(request.get('https://www.panvel.com/panvel/main.do').status)
print(request)



'''
class FastHTTP(object):
	"""
		Classe responsável por realizar solicitações simulataneas.
		Receber uma lista de objetos e manda brasa com thread pool
	"""
	def __init__(self, method, concurrent_requests, max_queue_size=0, concurrent_blocks=None): 

		self.method              = method
		self.max_queue_size      = max_queue_size
		self.concurrent_requests = concurrent_requests
		self.queue_block         = Queue(maxsize=self.max_queue_size)
		self.queue_result        = Queue(maxsize=self.max_queue_size)
		self.out_queue           = Queue(maxsize=self.max_queue_size)
		self.concurrent_blocks   = concurrent_blocks
		self.fake_block_size     = CONCURRENT_BLOCKS
		self.loop                = None
		self.urls                = []

	###################################################
	#   REALIZA A MONTAGEM DOS BLOCOS DE SOLICITAÇÃO  #
	###################################################
	def recover_block(self):
		for url in self.urls:
			try:
				request  = HTTPRequest(self.method, url)
				future   = asyncio.ensure_future(request.fetch())
				self.queue_block.put(future)

			except Exception as exc:
				try:
					code = exc.code
				except AttributeError:
					code = ''
					raised_exc = FailedAIO(code=code, message=exc, 
							 url=url,raised=exc.__class__.__name__)
				else:
					raised_exc = None
					print("Erro inesperado {}".format(exc))
					break

	###################################################
	#         REALIZA AS REQUISIÇÔES SIMULTANEAS      #
	###################################################
	def quick_response(self):
		try:
			self.loop = self.loop_generator
			self.loop.run_until_complete(asyncio.wait(
			self.queue_block.queue, return_when=asyncio.FIRST_COMPLETED))
   
			while not self.queue_block.empty():
				try:
					task = self.queue_block.get(block=True)
					self.queue_result.put(task.result())
				except Exception as exc:
					self.out_queue.put(task)
		except Exception as err:
			print("Erro inesperado :{}".format(err))
			self.close_loop

	##################################################
	#         NOVA TENTATIVA PARA OUT_QUEUE          #
	##################################################
	#não implementado

	###################################################
	#         INICIA O PROCESSAMENTO DAS URLS         #
	###################################################
	def start(self):
		japronto = 'http://0.0.0.0:8080'

		if self.urls:
			pass
		##################################
		#         INICIA O TESTE         #
		##################################
		start = time.time()  
		for _ in range(self.fake_block_size):    
			self.urls = [japronto for _ in range(self.concurrent_requests)]
			self.recover_block()
			self.quick_response()

		end = time.time()
		###################################################
		#                RESULTADO DOS TESTES             #
		###################################################
		print("Processamento finalizado.")
		print("Tempo de processamento             : ", round((end - start),4),"s")
		print("Numero requisições simultaneas     : ", self.concurrent_requests)
		print("Numero de blocos                   : ", self.fake_block_size)
		print("Tamanho da fila                    : " ,self.max_queue_size)
		print("Numero de conexões api(japronto)   : ", 200)
		print("Numero de requisições de sucesso   : ", self.queue_result.qsize())
		print("Número de requisições que falharam : ", self.out_queue.qsize())

	@property
	def loop_generator(self):
		return asyncio.get_event_loop()

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop()
		raise Exception('Encerramento do loop falhou.')
'''
#end-of-file
