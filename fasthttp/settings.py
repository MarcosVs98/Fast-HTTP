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
import socket
from pathlib import Path
from colorama import Fore, Style

#Configure the maximum number of requisition blocks
CONCURRENT_BLOCKS = 1
# Configure the maximum number of simultaneous requests
CONCURRENT_REQUESTS = 25
# set delay value for downloads
DOWNLOAD_DELAY = 0.57

# Size of the read buffer
READ_BUFSIZE = 2 ** 16

# HTTP status code 
HTTP_HTTP_SUCESS    = range(200, 207)
HTTP_REDIRECTION    = range(300, 309)
HTTP_CLIENT_ERROR   = range(400, 452)
HTTP_SERVER_ERROR   = range(500, 512)
# Async HTTP default status code
HTTP_CLIENT_DEFAULT_ERROR = 777 # Just an example of status

# Limits the total amount of parallel connections.
LIMIT_CONNECTIONS = 100

# Should the body response be automatically decompressed
AUTO_DESCOMPRESS = False

# The download delay setting will respect only one of the following.
# To limit the amount of open connection simultaneously to the same endpoint.
LIMIT_REQUESTS_PER_HOST = 0 #no limite
LIMIT_REQUESTS_PER_IP = 0 #no limite

# DNS caching enabled and resolutions will be cached by default for 10 seconds.
# This behavior can be changed.
TTL_DNS_CACHE = 300

# Should connector be closed on session closing.
CONNECTOR_OWNER = False

# Disables the use of the DNS cache table, causing all requests to end up doing a DNS resolution.
USE_DNS_CACHE = True

# Ajustar isso
AUTOTHROTTLE_MAX_DELAY   = 0.00020
AUTOTHROTTLE_START_DELAY = 0.00020
AUTOTHROTTLE_SOCK_DELAY  = 0.00020
AUTOTHROTTLE_READ_DELAY  = 0.00020

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Abort underlining transport after 2 seconds.
SHUTDOWN_TRANSPORT = False

# Disable Telnet console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Defaut Headers
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

# for fingerprint validation, ssl.SSLContext for custom SSL certificate validation.
SSL_CERTIFICATE_VALIDATION = None 

# Distribute http requests via network interface using round robin algoritm
ROUNDROBIN_ACTIVE = False # not implemented

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

# Maximum number of redirects
MAX_REDIRECTS = 30

# close underlying sockets after connection releasing (optional).
CLOSE_ALL_SOCKETS = True

# Certificates / SSL
VERIFY_SSL = False

# Default address to bind socket
DEFAULT_ADDRESS = ('0.0.0.0', None)

# Path absolute for ssl certificate.
DEFAULT_SSL_CONTEXT = None

ALLOW_REDIRECTS = True
RAISE_FOR_STATUS = False

# TCP socket family, both IPv4 and IPv6 by default.
TCP_SOCKET_FAMILY = { 4 : socket.AF_INET,  6 : socket.AF_INET6 }

# Custom resolvers allow you to resolve hostname.
RESOLVE_HOSTNAME = False

# end-of-file