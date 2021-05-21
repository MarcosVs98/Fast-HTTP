"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
*                                                                      *
************************************************************************

Usage: ab [options] [http[s]://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make at a time
    -t timelimit    Seconds to max. to spend on benchmarking
                    This implies -n 50000
    -s timeout      Seconds to max. wait for each response
                    Default is 30 seconds
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -B address      Address to bind to when making outgoing connections
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header to use for POST/PUT data, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -v verbosity    How much troubleshooting info to print
    -w              Print out results in HTML tables
    -i              Use HEAD instead of GET
    -x attributes   String to insert as table attributes
    -y attributes   String to insert as tr attributes
    -z attributes   String to insert as td or th attributes
    -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
    -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                    Inserted after all normal header lines. (repeatable)
    -A attribute    Add Basic WWW Authentication, the attributes
                    are a colon separated username and password.
    -P attribute    Add Basic Proxy Authentication, the attributes
                    are a colon separated username and password.
    -X proxy:port   Proxyserver and port number to use
    -V              Print version number and exit
    -k              Use HTTP KeepAlive feature
    -d              Do not show percentiles served table.
    -S              Do not show confidence estimators and warnings.
    -q              Do not show progress when doing more than 150 requests
    -l              Accept variable document length (use this for dynamic pages)
    -g filename     Output collected data to gnuplot format file.
    -e filename     Output CSV file with percentages served
    -r              Don't exit on socket receive errors.
    -m method       Method name
    -h              Display usage information (this message)
    -I              Disable TLS Server Name Indication (SNI) extension
    -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
    -f protocol     Specify SSL/TLS protocol
                    (SSL2, TLS1, TLS1.1, TLS1.2 or ALL)
    -E certfile     Specify optional client certificate chain and private key


Portugues)

	Uso: ab [opções] [http [s]: //] nome do host [: porta] / caminho
	As opções são:
    -n solicitações Número de solicitações a serem realizadas
    -c simultaneidade Número de várias solicitações a serem feitas ao mesmo tempo
    -t timelimit Segundos para máx. gastar em benchmarking
                    Isso implica -n 50000
    -s timeout Segundos para max. espere por cada resposta
                    O padrão é 30 segundos
    -b windowsize Tamanho do buffer de envio / recebimento TCP, em bytes
    -B endereço Endereço para vincular ao fazer conexões de saída
    -p postfile Arquivo contendo dados para POST. Lembre-se também de definir -T
    -u putfile Arquivo contendo dados para PUT. Lembre-se também de definir -T
    -T content-type Cabeçalho de tipo de conteúdo a ser usado para dados POST / PUT, por exemplo.
    'application / x-www-form-urlencoded'
                    O padrão é 'text / plain'
    -v verbosity Quantas informações de solução de problemas devem ser impressas
    -w Imprime resultados em tabelas HTML
    -i Usa HEAD em vez de GET
    -x attribute String para inserir como atributos de tabela
    -y atributos String para inserir como atributos tr
    -z atributos String a ser inserida como td ou th atributos
    -C atributo Adicionar cookie, por exemplo. 'Apache = 1234'. (Repetivel)
    -H attribute Adiciona linha de cabeçalho arbitrária, por exemplo. 'Aceitar Codificação: gzip'
                    Inserido após todas as linhas de cabeçalho normais. (Repetivel)
    - Um atributo Adicionar Autenticação WWW Básica, os atributos
                    são um nome de usuário e uma senha separados por dois pontos.
    -P attribute Add Basic Proxy Authentication, the attribute
                    são um nome de usuário e uma senha separados por dois pontos.
    -X proxy: porta Proxyserver e número da porta a ser usado
    -V Imprime o número da versão e sai
    -k Usa o recurso HTTP KeepAlive
    -d Não mostra a tabela de percentis servidos.
    -S Não mostra estimadores de confiança e avisos.
    -q Não mostra o progresso ao fazer mais de 150 solicitações
    -l Aceita comprimento variável do documento (use para páginas dinâmicas)
    -g nome do arquivo Dados coletados de saída para o arquivo de formato gnuplot.
    -e nome do arquivo Arquivo CSV de saída com porcentagens servidas
    -r Não sai em erros de recebimento de soquete.
    -m método Nome do método
    -h Exibir informações de uso (esta mensagem)
    -I Desativar extensão TLS Server Name Indication (SNI)
    -Z ciphersuite Especifique o conjunto de cifras SSL / TLS (consulte cifras openssl)
    -f protocol Especifica o protocolo SSL / TLS
                    (SSL2, TLS1, TLS1.1, TLS1.2 ou ALL)
    -E certfile Especificar cadeia de certificado de cliente opcional e chave privada
"""


# end-of-file