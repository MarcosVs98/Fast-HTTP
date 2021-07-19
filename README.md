<div align="center"><img src="img/fasthttp-logan.png" height="300px"/></div>

<h2 align="center">Python library for making asynchronous HTTP requests.</h1>


Fast-HTTP is a library packaged with an asynchronous HTTP client, which allows you to parallelize http requests in order to
optimize and improve persistence with the target server. All this because the HTTP protocol offers pipelining,
allowing multiple hits to be sent on the same connection without waiting for responses.
blocked or closed while the HTTP server responds.

### Async in Python
Become an asynchronous function/method using the keyword "async" before the definition and also using another word
reserved called "await" in the implementation, so you can know to expect something. 

### Cliente HTTP

Simple example of using HTTP client.
```pycon
>>> from fasthttp.HTTPClient import AssyncHTTPClient
>>>
>>> client = AssyncHTTPClient()
>>> response = client.get("https://www.python.org/")
>>> response 
<FHTTP Response [200 OK]>
>>>
```

## Installation

```
python setup.py install
```

### Cloning the repository
```
$ git clone https://github.com/MarcosVs98/Fast-HTTP.git
```

## Parameters

The application's base parameterization was based on the parameters already used by the core library [aiohttp](https://docs.aiohttp.org/en/stable/) used in this project.

For shipping control, the parameters were stored in specific data structures using modulo-level decorators from [dataclasses](https://docs.python.org/3/library/dataclasses.html).

### Resquest (AsyncHTTPRequest)

Data structure responsible for encapsulating request data. 

* `url`: Required attribute for AsyncHTTPClient instance. [ref](https://pt.wikipedia.org/wiki/URI)
* `method`: Request method responsible for indicating the action to be performed for a given resource. [ref](https://pt.wikipedia.org/wiki/Hypertext_Transfer_Protocol)
* `headers`: Addition of arbitrary header. Headers containing more information about the resource to be obtained or about the customer. [ref](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields)
* `timeout`: Maximum time in seconds to wait for http response.
* `postdata`: Content to be sent to the target server.
* `http_version`: http version to use. Available HTTP/1.0 and 1.1.
* `auth_user`: Login for client authentication.
* `auth_pass`: Password for client authentication.
* `allow_redirects`: http client, allows redirection by server.
* `redirects`: Maximum number of redirects allowed.
* `proxy_host`: Login for client authentication using proxy.
* `proxy_pass`: Password for client authentication using proxy.
* `outbound_address`: IP address used for outbound. By default it is set to `0.0.0.0` .
* `sslcontext`: Certificate file address for SSL context creation.
* `proxy_headers`: Addition of arbitrary header. Headers containing more information about the resource to be obtained or about the client itself using a proxy.
* `raise_for_status`: Raise exception for status codes other than 200.

### Session (AsyncSession)
Data structure responsible for configuring an interface to make HTTP requests. The session encapsulates a set of connections that support keepalives by default.

* `connector`: Custom connector for request transport layer.
* `loop`: Event loop for running asynchronous tasks. ref [asyncio](https://docs.python.org/3/library/asyncio-eventloop.html).
* `cookies`: Cookies for sharing across multiple requests.
* `headers`: Default headers for all session requests.
* `skip_auto_headers`: Set of HTTP headers for which auto generation should be skipped.
* `auth`: Tuple containing `(user, pass)` for default authentication for all requests.
* `cookie_jar`: Pass cookie processing to aiohttp.DummyCookie Jar instance for the client session. [ref](https://docs.aiohttp.org/en/stable/client_advanced.html#dummy-cookie-jar).
* `conn_timeout`: The number of [pipelined requests](https://en.wikipedia.org/wiki/HTTP_pipelining) for each connection. Will cause the `Client` API to throw when greater than 1. _OPTIONAL_ default: `1`.
* `timeout`: Timeout for IO operations used by the client.
* `raise_for_status`: Raise http exception to status other than 200 on all requests configured for the client.
* `connector_owner`: Indicates whether the connector should be closed on session close.
* `auto_decompress`: The body's response should be decompressed automatically.
* `read_bufsize`: Maximum read buffer size allowed per request.
* `requote_redirect_url`: Allow URL requote for redirect URLs.
* `trust_env`: Get proxies information from HTTP_PROXY/ https_proxy environment variables if parameter is true.
* `trace_configs`: A list of TraceConfig's instances used for client tracing.

#### TCP Conector (AsyncTCPConnector)

Data structure responsible for configuring the connector interface.

* `ssl`: SSL validation mode.
* `fingerprint`: Fingerprint helper for checking SSL certificates by SHA256 digest. 
* `use_dns_cache`: Use internal cache for DNS lookups.
* `ttl_dns_cache`: Expire after some seconds the DNS entries
* `family`: TCP socket family
* `ssl_context`: Specify optional client certificate chain and private key [connection]
* `local_addr`: Tuple of (local_host, local_port) used to [connection]
* `resolver`: Custom resolvers allow you to resolve hostnames
* `force_close`: Close underlying sockets after connection releasing (optional).
* `limit`: Total number simultaneous connections
* `limit_per_host`: Limit simultaneous connections to the same endpoint
* `enable_cleanup_closed`: Aborts underlining transport after 2 seconds. It is off by default.

 
### Response (AsyncHTTPResponse)

Fast-Http uses a default `ClientResponse` response object used by the aiohttp client. ref [ClientResponse](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponse), carrying out some negotiations for its usability.

* `request`: HTTPRequest request object used by Fast-HTTP. Count
* `content_text`: Text content returned by the request. It is self-decoded based on content type.
* `version`: Version of the response.
* `status`: HTTP response status code.
* `reason`: HTTP status response reason.
* `method`: Method used in HTTP request.
* `ok`: Boolean representation of the HTTP status code.
* `url`: Url used in the request.
* `real_url`: Unmodified request URL with unremoved URL fragment (URL).
* `connection`: [Connection]() used to handle the response.
* `content`: [StreamReader](https://docs.aiohttp.org/en/stable/streams.html#aiohttp.StreamReader) content of response.
* `cookies`: HTTP response cookies (Set-Cookie HTTP header, [SimpleCookie](https://docs.python.org/3/library/http.cookies.html#http.cookies.SimpleCookie).
* `headers`: HTTP response headers (Instance of [CIMultiDictProxy.](https://multidict.readthedocs.io/en/stable/multidict.html#multidict.CIMultiDictProxy)).
* `raw_headers`: Unmodified HTTP response headers as unconverted bytes, a sequence of pairs.(key, value)
* `links`: HTTP header of the link parsed in a [CIMultiDictProxy.](https://multidict.readthedocs.io/en/stable/multidict.html#multidict.MultiDictProxy).
* `content_type`: Specification of the content returned by the `Content-Type` header.
* `charset`: Specifying the encoding of content returned in the request
* `history`: A string of HTTPHistory objects containing instances of `ClientResponse` from previous requests (oldest request first) if there are redirects, otherwise an empty string.
* `request_info`: A namedtuple with request URL and `ClientRequest` object headers, [aiohttp.RequestInfoinstance](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.RequestInfo).
* `release`: Release a response object when the load is finished.                               
---
  
## Benchmark Tool
The library has a benchmarking tool supporting HTTP/1.0/1.1 written in python, with support for HTTP and HTTPS pipelining.


### HTTPBenchmark

 ![Web-Trader Block Diagram](https://github.com/MarcosVs98/Fast-HTTP/blob/main/img/example.png) 

The tool uses the Fast-HTTP asynchronous client sending request blocks in order to better balance the pipelines, being able to simulate long requests, using internal resources promoted by [aiohttp](https://docs.aiohttp.org/en/stable/) and by Fast-HTTP itself.
 
## Use
## Command Line

```
Fast-HTTP [options] [http[s]://]hostname[:port]/path

optional arguments:
  -h, --help            show this help message and exit

connector:
  -cs CONNECTOR_SSL, --connector_ssl CONNECTOR_SSL
                        SSL validation mode.
  -cf FINGERPRINT, --fingerprint FINGERPRINT
                        Fingerprint helper for checking SSL certificates by SHA256 digest.
  -cds USE_DNS_CACHE, --use_dns_cache USE_DNS_CACHE
                        use internal cache for DNS lookups
  -tt TTL_DNS_CACHE, --ttl_dns_cache TTL_DNS_CACHE
                        Expire after some seconds the DNS entries
  -fm FAMILY, --family FAMILY
                        TCP socket family
  -cE CONNECTOR_SSL_CONTEXT, --connector_ssl_context CONNECTOR_SSL_CONTEXT
                        Specify optional client certificate chain and private key [connection]
  -cA LOCAL_ADDR, --local_addr LOCAL_ADDR
                        Tuple of (local_host, local_port) used to [connection]
  -cR RESOLVER, --resolver RESOLVER
                        Custom resolvers allow you to resolve hostnames
  -cF FORCE_CLOSE, --force_close FORCE_CLOSE
                        close underlying sockets after connection releasing (optional).
  -cL LIMIT, --limit LIMIT
                        Total number simultaneous connections
  -cH LIMIT_PER_HOST, --limit_per_host LIMIT_PER_HOST
                        Limit simultaneous connections to the same endpoint
  -cC ENABLE_CLEANUP_CLOSED, --enable_cleanup_closed ENABLE_CLEANUP_CLOSED
                        Aborts underlining transport after 2 seconds. It is off by default.

session:
  -sC COOKIES, --cookies COOKIES
                        add cookie line
  -sH HEADERS, --headers HEADERS
                        add header line
  -sK SKIP_AUTO_HEADERS, --skip_auto_headers SKIP_AUTO_HEADERS
                        add header line
  -sAu AUTH, --auth AUTH
  -sV VERSION, --version VERSION
                        HTTP Version
  -sJ JSON_SERIALIZE, --json_serialize JSON_SERIALIZE
                        Python’s standard json module for serialization.
  -sM CONN_TIMEOUT, --conn_timeout CONN_TIMEOUT
                        add header line
  -sR RAISE_FOR_STATUS, --raise_for_status RAISE_FOR_STATUS
                        call raise for status for all answers not ok
  -sO CONNECTOR_OWNER, --connector_owner CONNECTOR_OWNER
                        Should connector be closed on session closing
  -sD AUTO_DECOMPRESS, --auto_decompress AUTO_DECOMPRESS
                        Should the body response be automatically decompressed
  -sB READ_BUFSIZE, --read_bufsize READ_BUFSIZE
                        Size of the read buffer
  -sQ REQUOTE_REDIRECT_URL, --requote_redirect_url REQUOTE_REDIRECT_URL
                        To disable re-quote system set requote_redirect_url attribute
  -sT TRUST_ENV, --trust_env TRUST_ENV
                        Get proxies information from HTTP_PROXY / HTTPS_PROXY environment variables
  -sF TRACE_CONFIGS, --trace_configs TRACE_CONFIGS
                        Get proxies information from HTTP_PROXY / HTTPS_PROXY environment variables

request:
  url                   URL
  -m METHOD, --method METHOD
                        HTTP method
  -ar ALLOW_REDIRECTS, --allow_redirects ALLOW_REDIRECTS
                        Allow redirects
  -mr REDIRECTS, --redirects REDIRECTS
                        Maximum number of redirects
  -k POSTDATA, --postdata POSTDATA
                        data to be sent via post
  -H HEADER, --header HEADER
                        add header line
  -PH PROXY_HEADERS, --proxy_headers PROXY_HEADERS
                        add proxy header line
  -pU PROXY_USER, --proxy_user PROXY_USER
                        Add Basic Proxy Authentication, [user]
  -pP PROXY_PASS, --proxy_pass PROXY_PASS
                        Add Basic Proxy Authentication, [pass]
  -S VERIFY_SSL, --verify_ssl VERIFY_SSL
                        Disable SSL ceertificate
  -E SSLCONTEXT, --sslcontext SSLCONTEXT
                        Specify optional client certificate chain and private key
  -X PROXY, --proxy PROXY
                        Proxyserver and port number proxy:server

benchmark:
  -T TELNET, --telnet TELNET
                        Telnet console (enabled by default)
  -lp LIMIT_PER_IP, --limit_per_ip LIMIT_PER_IP
                        Limit simultaneous connections to the same ip
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of simultaneous requests
  -b BLOCK, --block BLOCK
                        Number of request blocks
  -B OUTBOUND_ADDRESS, --outbound_address OUTBOUND_ADDRESS
                        Address to bind to when making outgoing connections
  -pp PUBLIC_PROXY, --public_proxy PUBLIC_PROXY
                        Public proxies list

timeout:
  -d TOTAL, --total TOTAL
                        Maximum delay on request [start]
  -s CONNECT, --connect CONNECT
                        Delay at the start of the request [connect]
  -sd SOCK_CONNECT, --sock_connect SOCK_CONNECT
                        Delay on socket request [socket]
  -rd SOCK_READ, --sock_read SOCK_READ
                        Delay for reading request [read]

```
## Testing the limits

## Performance

To make it easier, let's start with the basics - simple HTTP - just doing GET and getting a single HTTP response.

```
initializing benchmark...
Fast-HTTP Version 1.0.0 - Copyright (c) 2020 MarcosVs98
Benchmarking https://google.com.br/

10 requests divided into 1 blocks with 10 simultaneous requests.

* host: google.com.br 
* server: gws 
* method: GET 
* scheme : HTTPS 
* SSL/TLS : TLSv1.3 
* chipers TLS_AES_256_GCM_SHA384, TLSv1.3, 256
* name server TLS: google.com.br 
* path: / 
* document size: 112.89 KB's

* TCP connections: 100 
* máx. requests per hostname: 0 
* TTL dns cache: 300 
* concurrent requests: 10 
* qtd. request block: 1 

* total requests: 10 
* benchmark time: 0.25095 seconds
* success requests: 10
* failed requests: 0
* total buffer size: 1.10 MB's 
* average requests per second: 34 / sec (average)
* time per request: 0.029095 [ms] (average on all simultaneous requests)

```

Now using an internal address for a microservice - simple HTTP hello world - just doing GET and getting a single HTTP response.

```
initializing benchmark...
Fast-HTTP Version 1.0.0 - Copyright (c) 2020 MarcosVs98
Benchmarking http://0.0.0.0:9999

10000 requests divided into 25 blocks with 400 simultaneous requests.

* host: 0.0.0.0 
* method: GET 
* scheme : HTTP  
* name server TLS: 0.0.0.0:9999 
* path: / 
* document size: 11 bytes

* TCP connections: 100 
* máx. requests per hostname: 0 
* TTL dns cache: 300 
* concurrent requests: 25 
* qtd. request block: 400 

* total requests: 10000 
* benchmark time: 13.1065 seconds
* success requests: 10000
* failed requests: 0
* total buffer size: 0.11 MB's 
* average requests per second: 763 / sec (average)
* time per request: 0.0013106 [ms] (average on all simultaneous requests)

```                 

### Programmatically Examples

#### HTTPRequest

```pycon
from fasthttp.HTTPClient import HTTPRequest

request = HTTPRequest(url="https://www.python.org/", method='get')
```

#### AsyncSession
```pycon
from fasthttp.HTTPClient import AsyncSession

async with AsyncSession() as client:    
    ......  await implementation     
```

#### AssyncHTTPClient
```pycon
from fasthttp.HTTPClient import AssyncHTTPClient

client = AssyncHTTPClient()
response = client.get("https://www.python.org/")
```

#### HTTPBenchmark E1   
Class responsible for making simultaneous requests.

```pycon
>>> from fasthttp import HTTPBenchmark
>>> 
>>> benchmark = HTTPBenchmark(url='https://google.com.br/', method='get', concurrent_requests=1, concurrent_blocks=1)
>>> responses = benchmark.perform()
>>>
>>> responses.total_time
0.9957s
>>>, 
>>> responses.success
10
>>> 
>>> responses   
<FastHTTP-Benchmark[success=10, total_time=0.9957]>
>>> 
```

#### HTTPBenchmark E2

Model on the answer blocks.

```pycon
>>> from fasthttp import  HTTPBenchmark
>>> 
>>> with HTTPBenchmark(method='get', url=url, concurrent_requests=10, concurrent_blocks=3) as benchmark:
...     for n, resultados in enumerate(benchmark.blocks,1):
...         print(n, resultados)
1 <BlockResponse(sid=1-5b4e8305-1e60-4768-b0f9-2b811855d712)>
2 <BlockResponse(sid=2-dc9de4f2-7ea3-409f-96f3-29e149648724)>
3 <BlockResponse(sid=3-d4f1b244-8e99-4a64-9078-32c3507574e5)>
>>> 
```         
#### HTTPBenchmark E3

Model iterating over each response block.

```pycon
>>> from fasthttp import HTTPBenchmark
>>>
>>> with HTTPBenchmark(method='get', url=url, concurrent_requests=3, concurrent_blocks=3) as benchmark:
...     for n, resultados in enumerate(benchmark.blocks,1):
...		    print(n, resultados)
...
...		    for r in resultados.block:
... 			print(n, r)
1 <BlockResponse(sid=1-3bca286d-6eb7-4382-8c49-5da0edf019f3)>
1 <FHTTP Response [200 OK]>
1 <FHTTP Response [200 OK]>
1 <FHTTP Response [200 OK]>
2 <BlockResponse(sid=2-45631018-9a71-49d7-918b-cf29742eb71c)>
2 <FHTTP Response [200 OK]>
2 <FHTTP Response [200 OK]>
2 <FHTTP Response [200 OK]>
3 <BlockResponse(sid=3-61219706-c29b-4cf8-9483-501e60981d2f)>
3 <FHTTP Response [200 OK]>
3 <FHTTP Response [200 OK]>
3 <FHTTP Response [200 OK]>
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
