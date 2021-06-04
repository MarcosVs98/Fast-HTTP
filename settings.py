"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import sys
import random
import logging
from pathlib import Path
from colorama import Fore, Style


# Build paths inside the project like this: BASE_DIR / 'subdir'. <- Django ref
BASE_DIR = Path(__file__).resolve().parent.parent


# Fast http settings
APPLICATION_CONFIG = {
	'logging_mode'       : 'console_debug',
	'logfile'            : BASE_DIR / 'fasthttp.log'
}

#Configure the maximum number of requisition blocks
CONCURRENT_BLOCKS = 1

# Configure the maximum number of simultaneous requests
CONCURRENT_REQUESTS = 24

# set delay value for downloads
DOWNLOAD_DELAY = 0.57

# HTTP status code 
HTTP_HTTP_SUCESS    = range(200, 207)
HTTP_REDIRECTION    = range(300, 309)
HTTP_CLIENT_ERROR   = range(400, 452)
HTTP_SERVER_ERROR   = range(500, 512)

# The download delay setting will respect only one of the following
CONCURRENT_REQUESTS_PER_DOMAIN = 10000
CONCURRENT_REQUESTS_PER_IP = 100000


# Ajustar isso
AUTOTHROTTLE_MAX_DELAY   = 0.00020
AUTOTHROTTLE_START_DELAY = 0.00020
AUTOTHROTTLE_SOCK_DELAY  = 0.00020
AUTOTHROTTLE_READ_DELAY  = 0.00020

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Defaut Headers
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# Distribute http requests via network interface using round robin algoritm
ROUNDROBIN_ACTIVE = False

# The average number of HTTPRequest requests must
# send in parallel to each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0 #to control

# Enable the display of optimization logs for each response received:
AUTOTHROTTLE_DEBUG = False

# The maximum download delay to be defined in case of high latencies
DEFAULT_REQUEST_TIMEOUT = {

	"total"       : AUTOTHROTTLE_MAX_DELAY,
	"connect"     : AUTOTHROTTLE_START_DELAY,
	"sock_connect": AUTOTHROTTLE_SOCK_DELAY,
	"sock_read"   : AUTOTHROTTLE_READ_DELAY
}


PUBLIC_PROXY_RAW = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
PUBLIC_PROXY_LIST = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'


# Certificates / SSL
VERIFY_SSL = False

# Default address to bind socket
DEFAULT_ADDRESS = ('0.0.0.0')

# Configurações de Logging e Debugging

LOGGING_CONFIG = {
	'console_release' : {
		'format'   : '[%(asctime)s.%(msecs)03d][%(process)s]'
					 '[%(threadName)s] %(message)s',
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'level'    : logging.WARNING,
		'stream'   : sys.stdout
	},

	'logfile_release' : {
		'format'   : '[%(asctime)s.%(msecs)03d][%(process)s]'
					 '[%(threadName)s] %(message)s',
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'level'    : logging.WARNING,
		'filename' : APPLICATION_CONFIG['logfile']
	},

	'console_debug' : {
		'format'   : '[%(asctime)s.%(msecs)03d]'
					 '[PID-%(process)s][%(threadName)s]'
					 '[%(module)s:%(funcName)s:%(lineno)d] '
					 '%(levelname)s: '
					 '%(message)s',
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'level'    : logging.WARNING,
		'stream'   : sys.stdout
	},

	'logfile_debug' : {
		'format'   : '[%(asctime)s.%(msecs)03d]'
					 '[PID-%(process)s][%(threadName)s]'
					 '[%(module)s:%(funcName)s:%(lineno)d] '
					 '%(levelname)s: '
					 '%(message)s',
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'level'    : logging.DEBUG,
		'filename' : APPLICATION_CONFIG['logfile']
	},

	'console_color_debug' : {
		'format'   : f'{Fore.CYAN}[%(asctime)s.%(msecs)03d]'
					 f'{Fore.RED}[PID-%(process)s]'
					 f'{Fore.MAGENTA}[%(threadName)s]'
					 f'{Fore.GREEN}[%(module)s:%(funcName)s:%(lineno)d]'
					 f'{Fore.YELLOW}[%(name)s:%(levelname)s]'
					 f'{Fore.RESET}'
					 f': %(message)s',
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'level'    : logging.DEBUG,
		'stream'   : sys.stderr
	}
}

#end-of-file