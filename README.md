# Fast-HTTP
Aplicação em python utilizando aiohttp e japronto para realização de testes de performance http.

Todos testes foram realizados sobre a api de teste utilizando japronto com 200 conexões abertas. A api "hello_world.py" se encontra na raiz do projeto. Para realizar os testes dos exemplos abaixo é necessário iniciar o micro server.

![Web-Trader Block Diagram](https://github.com/MarcosVs98/Fast-HTTP/blob/main/example.png)

### Exemplo utilizando HTTPRequest

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