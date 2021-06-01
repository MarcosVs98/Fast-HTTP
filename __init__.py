
from dataclasses import dataclass
import settings
from HTTPClient import HTTPClient

#PUBLIC_PROXIES_LIST

# Obtein os proxies
client =  HTTPClient()
response = client.get(settings.PUBLIC_PROXIES_RAW)

#print(response.content_text)

#proxies_raw = response.content_text.split('\n')
#print(proxies_raw)


PUBLIC_PROXIES_RAW = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
PUBLIC_PROXIES_LIST = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
PUBLIC_PROXIES_STATUS = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-status.txt'

@dataclass
class ProxyParsed():
	ip                   : str
	port                 : int
	scheme               : str
	level_anonymity      : int
	proxy_contry         : str
	proxy_google_passed  : bool
	outgoing_ip          : bool

	def get_proxy(self):
		return f"{self.scheme}://{self.ip}:{self.port}/"


class InvalidProxyToParser(Exception):
	pass


"""
	# Definitions

	1. IP address
	2. Port number
	3. Country code
	4. Anonymity
	   N = No anonymity
	   A = Anonymity
	   H = High anonymity
	5. Type
		 = HTTP
	   S = HTTP/HTTPS
	   ! = incoming IP different from outgoing IP
	6. Google passed
	   + = Yes
	   – = No
"""


def parse_public_proxies(proxy):
	"""
	ref: https://github.com/clarketm/proxy-list

	IP [1]
	|
	| Port [2]
	|   |
	|   | Country [3]
	|   |   |
	|   |   | Anonymity [4]
	|   |   |  |
	|   |   |  |  Type [5]
	|   |   |  |   |_ _ _ _
	|   |   |  |_ _ _ _ _  | Google passed [6]
	|   |   |_ _ _ _ _   | |  |
	|   |_ _ _ _ _    |  | |  |
	|             |   |  | |  |
	200.2.125.90:8080 AR-N-S! +
	"""
	try:
		proxy_raw = proxy.split(' ')
		address_info = proxy_raw[0].split(':')
		ip = address_info[0] 
		port = address_info[1]
		proxy_info  = proxy_raw[1].split('-')

		proxy_contry    = proxy_info[0]  
		proxy_anonymity = proxy_info[1]

		if proxy_anonymity.startswith('N'):
			level_anonymity = 0
		elif proxy_anonymity.startswith('A'):
			level_anonymity = 1
		elif proxy_anonymity.startswith('H'):
			level_anonymity = 2
		try:
			proxy_type = proxy_info[2]
		except IndexError:
			proxy_type = proxy_info[1]

		if proxy_type.startswith('S'):
			scheme = 'https'
		else:
			scheme = 'http'

		if proxy_type.endswith('!'):
			outgoing_ip = True
		else:
			outgoing_ip = False

		if proxy.endswith('+'):
			proxy_google_passed = True
		else:
			proxy_google_passed = False

		proxy_parsed = ProxyParsed(
			ip=ip, port=port, scheme=scheme,
			level_anonymity=level_anonymity,
			proxy_contry=proxy_contry,
			proxy_google_passed=proxy_google_passed,
			outgoing_ip=outgoing_ip)

		return proxy_parsed
	except IndexError as e:
		raise InvalidProxyToParser(e)


print(parse_public_proxies('190.92.9.162:999 HN-N-S -').get_proxy())
print(parse_public_proxies('82.114.93.210:8080 AL-N-S! -').get_proxy())
print(parse_public_proxies('95.0.90.243:8080 TR-A! + ').get_proxy())
print(parse_public_proxies('173.46.67.172:58517 US-H -').get_proxy())

