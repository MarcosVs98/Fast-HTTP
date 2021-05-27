 # Fast-HTTP

Python library for making asynchronous HTTP requests.
 ![Web-Trader Block Diagram](https://github.com/MarcosVs98/Fast-HTTP/blob/main/example.png)

***

## Sobre
Fast-HTTP é uma biblioteca empacotada com um cliente HTTP assíncrono, que permite uma paralelização da execução, a fim 
de otimizar e melhorar a persistência com o servidor destino.Tudo isso porque o protocolo HTTP oferece pipelining, 
permitindo o envio de múltiplas ocorrências na mesma conexão sem esperar por respostas.Portanto, a chamada não é bloqueada ou fechada enquanto o servidor HTTP responde.

## Assincronicidade

As solicitações são totalmente síncronas.Isso bloqueia o cliente enquanto espera alguma resposta, tornando o programa   
lento. Fazer solicitações HTTP em encadeamentos é uma solução, porém encadeamentos têm uma sobrecarga e isso implica em paralelismo.

### Assincrono em Python
Se torna função/método assíncrono usando a palavra reservada async antes da definição e também utilizando outra palavra 
reservada chamada "await" na implementação, para que assim possa saber esperar por algo. 

## Benchmark Tool
A biblioteca possuí uma ferramenta para benchmarking suportando HTTP/1.0/1.1 escrita em python, com suporte para pipelining HTTP e HTTPS.

O HTTPBenchmark utiliza o cliente AsyncFastHTTP enviando blocos de solicitações a fim de usar o melhor das pipelines, podendo simular solicitações longas
 
## Testando os limites

## Performance

Para tornar mais fácil, vamos começar com o básico - simples HTTP hello world - apenas fazendo GET e obtendo uma única resposta HTTP.

***
   
## Requisitos
 - Python : Python >= 3.5
 
***
## Instalação

```
python setup.py install
```

#### Instalando via [GitHub](https://github.com/WebGlobal/Renova-Cookies.git)
```
$ git clone https://github.com/WebGlobal/Renova-Cookies.git
```

***
## Utilização

### Linha de Comando




```
                *****************************************************************
                *                       ┬────┬────┬───┬                         *
                *                       |    |    |   |                         *
                *                       |    QUEUE    |                         *
                *                       |    |    |   |                         *
                *                       └────└────└───┘                         *
                *                              ||                               *
                *                       ┬──────┘└───────┬                       *
                *                       | Request Block |                       *
                *                       └───────┬───────┘                       *
                *                               |                               *
                *      ┬────────────────────────└────────────────────────┬      *
                *      |        ┬───────────────┬───────────────┬        |      *
                *      |   ┬────└────┬     ┬────└────┬     ┬────└────┬   |      *
                *      |   |    |    |     |    |    |     |    |    |   |      *
                *      |   v    v    v     v    v    v     v    v    v   |      *
                *      |   ┬─────────┬     ┬─────────┬     ┬─────────┬   |      *
                *      |   | #target |     | #target |     | #target |   |      *
                *      |   └─────────┘     └─────────┘     └─────────┘   |      *
                *      |   |    |    |     |    |    |     |    |    |   |      *
                *      |   v    v    v     v    v    v     v    v    v   |      *
                *      |   ┬─────────┬     ┬─────────┬     ┬─────────┬   |      *
                *      |   |#Response|     |#Response|     |#Response|   |      *
                *      |   └─────────┘     └─────────┘     └─────────┘   |      *
                *      |   |    |    |     |    |    |     |    |    |   |      *
                *      |   v    v    v     v    v    v     v    v    v   |      *
                *      └───────────────────────┬┬────────────────────────┘      *
                *                              ||                               *
                *                    ┬─────────┘└──────────┬                    *
                *                    |    Response block   |                    *
                *                    └─────────────────────┘                    *
                *****************************************************************
```

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

### autocannon(opts[, cb])

Start autocannon against the given target.

* `opts`: Configuration options for the autocannon instance. This can have the following attributes. _REQUIRED_.
    * `url`: The given target. Can be http or https. More than one url is allowed, but it is recommended that the number of connections be an integer multiple of the url. _REQUIRED_.
    * `socketPath`: A path to a Unix Domain Socket or a Windows Named Pipe. A `url` is still required in order to send the correct Host header and path. _OPTIONAL_.
    * `workers`: Number of worker threads to use to fire requests.
    * `connections`: The number of concurrent connections. _OPTIONAL_ default: `10`.
    * `duration`: The number of seconds to run the autocannon. Can be a [timestring](https://www.npmjs.com/package/timestring). _OPTIONAL_ default: `10`.
    * `amount`: A `Number` stating the amount of requests to make before ending the test. This overrides duration and takes precedence, so the test won't end until the amount of requests needed to be completed are completed. _OPTIONAL_.
    * `timeout`: The number of seconds to wait for a response before . _OPTIONAL_ default: `10`.
    * `pipelining`: The number of [pipelined requests](https://en.wikipedia.org/wiki/HTTP_pipelining) for each connection. Will cause the `Client` API to throw when greater than 1. _OPTIONAL_ default: `1`.
    * `bailout`: The threshold of the number of errors when making the requests to the server before this instance bail's out. This instance will take all existing results so far and aggregate them into the results. If none passed here, the instance will ignore errors and never bail out. _OPTIONAL_ default: `undefined`.
    * `method`: The http method to use. _OPTIONAL_ `default: 'GET'`.
    * `title`: A `String` to be added to the results for identification. _OPTIONAL_ default: `undefined`.
    * `body`: A `String` or a `Buffer` containing the body of the request. Insert one or more randomly generated IDs into the body by including `[<id>]` where the randomly generated ID should be inserted (Must also set idReplacement to true). This can be useful in soak testing POST endpoints where one or more fields must be unique. Leave undefined for an empty body. _OPTIONAL_ default: `undefined`.
    * `form`: A `String` or an `Object` containing the multipart/form-data options or a path to the JSON file containing them
    * `headers`: An `Object` containing the headers of the request. _OPTIONAL_ default: `{}`.
    * `initialContext`: An object that you'd like to initialize your context with. Checkout [an example of initializing context](./samples/init-context.js). _OPTIONAL_
    * `setupClient`: A `Function` which will be passed the `Client` object for each connection to be made. This can be used to customise each individual connection headers and body using the API shown below. The changes you make to the client in this function will take precedence over the default `body` and `headers` you pass in here. There is an example of this in the samples folder. _OPTIONAL_ default: `function noop () {}`. When using `workers`, you need to supply a file path that default exports a function instead (Check out [workers](#workers) section for more details).
    * `maxConnectionRequests`: A `Number` stating the max requests to make per connection. `amount` takes precedence if both are set. _OPTIONAL_
    * `maxOverallRequests`: A `Number` stating the max requests to make overall. Can't be less than `connections`. `maxConnectionRequests` takes precedence if both are set. _OPTIONAL_
    * `connectionRate`: A `Number` stating the rate of requests to make per second from each individual connection. No rate limiting by default. _OPTIONAL_
    * `overallRate`: A `Number` stating the rate of requests to make per second from all connections. `connectionRate` takes precedence if both are set. No rate limiting by default. _OPTIONAL_
    * `ignoreCoordinatedOmission`: A `Boolean` which disable the correction of latencies to compensate the coordinated omission issue. Does not make sense when no rate of requests has been specified (`connectionRate` or `overallRate`). _OPTIONAL_ default: `false`.
    * `reconnectRate`: A `Number` which makes the individual connections disconnect and reconnect to the server whenever it has sent that number of requests. _OPTIONAL_
    * `requests`: An `Array` of `Object`s which represents the sequence of requests to make while benchmarking. Can be used in conjunction with the `body`, `headers` and `method` params above. Check the samples folder for an example of how this might be used. _OPTIONAL_. Contained objects can have these attributes:
       * `body`: When present, will override `opts.body`. _OPTIONAL_
       * `headers`: When present, will override `opts.headers`. _OPTIONAL_
       * `method`: When present, will override `opts.method`. _OPTIONAL_
       * `path`: When present, will override `opts.path`. _OPTIONAL_
       * `setupRequest`: A `Function` you may provide to mutate the raw `request` object, e.g. `request.method = 'GET'`. It takes `request` (Object) and `context` (Object) parameters, and must return the modified request. When it returns a falsey value, autocannon will restart from first request. When using `workers`, you need to supply a file path that default exports a function instead (Check out [workers](#workers) section for more details) _OPTIONAL_
       * `onResponse`: A `Function` you may provide to process the received response. It takes `status` (Number), `body` (String) `context` (Object) parameters and `headers` (Key-Value Object). When using `workers`, you need to supply a file path that default exports a function instead (Check out [workers](#workers) section for more details) _OPTIONAL_
    * `har`: an `Object` of parsed [HAR](https://w3c.github.io/web-performance/specs/HAR/Overview.html) content. Autocannon will extra and use `entries.request`: `requests`, `method`, `form` and `body` options will be ignored. _NOTE_: you must ensure that entries are targeting the same domain as `url` option. _OPTIONAL_
    * `idReplacement`: A `Boolean` which enables the replacement of `[<id>]` tags within the request body with a randomly generated ID, allowing for unique fields to be sent with requests. Check out [an example of programmatic usage](./samples/using-id-replacement.js) can be found in the samples. _OPTIONAL_ default: `false`
    * `forever`: A `Boolean` which allows you to setup an instance of autocannon that restarts indefinitely after emiting results with the `done` event. Useful for efficiently restarting your instance. To stop running forever, you must cause a `SIGINT` or call the `.stop()` function on your instance. _OPTIONAL_ default: `false`
    * `servername`: A `String` identifying the server name for the SNI (Server Name Indication) TLS extension. _OPTIONAL_ default: Defaults to the hostname of the URL when it is not an IP address.
    * `excludeErrorStats`: A `Boolean` which allows you to disable tracking non 2xx code responses in latency and bytes per second calculations. _OPTIONAL_ default: `false`.
    * `expectBody`: A `String` representing the expected response body. Each request whose response body is not equal to `expectBody`is counted in `mismatches`. If enabled, mismatches count towards bailout. _OPTIONAL_
    * `tlsOptions`: An `Object` that is passed into `tls.connect` call ([Full list of options](https://nodejs.org/api/tls.html#tls_tls_connect_port_host_options_callback)). Note: this only applies if your url is secure.
* `cb`: The callback which is called on completion of a benchmark. Takes the following params. _OPTIONAL_.
    * `err`: If there was an error encountered with the run.
    * `results`: The results of the run.

**Returns** an instance/event emitter for tracking progress, etc. If cb omitted, the return value can also be used as a Promise.

### Customizing sent requests

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