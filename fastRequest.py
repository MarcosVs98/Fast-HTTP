import json
import time
import asyncio
import aiohttp
import random
from queue import Queue
from utils import generate_proxy_address
from clientResponse import dict_response 
from exceptions import FailedAIO
from clientResponse import ClientResponse
from settings import DEFAULT_REQUEST_HEADERS
from settings import DEFAULT_REQUEST_TIMEOUT
from settings import CONCURRENT_BLOCKS
from settings import CONCURRENT_REQUESTS


class ClientSession:
	"""
		Classe responsável por montar interface para realização de solicitações HTTP. 
  		A sessão encapsula um conjunto de conexões suportando keepalives por padrão.   
	"""
	def __init__(self,loop=None, connector=None, cookies=None, headers=DEFAULT_REQUEST_HEADERS, timeout=None, **kwargs):

		self.loop      = loop
		self.connector = connector
		self.cookies   = cookies
		self.headers   = headers
		self.timeout   = timeout

	def connect(self):

		kwargs = {
			"connector"            : self.connector,
			"loop"                 : self.loop, 
			"cookies"              : self.cookies, 
			"headers"              : self.headers, 
			"skip_auto_headers"    : None, 
			"auth"                 : None, 
			"json_serialize"       : json.dumps, 
			"cookie_jar"           : None, 
			"read_timeout"         : None, 
			"conn_timeout"         : None, 
			"raise_for_status"     : True, 
			"connector_owner"      : True, 
			"auto_decompress"      : True, 
			"requote_redirect_url" : False, 
			"trust_env"            : False, 
			"trace_configs"        : None
		}

		return aiohttp.ClientSession(**kwargs)

	async def __aenter__(self):
		return self.session

	async def __aexit__(self, exc_type, exc, tb):
		return self.connect().close()

	async def __aiter__(self):
		return self
    
	async def __await__(self):
		return self.connect().__await__()


class HTTPRequest(object):
	"""
		Classe responsavel por executar solicitações HTTP assíncronas 
		e retornar objetos de resposta.
	"""
	def __init__(self, method, url, headers=None, cookies=None, redirects=None,max_redirects=None, auth=None, timeout=None, 
			postdata=None, proxy=None, luminati=False, proxy_user=None, proxy_auth=None, proxy_pass=None, proxy_headers=None,json=None,
   			 params=None, skip_auto_headers=None, ssl=True, sslcontext=None, verify_ssl=True, raise_for_status=False):

		self.method            = method.upper()
		self.url               = url
		self.headers           = headers
		self.cookies           = cookies
		self.redirects         = redirects
		self.max_redirects     = max_redirects
		self.auth              = auth
		self.timeout           = timeout
		self.postdata          = postdata
		self.proxy             = proxy
		self.luminati          = luminati 
		self.proxy_auth        = proxy_auth
		self.proxy_user        = proxy_user
		self.proxy_pass        = proxy_pass
		self.proxy_headers     = proxy_headers
		self.json              = json
		self.params            = params
		self.skip_auto_headers = skip_auto_headers
		self.ssl               = ssl
		self.sslcontext        = sslcontext
		self.verify_ssl        = verify_ssl
		self.raise_for_status  = raise_for_status
		self.loop = None
 
	async def prepare_request(self):

		if not self.headers:
			self.headers = DEFAULT_REQUEST_HEADERS
  
		if self.timeout:
			self.timeout = aiohttp.ClientTimeout(**DEFAULT_REQUEST_TIMEOUT)
   
		if self.luminati is True:
			self.proxy = generate_proxy_address()
   
		if self.proxy_user and self.proxy_pass:
			self.proxy_auth = aiohttp.BasicAuth(self.proxy_user, self.proxy_pass)
		
		if self.verify_ssl and self.sslcontext:
			#Path dos certificados exemplo '/path/to/ca-bundle.crt'
			self.ssl.create_default_context(cafile=self.sslcontext)
	
		kwargs = {
				"params"               : self.params,
				"data"                 : self.postdata,
				"json"                 : self.json, 
				"cookies"              : self.cookies, 
				"headers"              : self.headers, 
				"skip_auto_headers"    : self.skip_auto_headers,
				"auth"                 : self.auth, 
				"allow_redirects"      : self.redirects, 
				"max_redirects"        : self.max_redirects, 
				"compress"             : None, 
				"chunked"              : None, 
				"raise_for_status"     : self.raise_for_status,
				"proxy"                : self.proxy, 
				"proxy_auth"           : self.proxy_auth, 
				"timeout"              : self.timeout, 
				"ssl"                  : self.ssl, 
				"verify_ssl"           : self.verify_ssl, 
				"proxy_headers"        : self.proxy_headers
		}
		try:
			###############################################
			#     CRIA UMA INSTANCIA DE CLIENT SESSION    #
			###############################################
			async with ClientSession().connect() as client:
				
				######################################
				#           SOLICITAÇÃO GET          #
				######################################
				if self.method == 'GET':
					async with client.get(self.url,**kwargs) as resp:
						return ClientResponse(**await dict_response(resp)) 
					raise aiohttp.errors.ClientResponseError('Falha de resposta')

				######################################
				#          SOLICITAÇÃO POST          #
				######################################
				elif self.method == 'POST':
					async with client.post(self.url,**kwargs) as resp:
						return ClientResponse(**await dict_response(resp))
					raise aiohttp.errors.ClientResponseError('Falha de resposta')

				######################################
				#          SOLICITAÇÃO PUT           #
				######################################
				elif self.method == 'PUT':
					async with client.put(self.url,**kwargs) as resp:
						return ClientResponse(**await dict_response(resp))
					raise aiohttp.errors.ClientResponseError('Falha de resposta')

				######################################
				#           SOLICITAÇÃO HEAD         #
				######################################
				elif self.method == 'HEAD':
					async with client.head(self.url,**kwargs) as resp:
						return ClientResponse(**await dict_response(resp))
					raise aiohttp.errors.ClientResponseError('Falha de resposta')

				######################################
				#     SOLICITAÇÂO NÃO IMPLEMENTADA   #
				######################################
				else:
					raise aiohttp.errors.ClientRequestError("Método de requisição não suportado")
			raise aiohttp.ClientError('Falha ao conectar à interface.')
		except Exception as exc:
			print('Erro inesperado')
   
	@property
	def loop_generator(self):
		return asyncio.get_event_loop()

	@property
	def close_loop(self):
		if self.loop is not None:
			self.loop()
		raise Exception('Encerramento do loop falhou.')

	async def fetch(self):
		return await self.prepare_request()
	
	def result(self):
		self.loop = self.loop_generator
		return self.loop.run_until_complete(self.fetch())  
	
	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass



class FastHTTP(object):
	"""
		Classe responsável por realizar solicitações simulataneas.
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

#end-of-file