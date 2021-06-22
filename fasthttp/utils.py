"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""

import ssl
import types
import socket
import urllib3
import requests
import argparse
import netifaces
from dataclasses import dataclass
from urllib.parse import urlparse
from abc import ABC, abstractmethod
from fasthttp.__version__ import __title__
from fasthttp.__version__ import __version__
from fasthttp.__version__ import __description__
from fasthttp.__version__ import __copyright__

INFO = types.SimpleNamespace(title=__title__,
	                         version=__version__,
	                         description=__description__,
	                         copyright=__copyright__)

SOCK = None

@dataclass
class Structure(ABC):
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


def get_ipv4_addresses():
	for name in netifaces.interfaces():
		iface = netifaces.ifaddresses(name)
		for addr in iface.get(netifaces.AF_INET, []):
			yield addr.get('addr')


def humanbytes(b):

	b = float(b)
	kb = float(1024)
	mb = float(kb ** 2) # 1,048,576
	gb = float(kb ** 3) # 1,073,741,824
	tb = float(kb ** 4) # 1,099,511,627,776

	if b < kb:
		return '{0} {1}'.format(b,'Bytes' if 0 == b > 1 else 'Byte')
	elif kb <= b < mb:
		return '{0:.2f} KB'.format(b/kb)
	elif mb <= b < gb:
		return '{0:.2f} MB'.format(b/mb)
	elif gb <= b < tb:
		return '{0:.2f} GB'.format(b/gb)
	elif tb <= b:
		return '{0:.2f} TB'.format(b/tb)


def validate_url(url):
	uri = urlparse(url)
	if not all((uri.scheme, uri.netloc, uri.path)):
		raise argparse.ArgumentTypeError(
			"URL used for fetching is malformed, e.g. it does not contain host part")
	return uri.geturl()


def str_auth_tuple(s):
	if isinstance(s, str) and len(s.replace('.', '')) == 2:
		if int(s[0]) == 1 and int(s[-1]) in [0, 1]:
			return int(s[0]), int(s[-1])
	raise Exception("HTTP version is not supported.")


def str_to_tuple(s):
	if isinstance(s, str):
		return s[0], s[-1]
	raise Exception("HTTP auth error.")


def get_family(n):
	return settings.TCP_SOCKET_FAMILY.get(int(n))


def get_tls_info(url):
	tls_info = types.SimpleNamespace(
		tls_protocol=None,
		tls_remote_certificate=None,
		tls_version=None)

	_orig_connect = urllib3.connection.VerifiedHTTPSConnection.connect

	def _connect(self):
		global SOCK
		_orig_connect(self)
		SOCK = self.sock

	try:
		urllib3.connection.VerifiedHTTPSConnection.connect = _connect
		requests.get(url)
	except requests.RequestException:
		raise ("Request Exception.")

	try:
		tlscon = SOCK.connection
		tls_info.tls_protocol = f"{tlscon.get_cipher_name()}, {tlscon.get_cipher_version()}, {tlscon.get_cipher_bits()}"
		tls_info.tls_remote_certificate = tlscon.get_peer_certificate()
		tls_info.tls_version = tlscon.get_protocol_version_name()
		return tls_info
	except AttributeError:
		return tls_info


# end-of-file