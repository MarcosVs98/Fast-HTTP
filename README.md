# Fast-HTTP
Aplicação em python utilizando aiohttp e japronto para realização de testes de performance http.

Todos testes foram realizados sobre a api de teste utilizando japronto com 200 conexões abertas. A api "hello_world.py" se encontra na raiz do projeto. Para realizar os testes dos exemplos abaixo é necessário iniciar o micro server.

![Web-Trader Block Diagram](https://github.com/MarcosVs98/Fast-HTTP/blob/main/example.png)

### Exemplo utilizando HTTPRequest
Classe responsavel por executar solicitações HTTP assíncronas e retornar objetos de resposta.
```pycon
>>> from fastRequest import HTTPRequest
>>> 
>>> url = 'https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'
>>>
>>> response = HTTPRequest('get',url)
>>> response.result()
>>>
{'version': HttpVersion(major=1, minor=1),'status': 200,'reason': 'OK','method': 'GET',
'url': URL('https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'),
'real_url': URL('https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'),
'connection': None,'content': <StreamReader eof e=ClientConnectionError('Connection closed',)>,
'cookies':<SimpleCookie: >,'headers':<CIMultiDictProxy('Content-Length':'2272','Connection':'keep-alive',
'Server':'Server','Date':'Tue, 12 May 2020 22:30:04 GMT','Edge-Control': 'no-store',
'Vary': 'Content-Type,Accept-Encoding,X-Amzn-CDN-Cache,X-Amzn-AX-Treatment,User-Agent',
'Content-Encoding': 'gzip','x-amz-rid': 'HVXNT5PSHKHJ99CBPY9P','X-Cache': 'Miss from cloudfront',
'Via': '1.1 ff59f24ad9231de5fbb56e661c4dad59.cloudfront.net (CloudFront)','X-Amz-Cf-Pop': 'GRU1-C1',
'X-Amz-Cf-Id': 'H_G1efnQihsuFOiiae7Vc6lN9zAXPehfFKdXUULEbIWfsZI9jkWSIg==')>,
'raw_headers': ((b'Content-Length', b'2272'), (b'Connection', b'keep-alive'), (b'Server', b'Server'), 
(b'Date', b'Tue, 12 May 2020 22:30:04 GMT'), (b'Vary', 
b'Content-Type,Accept-Encoding,X-Amzn-CDN-Cache,X-Amzn-AX-Treatment,User-Agent'), (b'Edge-Control',
b'no-store'), (b'Content-Encoding', b'gzip'), (b'x-amz-rid', b'HVXNT5PSHKHJ99CBPY9P'), (b'X-Cache',
b'Miss from cloudfront'), (b'Via', b'1.1 ff59f24ad9231de5fbb56e661c4dad59.cloudfront.net (CloudFront)'), 
(b'X-Amz-Cf-Pop', b'GRU1-C1'), (b'X-Amz-Cf-Id', b'H_G1efnQihsuFOiiae7Vc6lN9zAXPehfFKdXUULEbIWfsZI9jkWSIg==')),
'links': <MultiDictProxy()>,'content_type': 'application/octet-stream','charset': None,'history': (),
'request_info': RequestInfo(url=URL('https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6'), 
method='GET', headers=<CIMultiDictProxy('Host': 'www.amazon.com.br','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
>>>>>>> bdef12f7890feca86634ba77cb4630704197e752
'Accept-Language': 'en','User-agent': 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
'Accept-Encoding': 'gzip, deflate')>, real_url=URL('https://www.amazon.com.br/Novo-Kindle-Paperwhite-Agora-prova-agua/dp/B0773XBMB6')),
'release': None}
>>>
```
### Exemplo utilizando FastHTTP 
Classe responsável por realizar solicitações simulataneas.
```pycon
>>> from fastRequest import FastHTTP
>>> 
>>> assincrone_res = FastHTTP(method='get',concurrent_requests=24, 417)
>>> assincrone_res.start()
>>>
Processamento finalizado.
Tempo de processamento             :  13.9957 s
Número requisições simultaneas     :  24
Número de blocos                   :  417
Tamanho da fila                    :  0
Número de conexões api(japronto)   :  200
Número de requisições de sucesso   :  10008
Número de requisições que falharam :  0
>>> 
```
### Exemplo 2 FastHTTP
```pycon
>>> from fastRequest import FastHTTP
>>> 
>>> assincrone_res = FastHTTP(method='get',concurrent_requests=24, 834)
>>> assincrone_res.start()
>>>
Processamento finalizado.
Tempo de processamento             :  31.8837 s
Número requisições simultaneas     :  24
Número de blocos                   :  834
Tamanho da fila                    :  0
Número de conexões api(japronto)   :  200
Número de requisições de sucesso   :  20016
Número de requisições que falharam :  0
>>> 
```

### Exemplo utilizando ClientSession
Classe responsável por montar interface para realização de solicitações HTTP. A sessão encapsula um conjunto de conexões suportando keepalives por padrão.
```pycon
from fastRequest import ClientSession
>>> 
>>> client = ClientSession()
>>> client.connect()
<aiohttp.client.ClientSession object at 0x7f73edcb8080>
>>>
```

### License
```
MIT License

Copyright (c) 2020 MarcosVs98

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```