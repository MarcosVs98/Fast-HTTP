 # Fast-HTTP

Python library for making asynchronous HTTP requests.
 ![Web-Trader Block Diagram](https://github.com/MarcosVs98/Fast-HTTP/blob/main/example.png)


* [Installation](#install)
* [Usage](#usage)
* [API](#api)
* [Acknowledgements](#acknowledgements)
* [License](#license)

## Sobre
Fast-HTTP é uma biblioteca empacotada com um cliente HTTP assíncrono, que permite paralelizar solicitações http, a fim de 
otimizar e melhorar a persistência com o servidor destino.Tudo isso porque o protocolo HTTP oferece pipelining, 
permitindo o envio de múltiplas ocorrências na mesma conexão sem esperar por respostas.Portanto, a chamada não é 
bloqueada ou fechada enquanto o servidor HTTP responde.

### Assincrono em Python
Se torna uma função/método assíncrono usando a palavra reservada "async" antes da definição e também utilizando outra palavra 
reservada chamada "await" na implementação, para que assim possa saber esperar algo. 

### Cliente HTTP

Exemplo simples do uso cliente HTTP.
```pycon
>>> from fasthttp.HTTPClient import AssyncHTTPClient
>>>
>>> client = AssyncHTTPClient()
>>> response = client.get("https://www.python.org/")
>>> response 
<FHTTP Response [200 OK]>
>>>
```

## Instalação

```
python setup.py install
```

### Clonando o repositório
```
$ git clone https://github.com/MarcosVs98/Fast-HTTP.git
```

## Parametros
A parametrização base da aplicação foi baseada nos próprios parametros já utilizados pela biblioteca núcleo [aiohttp](https://docs.aiohttp.org/en/stable/) utilizado neste projeto.

Para controle de envio, os parametros foram armazenados em estruturas de dados específicas utilizando decoradores de nível de múdulo da [dataclasses](https://docs.python.org/3/library/dataclasses.html).

### Resquest (AsyncHTTPRequest)

Estrutura de dados responsável por encapsular os dados de solicitação. 

* `url`: Atríbuto obrigátorio para instância do AsyncHTTPClient. [ref](https://pt.wikipedia.org/wiki/URI)
* `method`: Método de requisição responsável por indicar a ação a ser executada para um dado recurso. [ref](https://pt.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
* `headers`: Adicão de cabeçalho arbitrário. Cabeçalhos contendo mais informação sobre o recurso a ser obtido ou sobre o próprio cliente. [ref](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields)
* `timeout`: Tempo máximo em segundos para o aguardo de resposta http.
* `postdata`: Conteúdo a ser enviado ao servidor alvo.
* `http_version`: Versão http para utilização. Disponíveis HTTP/1.0 e 1.1.
* `auth_user`: Login para autenticação do cliente.
* `auth_pass`: Senha para autenticação do cliente.
* `allow_redirects`: Cliente http, permite redirecionamento pelo servidor. 
* `redirects`: Número máximo de redirecionamentos permitidos.
* `proxy_host`: Login para autenticação do cliente utilizando proxy.
* `proxy_pass`: Senha para autenticação do cliente utilizando proxy.
* `outbound_address`: Endereço de IP utilizado para saída.Por default é definido  `0.0.0.0` .
* `sslcontext`: Endereço do arquivo de certificação para criação de contexto SSL.
* `proxy_headers`: Adicão de cabeçalho arbitrário. Cabeçalhos contendo mais informação sobre o recurso a ser obtido ou sobre o próprio cliente utilizando proxy.
* `raise_for_status`: Levantar exceção para códigos de status diferente de 200.

### Session (AsyncSession)
Estrutura de dados responsável por configurar uma interface para fazer solicitações HTTP.A sessão encapsula um conjunto de conexões que suportam keepalives por padrão.

* `connector`: Conector personalizado para camada de transporte de solicitações.
* `loop`: Loop de eventos para execução de tarefas assíncronas. ref [asyncio](https://docs.python.org/3/library/asyncio-eventloop.html).
* `cookies`: Cookies para compartilhação entre várias solicitações.
* `headers`: Cabeçalhos padrão para todas as solicitações de sessão.
* `skip_auto_headers`: Conjunto de cabeçalhos HTTP para os quais a geração automática deve ser ignorada.
* `auth`: Tupla contendo `(user, pass)` para autenticação padrão para todas solicitações.
* `cookie_jar`: Passar o processamento de cookies ao aiohttp.DummyCookieJarinstância para a sessão do cliente. [ref](https://docs.aiohttp.org/en/stable/client_advanced.html#dummy-cookie-jar).
* `conn_timeout`: The number of [pipelined requests](https://en.wikipedia.org/wiki/HTTP_pipelining) for each connection. Will cause the `Client` API to throw when greater than 1. _OPTIONAL_ default: `1`.
* `timeout`: Tempo limite para operações de IO utilizados pelo cliente.
* `raise_for_status`: Levantar exceção http para status diferente de 200 em todas solicitações configuradas para o cliente.
* `connector_owner`: Indica se o conector deve ser fechado no fechamento da sessão.
* `auto_decompress`: A resposta do corpo deve ser descompactada automaticamente.
* `read_bufsize`: Tamanho máximo do buffer de leitura permitido por solicitação.
* `requote_redirect_url`: Permitir recotação de URL para URLs de redirecionamento.
* `trust_env`: Obter proxies informações de HTTP_PROXY/ https_proxy variáveis de ambiente se o parâmetro for verdadeiro.
* `trace_configs`: Uma lista de instâncias de TraceConfig's usadas para rastreamento de cliente. 

### Response (AsyncHTTPResponse)

A Fast-Http usa um objeto de resposta padrão `ClientResponse` utilizado pelo cliente aiohttp. ref [ClientResponse](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse), realizando algumas tratativas para usabilidade do mesmo.

* `request`: Objeto de solicitação HTTPRequest utilizado pelo Fast-HTTP. Cont
* `content_text`: Conteúdo de texto retornado pela solicitação. A mesma é autodecodificada com base no tipo de conteúdo.
* `version`: Versão da resposta.
* `status`: Código de status HTTP de resposta.
* `reason`: Razão status HTTP de resposta.
* `method`: Método utilizado na solicitação HTTP.
* `ok`: Representação booleana do código de status HTTP.  
* `url`:  Url utilizada na solicitação.
* `real_url`: URL não modificado da solicitação com fragmento de URL não removido ( URL).
* `connection`: [Connection]() usado para lidar com a resposta.
* `content`:  Conteúdo [StreamReader](https://docs.aiohttp.org/en/stable/streams.html#aiohttp.StreamReader) de resposta. 
* `cookies`:  Cookies de resposta HTTP (cabeçalho Set-Cookie HTTP, [SimpleCookie](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie).
* `headers`:  Cabeçalhos de resposta HTTP  (Instância de [CIMultiDictProxy.](https://multidict.readthedocs.io/en/stable/multidict.html#multidict.CIMultiDictProxy)).
* `raw_headers`: Cabeçalhos de resposta HTTP não modificados como bytes não convertidos, uma sequência de pares.(key, value)
* `links`: Cabeçalho HTTP do link analisado em um [CIMultiDictProxy.](https://multidict.readthedocs.io/en/stable/multidict.html#multidict.MultiDictProxy).
* `content_type`: Especificação do conteúdo retornado por parte do cabeçalho `Content-Type`.
* `charset`: Especificação da codificação do conteúdo restornado na solicitação
* `history`: Uma sequência de objetos HTTPHistory contendo instâncias de `ClientResponse` das solicitações anteriores (a solicitação mais antiga primeiro) se houver redirecionamentos, caso contrário, uma sequência vazia.
* `request_info`: Um namedtuple com URL de solicitação e cabeçalhos de `ClientRequest` objeto, [aiohttp.RequestInfoinstância](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.RequestInfo). 
* `release`:  Libera um obketo de resposta quando a carga é finalizada.
                               
---
  
## Benchmark Tool
A biblioteca possuí uma ferramenta para benchmarking suportando HTTP/1.0/1.1 escrita em python, com suporte para pipelining HTTP e HTTPS.


### HTTPBenchmark 

A ferramenta utiliza o cliente assincrono Fast-HTTP enviando blocos de solicitações a fim de balancear melhor as pipelines, podendo simular solicitações longas, utilizando recursos internos promovidos pela [aiohttp](https://docs.aiohttp.org/en/stable/) e pela própria Fast-HTTP.

#### Recursos Disponíveis

* [Balancemento de cargas]()
* [Auto Binding Utilizando Interface de Rêdes](#usage)
* [Distruibuição Controlada com algoritimo de Round-robin](#usage)
* [Pool de proxies controlados](#api)
* [Limpeza de cache DNS](#api)
* [Testes automatizados via linha de comando](#acknowledgements)
* [Arquivo de configuração manual](#acknowledgements)
* [Geração de statísticas HTTP](#acknowledgements)
 
## Utilização
### Command Line

```
Fast-HTTP [options] [http[s]://]hostname[:port]/path

positional arguments:
  url                   uRL

optional arguments:
  -h, --help            show this help message and exit
  -rpd MAX_REQUESTS_PER_DOMAIN, --max_requests_per_domain MAX_REQUESTS_PER_DOMAIN
                        Number of requests per domain
  -rpi MAX_REQUESTS_PER_IP, --max_requests_per_ip MAX_REQUESTS_PER_IP
                        Number of requests per ip
  -d MAX_DELAY, --max_delay MAX_DELAY
                        Maximum delay on request
  -s START_DELAY, --start_delay START_DELAY
                        Delay at the start of the request
  -sd SOCK_DELAY, --sock_delay SOCK_DELAY
                        Delay on socket request
  -rd READ_DELAY, --read_delay READ_DELAY
                        Delay for reading request
  -T TELNET, --telnet TELNET
                        Telnet console (enabled by default)
  -R ROUNDROBIN, --roundrobin ROUNDROBIN
                        Distribute http requests via network interface
  -c CONCURRENT, --concurrent CONCURRENT
                        Number of simultaneous requests
  -b BLOCK, --block BLOCK
                        Number of request blocks
  -t TIMEOUT, --timeout TIMEOUT
                        Number of request blocks
  -B BIND_ADDRESS, --bind_address BIND_ADDRESS
                        Address to bind to when making outgoing connections
  -p POSTDATA, --postdata POSTDATA
                        data to be sent via post
  -H HEADER, --header HEADER
                        add header line
  -C COOKIE, --cookie COOKIE
                        add cookie line
  -P PROXY, --proxy PROXY
                        Proxyserver and port number proxy:server
  -S VERIFY_SSL, --verify_ssl VERIFY_SSL
                        Disable SSL ceertificate
  -E CERTFILE, --certfile CERTFILE
                        Specify optional client certificate chain and private key
```
## Testando os limites

## Performance

Para tornar mais fácil, vamos começar com o básico - simples HTTP hello world - apenas fazendo GET e obtendo uma única resposta HTTP.

```
Fast-HTTP Versão 1.0
Benchmarking 0.0.0.0:8000

10000 requests divided into 417 blocks with 24 simultaneous requests
.....
40/417 blocks completed with 1000 requests
80/417 blocks completed with 960 requests
120/417 blocks completed with 960 requests
160/417 blocks completed with 960 requests
200/417 blocks completed with 960 requests
.....

Server : cloudflare | 
Host: 0.0.0.0 | Port: 8000
Protocol : HTTP 
SSL/TLS : TLSv1.1 
Chipers : , ECDHE-ECDSA-CHACHA20-POLY1305, 256, 256
Name server TLS: 0.0.0.0
Path: /test
Document Size: 3 bytes

Concurrent requests: 24
Benchmark time: 12,077 seconds
Completed Requests: 10.000
Failed Requests: 0
Content Buffer Size: 30000 Byte's / 0.03 Mega's

Average requests per second: 959,53 / sec (average)
Time per Request: 0,0027 [ms] (average on all simultaneous requests)
Transfer rate: 01,02 [Kbytes / s] received
Tempos de conexão (ms) mínimo médio [+/- dp] mediano máximo

Percentage of requests fulfilled within a given time (ms)
  1 - 50% 954
  2 - 66% 948
  3 - 75% 972
  4 - 80% 948
  5 - 90% 989
  6 - 95% 1190
  7 - 98% 1010
  8 - 99% 1749
  9 - 100% 31895 (solicitação mais longa)
```                 

### Programmatically Examples

##### HTTPRequest

```pycon
from fasthttp.HTTPClient import HTTPRequest

request = HTTPRequest(url="https://www.python.org/", method='get')
```

##### AsyncSession
```pycon
from fasthttp.HTTPClient import AsyncSession

async with ClientSession() as client:    
    ......  await implementation     
```

##### AssyncHTTPClient
```pycon
from fasthttp.HTTPClient import AssyncHTTPClient

client = AssyncHTTPClient()
response = client.get("https://www.python.org/")
```

#### HTTPBenchmark   
Classe responsável por realizar solicitações simulataneas.

```pycon
>>> from Benchmark import HTTPBenchmark
>>> 
>>> benchmark = HTTPBenchmark(method='get', concurrent_requests=24, 417)
>>> responses = benchmark.start()
>>>
>>> responses.total_time
13.9957 s
>>>
>>> responses.sucess
10008 
>>> responses.downloaded_content
130M
>>> 
>>> responses
< FastHTTP [Benchmark(success=10008, total_time=13.995]>
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