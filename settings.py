import sys
import random
import logging

# Rastreie com responsabilidade, identificando-se

# Configure o máximo de blocos 
CONCURRENT_BLOCKS   = 2
# Configure o máximo de solicitações simultâneas executadas
CONCURRENT_REQUESTS = 40

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
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
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



#end-of-file