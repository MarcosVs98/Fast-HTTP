import sys
import random
import logging
from fake_useragent import UserAgent

# Rastreie com responsabilidade, identificando-se 
# (e seu site) no agente do usuário
USER_AGENT = UserAgent().random
# Configure o máximo de blocos 
CONCURRENT_BLOCKS   = 417
# Configure o máximo de solicitações simultâneas executadas
CONCURRENT_REQUESTS = 24

DOWNLOAD_DELAY = 0.57

# HTTP status code 
HTTP_HTTP_SUCESS    = range(200, 207)
HTTP_REDIRECTION    = range(300, 309)
HTTP_CLIENT_ERROR   = range(400, 452)
HTTP_SERVER_ERROR   = range(500, 512)

# A configuração de atraso no download respeitará apenas um dos seguintes:
CONCURRENT_REQUESTS_PER_DOMAIN = 10000
CONCURRENT_REQUESTS_PER_IP = 100000

# Utilizado nessa maneira para o 'japronto'
AUTOTHROTTLE_MAX_DELAY   = 0.00026
AUTOTHROTTLE_START_DELAY = 0.00002
AUTOTHROTTLE_SOCK_DELAY  = 0.00100
AUTOTHROTTLE_READ_DELAY  = 0.00100

# Desativar cookies (ativado por padrão)
COOKIES_ENABLED = False

# Desativar console Telnet (ativado por padrão)
TELNETCONSOLE_ENABLED = False

# Substitua os cabeçalhos de solicitação padrão:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-agent':USER_AGENT
}

# O número médio de solicitações WGFastRequest deve
# enviar paralelamente ao cada servidor remoto
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Ative a exibição de estatísticas de otimização para cada resposta recebida:
AUTOTHROTTLE_DEBUG = False

# O atraso máximo de download a ser definido em caso de altas latências
DEFAULT_REQUEST_TIMEOUT = {
    "total"       : AUTOTHROTTLE_MAX_DELAY, 
    "connect"     : AUTOTHROTTLE_START_DELAY,
    "sock_connect": AUTOTHROTTLE_SOCK_DELAY, 
    "sock_read"   : AUTOTHROTTLE_READ_DELAY
}

LOGGER = {
	'datefmt'  : '%Y-%m-%d %H:%M:%S',
	'format'   :'[%(asctime)s][%(threadName)s][%(module)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s',
	'level'    : logging.INFO,
	'stream'   : sys.stdout
}

LUMINATI = {
	'countries' : ['al', 'ar', 'am', 'au', 'at', 'az', 'bd', 'by', 'be', 'bo',
		'br', 'bg', 'kh', 'ca', 'cl', 'cn', 'co', 'cy', 'cz', 'dk', 'do', 'ec',
		'eg', 'ee', 'fi', 'fr', 'ge', 'de', 'gr', 'gt', 'hk', 'hu', 'is', 'in',
    	'id', 'ie', 'il', 'it', 'jm', 'jp', 'jo', 'kz', 'kr', 'kg', 'la', 'lv',
		'lt', 'lu', 'my', 'mx', 'md', 'ma', 'nl', 'nz', 'no', 'pk', 'pa', 'pe',
		'ph', 'pl', 'pt', 'ro', 'ru', 'sa', 'sg', 'sk', 'za', 'es', 'lk', 'se',
		'ch', 'tw', 'tj', 'th', 'tr', 'tm', 'ua', 'ae', 'gb', 'us', 'uz', 'vn'],

	'hostname'  : 'zproxy.lum-superproxy.io',
	'port'      : 22225,
	'baseuser'  : '************',
	'passwd'    : '************',
	'zone'      : 'iptester'
}

#end-of-file