from dataclasses import dataclass
import asyncio

@dataclass
class ClientResponse():
	"""
		Classe de Dados responsavel por encapsular
		respostas de requisicoes HTTP. O ClientResponse 
		suporta protocolo de gerenciador de contexto assíncrono
	"""
	content_text : str
	version      : None
	status       : int
	reason       : str
	method       : str 
	url          : str
	real_url     : str
	connection   : None
	content      : str
	cookies      : None
	headers      : None
	raw_headers  : None
	links	     : None
	content_type : None
	charset      : None 
	history      : None
	request_info : None
	release      : None

	def __str__(self):
		summary = {k:v for k,v in self.__dict__.items() if k not in ['content_text']}
		return str(summary)

	def __repr__(self):
		return self.__str__()

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass


async def dict_response(response):
	res =  {
		"content_text"        : await response.text('UTF-8'),
		"version"             : response.version,
		"status"              : response.status,
		"reason"              : response.reason,
		"method"              : response.method,
		"url"                 : response.url,
		"real_url"            : response.real_url,
		"connection"          : response.connection,
		"content"             : response.content,
		"cookies"             : response.cookies,
		"headers"             : response.headers,
		"raw_headers"         : response.raw_headers,
		"links"               : response.links,
		"content_type"        : response.content_type,
		"charset"             : response.charset,
		"history"	            : response.history,	
		"request_info"        : response.request_info,
		"release"             : await response.release(),
	}
	return res
# fim-de-arquivo #