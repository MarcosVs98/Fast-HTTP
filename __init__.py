from datetime import datetime
from dataclasses import dataclass , field
import settings
from HTTPClient import HTTPClient

PUBLIC_PROXIES_RAW = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
PUBLIC_PROXIES_LIST = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
PUBLIC_PROXIES_STATUS = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-status.txt'

@dataclass
class ProxyParsed():
	proxy_ip                   : str
	proxy_port                 : int
	proxy_scheme               : str
	proxy_level_anonymity      : int
	proxy_country              : str
	proxy_google_passed        : bool
	proxy_outgoing_ip          : bool
	proxy_uri                  : str
	proxy_status               : str = field(default="no-status-available")



class InvalidProxyToParser(Exception):
	pass

"""
# Definitions
----------------------------------------------------------------
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
----------------------------------------------------------------
"""

import json

class ProxyListAPI():
	"""
	Uma lista de servidores proxy gratuitos, públicos e de encaminhamento.
	Disponibilizados diariamente em 'https://github.com/clarketm/proxy-list'.
	"""
	def __init__(self):
		self.client = HTTPClient()
		self._proxies_result = {}
		self._proxies_status = {}
		self._initialize()

	def get_proxies(self, proxy_path=None):
		with open('proxy-list-cache.json', 'r') as f:
			proxies = json.load(f)
			if proxy_path:
				try:
					p, s = tuple(proxy_path.split('.'))
					return proxies[p][s]
				except (KeyError, ValueError):
					raise Exception("this filter is not available")
			return proxies['raw']

	def _get_proxy_list_status(self):
		response = self.client.get(settings.PUBLIC_PROXIES_STATUS)
		proxies_status = response.content_text.split('\n')
		for proxie in proxies_status:
			try:
				address, status = proxie.split(': ')
			except ValueError:
				continue
			self._proxies_status[address] = status

	def _order_proxies_by(self, proxy_item, ref, name=None):
		if not name in self._proxies_result:
			self._proxies_result[name] = {}
		if not ref in self._proxies_result[name]:
			self._proxies_result[name][ref] = []
		self._proxies_result[name][ref].append(proxy_item.__dict__)

	def _initialize(self):
		self._get_proxy_list_status()
		# get proxies list
		response = self.client.get(settings.PUBLIC_PROXIES_LIST)
		proxies = response.content_text.split('\n\n')
		proxies_header = proxies[0]
		proxies_list = proxies[1].split('\n')
		self._proxies_result['info'] = {}
		for proxy_line in proxies_list:
			proxy_item = self._parse(proxy_line)
			try:
				# get proxies status
				proxy_item.proxy_status = self._proxies_status[proxy_item.proxy_ip]
			except KeyError:
				pass
			# sort by proxy status
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_status, name="status")
			# sort by schema type
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_scheme, name="scheme")
			# sort by anonymity level
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_level_anonymity, name="level_anonymity")
			# sort by country of origin
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_country, name="country")
			# sorts by http port
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_port, name="http-port")
			# sort by proxy who goes through google
			self._order_proxies_by(proxy_item, ref=proxy_item.proxy_google_passed, name="google_passed")
			# all proxies
			if not 'raw' in self._proxies_result:
				self._proxies_result['raw'] = []
			self._proxies_result['raw'].append(proxy_item.__dict__)
		# parsing headers info
		self._proxies_result['info']['header'] = [line for line in proxies_header.split('\n')]
		self._proxies_result['info']['updated'] = str(datetime.now())
		self._proxies_result['info']['count_proxies'] = len(proxies_list)
		# statistics
		self._proxies_result['info']['success'] = len(self._proxies_result['status']['success'])
		self._proxies_result['info']['failure'] = len(self._proxies_result['status']['failure'])
		self._proxies_result['info']['no-status-available'] = len(self._proxies_result['status']['no-status-available'])
		success_rate = round(100 * (sum(1 for s in self._proxies_status.values()
			if s=='success'))/ len(self._proxies_status), 2)
		self._proxies_result['info']['success-rate'] = f"{success_rate}%"
		self._proxies_result['info']['failure-rate'] = f"{100.00 - success_rate}%"
		# Prepare a json file for cache
		with open('proxy-list-cache.json', 'w') as f:
			json.dump(self._proxies_result, f, indent=4)

	def _parse(self, proxy_line):
		"""
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
		└────────────┬────────────┘
				 Proxy line
		"""
		try:
			proxy_splited = proxy_line.split(' ')
			proxy_address_info = proxy_splited[0].split(':')
			proxy_ip = proxy_address_info[0]
			proxy_port = proxy_address_info[1]
			proxy_info = proxy_splited[1].split('-')
			proxy_country = proxy_info[0]
			proxy_level_anonymity = self._parse_anonymity(proxy_info[1])
			proxy_type = self._parse_proxy_type(proxy_info)
			proxy_outgoing_ip = self._parse_output_ip(proxy_type)
			proxy_scheme = self._parse_http_type(proxy_type)
			proxy_google_passed = self._parse_google_passed(proxy_line)
			proxy_uri = f"{proxy_scheme}://{proxy_ip}:{proxy_port}/"

			proxy_parsed = ProxyParsed(
				proxy_ip=proxy_ip, proxy_port=proxy_port,
				proxy_scheme=proxy_scheme,
				proxy_level_anonymity=proxy_level_anonymity,
				proxy_country=proxy_country,
				proxy_google_passed=proxy_google_passed,
				proxy_outgoing_ip=proxy_outgoing_ip,
				proxy_uri=proxy_uri)
			return proxy_parsed
		except IndexError as e:
			raise InvalidProxyToParser(e)

	def _parse_anonymity(self, proxy_info):
		if proxy_info.startswith('N'):
			proxy_level_anonymity = 0
		elif proxy_info.startswith('A'):
			proxy_level_anonymity = 1
		elif proxy_info.startswith('H'):
			proxy_level_anonymity = 2
		return proxy_level_anonymity

	def _parse_proxy_type(self, proxy_info):
		try:
			proxy_type = proxy_info[2]
		except IndexError:
			proxy_type = proxy_info[1]
		return proxy_type

	def _parse_google_passed(self, proxy_line):
		if proxy_line.endswith('+'):
			return True
		return False

	def _parse_output_ip(self, proxy_type):
		if proxy_type.endswith('!'):
			return True
		return False

	def _parse_http_type(self, proxy_type):
		if proxy_type.startswith('S'):
			return 'https'
		return 'http'


proxy_api = ProxyListAPI()

print(proxy_api.get_proxies('scheme.http'))
#	print(proxy)

#print(proxy_api.parse('190.92.9.162:999 HN-N-S -'))
#print(proxy_api.parse('82.114.93.210:8080 AL-N-S! -'))
#print(proxy_api.parse('95.0.90.243:8080 TR-A! + '))
#print(proxy_api.parse('173.46.67.172:58517 US-H -'))

