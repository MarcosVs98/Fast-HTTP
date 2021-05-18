from dataclasses import dataclass
from abc import ABC, abstractmethod

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

# end-of-file