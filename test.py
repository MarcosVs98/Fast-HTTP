'''
from fastRequest import FastHTTP
from fastRequest import HTTPRequest


#assincrone_res = FastHTTP(method='get',concurrent_requests=24)
#assincrone_res.start()
'''
from fastRequest import HTTPRequest

url = 'https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'

response = HTTPRequest('get',url)
print(response.result())
