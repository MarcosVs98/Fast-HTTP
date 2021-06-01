"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************
"""
import logging
import threading
from HTTPClient import AsyncHTTPRequest
from abc import ABC, abstractmethod
from queue import Queue


class ThreadPool(ABC):
	"""
		Representa um Pool de Threads
	"""
	def __init__(self, nthreads, maxqueue=0):
		self._queue = queue.Queue(maxqueue)
		self._nthreads = nthreads
		self._threads = [None] * nthreads
		self._active = False

	@abstractmethod
	def handler(self, task):
		pass

	def _thread_handler(self):
		while self._active:
			try:
				task = self._queue.get(block=True, timeout=0.5)
				self.handler(task)
				self._queue.task_done()
			except queue.Empty:
				pass

	def start(self):
		if not self._active:
			self._active = True
			for i in range(self._nthreads):
				self._threads[i] = threading.Thread(target=self._thread_handler)
				self._threads[i].daemon = True
				self._threads[i].start()

	def stop(self):
		if self._active:
			self._active = False
			for i in range(self._nthreads):
				self._threads[i].join()
				self._threads[i] = None

	def add_task(self, task):
		self._queue.put(task, block=True, timeout=None)

	def task_count(self):
		return self._queue.qsize()

	def wait_tasks(self):
		self._queue.join()

	def __enter__(self):
		self.start()
		return self

	def __exit__(self, _type, value, traceback):
		self.stop()
		return False



class PublicProxiesPool(ThreadPool):
	"""
	Classe responsável por representar um pool de proxies públicos.

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

	ref: https://github.com/clarketm/proxy-list
	"""
	def __init__(self, nthreads):
		ThreadPool.__init__(nthreads)
		self.client = AsyncHTTPRequest()

	def get_proxies_list(self):
		response = self.client.get(settings.PUBLIC_PROXIES)



			

	





# end-of-file