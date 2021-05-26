'''
from japronto import Application


def hello(request):
    return request.Response(text='H')


app = Application()

r = app.router
r.add_route('/', hello, method='GET')


app.run(port=9000, worker_num=200, debug=True)
'''




# end-of-file

"""
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking api.myip.com (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        cloudflare
Server Hostname:        api.myip.com
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-ECDSA-CHACHA20-POLY1305,256,256
Server Temp Key:        X25519 253 bits
TLS Server Name:        api.myip.com

Document Path:          /
Document Length:        52 bytes

Concurrency Level:      24
Time taken for tests:   148.077 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      10314014 bytes
HTML transferred:       520000 bytes
Requests per second:    67.53 [#/sec] (mean)
Time per request:       355.384 [ms] (mean)
Time per request:       14.808 [ms] (mean, across all concurrent requests)
Transfer rate:          68.02 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:       89  194 1436.5    112   31739
Processing:   144  160  26.9    157     908
Waiting:      141  157  26.9    154     904
Total:        242  354 1436.7    269   31895

Percentage of the requests served within a certain time (ms)
  50%    269
  66%    273
  75%    275
  80%    277
  90%    282
  95%    287
  98%    300
  99%    604
 100%  31895 (longest request)



Este é o ApacheBench, Versão 2.3 <$ Revisão: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/

Licenciado para The Apache Software Foundation, http://www.apache.org/

Fast-HTTP Versão 1.0
Benchmarking api.myip.com

10000 requests divided into 417 blocks with 24 simultaneous requests

.....
40/417 blocks completed with 960 requests
80/417 blocks completed with 960 requests
120/417 blocks completed with 960 requests
160/417 blocks completed with 960 requests
200/417 blocks completed with 960 requests
240/417 blocks completed with 960 requests
280/417 blocks completed with 960 requests
320/417 blocks completed with 960 requests
360/417 blocks completed with 960 requests
400/417 blocks completed with 960 requests
417/417 blocks completed with 408 requests


Software de servidor: cloudflare
Nome do host do servidor: api.myip.com
Porta do servidor: 443
Protocolo SSL / TLS: TLSv1.2, ECDHE-ECDSA-CHACHA20-POLY1305,256,256
Chave temporária do servidor: X25519 253 bits
Nome do servidor TLS: api.myip.com
Caminho do documento: /
Comprimento do documento: 52 bytes

Nível de simultaneidade: 24
Tempo gasto para testes: 148,077 segundos
Pedidos completos: 10.000
Pedidos com falha: 0
Total transferido: 10314014 bytes
HTML transferido: 5.20000 bytes

Solicitações por segundo: 67,53 [# / seg] (média)
Tempo por solicitação: 355,384 [ms] (média)
Tempo por solicitação: 14,808 [ms] (média, em todas as solicitações simultâneas)
Taxa de transferência: 68,02 [Kbytes / s] recebidos
Tempos de conexão (ms)
              mínimo médio [+/- dp] mediano máximo
Conecte-se: 89 194 1436,5 112 31739
Processamento: 144 160 26,9 157 908
Em espera: 141 157 26,9 154 904
Total: 242 354 1436,7 269 31895
Porcentagem das solicitações atendidas dentro de um determinado tempo (ms)
  50% 269
  66% 273
  75% 275
  80% 277
  90% 282
  95% 287
  98% 300
  99% 604
 100% 31895 (solicitação mais longa)

aiohttp.client_exceptions.ClientPayloadError:
"""
