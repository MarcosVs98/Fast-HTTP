"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
************************************************************************
"""
# Import's

# HTTPClient
from fasthttp import AsyncTCPConnector
from fasthttp import AsyncSession
from fasthttp import AsyncHTTPRequest
from fasthttp import AsyncRequestTimeout

# HTTPBenchmark
from fasthttp import HTTPBenchmark

# Benchmarking Command
from fasthttp import FastHTTPCommand


url = 'http://0.0.0.0:9999/'
#url = 'https://www.google.com/'



with HTTPBenchmark(method='get', url=url, concurrent_requests=120, concurrent_blocks=3) as benchmark:
	for n, resultados in enumerate(benchmark.blocks,1):
		print(n, resultados)
		#for r in resultados.block:
		#	print(n, r)



#benchmark.perform()





'''
import unittest

class FastHTTPtest(unittest.TestCase):

	def test_upper(self):
		print('1')
		self.assertEqual('foo'.upper(), 'FOO')

	def test_isupper(self):
		print('2')
		self.assertTrue('FOO'.isupper())
		self.assertFalse('Foo'.isupper())

	def test_split(self):
		s = 'hello world'
		print('3')
		self.assertEqual(s.split(), ['hello', 'world'])
		# check that s.split fails when the separator is not a string
		with self.assertRaises(TypeError):
			s.split(2)

if __name__ == '__main__':
    unittest.main()

'''
# end-of-file