#############################################################################
## Marcos Vinicios da Silveira                                             ##
#############################################################################
import io
import asyncio
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from settings import DEFAULT_REQUEST_HEADERS
from urllib.parse import urlencode, urlparse



@dataclass
class WBEntity(ABC):
	def __init__(self, **kwargs):
		self.update(kwargs)

	def to_dict(self):
		return vars(self)

	def update(cls, dic):
		for k, v in dic.items():
			setattr(cls, k, v)

	def get(self, key, NaN=None):
		return self.__dict__.get(key, NaN)

	def __str__(self):
		res = {k: v for k, v in self.__dict__.items()}
		return str(res)

	def __repr__(self):
		return self.__str__()

	def __getitem__(cls, x):
		return getattr(cls, x)

	def __setitem__(cls, key, value):
		return setattr(cls, key, value)

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass

	def __del__(self):
		pass

	def __len__(self):
		return len(self.__dict__)




class SClientSession(WBEntity):
	"""
		Classe de dados responsável por incapsular e representar os
		campos de uma sessão http.
	"""
	loop      : list = field(default=None)
	connector : list = field(default=None)
	cookies   : dict = field(default=None)
	headers   : dict = field(default=DEFAULT_REQUEST_HEADERS)
	timeout   : int  = field(default=30)
	

@dataclass
class HTTPRedirectHistoryItem(WBEntity):
	"""
		Classe de dados responsavel por representar
		os campos de um header de resposta HTTP
	"""
	http_version     : str = None
	status_code      : int = 0
	reason           : str = None
	headers          : list = None


#domain            : str = field(default=None)
#scheme            : str = field(default=None)
#postdata          : bytes = field(default=None, repr=False)
#http_version      : str = field(default='HTTP/1.1')
#follow_redirects  : bool = field(default=True)
#redirects         : int = field(default=30)
#proxy_host        : str = field(default=None)
#proxy_port        : int = field(default=0)
#proxy_user        : str = field(default=None)
#proxy_pass        : str = field(default=None)
#outbound_address  : str = field(default=None)
#ssl_verify        : bool = field(default=False)
#sslcontext        : str = field(default=None)

@dataclass
class AIORequests(WBEntity):
	url               : str
	params            : list = field(default=None)
	cookies           : list = field(default=None)
	headers           : list = field(default=None)
	json              : dict = field(default=None)
	timeout           : int = field(default=120)
	max_redirects     : int = field(default=30)
	auth              : str = field(default=None)
	proxy             : str = field(default=None)
	proxy_headers     : list = field(default=None)
	skip_auto_headers : bool = field(default=False)
	ssl               : bool = field(default=False)
	verify_ssl        : bool = field(default=False)
	raise_for_status  : bool = field(default=False)



@dataclass
class HTTPRequest(WBEntity):
	"""
		Classe de dados responsavel por representar
		os campos de uma requisicao HTTP
	"""
	method            : str
	domain            : str = field(default=None)
	scheme            : str = field(default=None)
	postdata          : bytes = field(default=None, repr=False)
	http_version      : str = field(default='HTTP/1.1')
	follow_redirects  : bool = field(default=True)
	redirects         : int = field(default=30)
	proxy_host        : str = field(default=None)
	proxy_port        : int = field(default=0)
	proxy_user        : str = field(default=None)
	proxy_pass        : str = field(default=None)
	outbound_address  : str = field(default=None)
	ssl_verify        : bool = field(default=False)
	sslcontext        : str = field(default=None)


	def __post_init__(self):
		uri = urlparse(self.url)
		self.domain = uri.netloc
		self.scheme = uri.scheme

	def __setattr__(self, name, value):
		if name == 'url':
			uri = urlparse(value)
			self.__dict__['domain'] = uri.netloc
			self.__dict__['scheme'] = uri.scheme
		self.__dict__[name] = value



async def auto_decode(content):
	for enc in ['ascii', 'utf8', 'iso-8859-1', 'cp-1252']:
		try:
			return await content(enc)
		except UnicodeDecodeError:
			pass



async def dict_response(response):

	res =  {
		"content_text"        : await auto_decode(response.text),
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

# end-of-file #



# end-of-file #

from types import SimpleNamespace

class ClientResponse(WBEntity):
	"""
		Classe de Dados responsavel por encapsular respostas de requisicoes HTTP.
		O ClientResponse suporta protocolo de gerenciador de contexto assíncrono
	"""
	def __str__(self):
		summary = SimpleNamespace(**{k:v for k,v in self.__dict__.items() if k not in ['content_text']})
		return (f'<[FHTTP/'
				f'{summary.status} '
				f'{summary.reason}]>')

	def __repr__(self):
		return __str__()

	def __enter__(cls):
		return cls

	def __exit__(cls, typ, value, tb):
		pass





