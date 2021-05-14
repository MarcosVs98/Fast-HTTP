'''
from fastRequest import FastHTTP
from fastRequest import HTTPRequest


#assincrone_res = FastHTTP(method='get',concurrent_requests=24)
#assincrone_res.start()
'''
from HTTPClient import HTTPClient, HTTPBoost


request = HTTPClient()
response = request.get('https://www.panvel.com/panvel/main.do')
print(response.request_info)



assincrone_res = HTTPBoost(url='https://www.panvel.com/panvel/main.do', method='get',concurrent_requests=24)
assincrone_res.start()

#url = 'https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'

#response = HTTPRequest('get',url)
#print(response.result())

#from entities import *

#ss = ClientResponse('https://www.google.com', 'get')
#print(ss)

