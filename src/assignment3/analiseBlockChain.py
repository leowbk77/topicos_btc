"""Instruções
Utilizando a API do blockchain.info (https://www.blockchain.com/explorer/api/blockchain_api) desenvolva um script para:


Pegar o último bloco da blockchain
Encontrar a transação de Coinbase
Listar os endereços que estão recebendo os Bitcoins minerados + taxas
Imprimir a taxa paga por cada transacao do bloco
Impimir o numero de entradas e o número de saidas de cada transacao
"""
import requests
import time

latestBlockEndPoint = 'https://blockchain.info/latestblock'
blockInfoEndPoint = 'https://blockchain.info/rawblock/'

# Obtém o hash do bloco mais recente
def find_latest_block_hash():
    with requests.get(latestBlockEndPoint) as request:
        if request.ok:
            data = request.json()
            print('Request latest block: OK')
        else:
            print('Request latest block: ERRO')
        return data["hash"]

# Obtém o JSON de determinado bloco
def block_info(hash):
    endPoint = blockInfoEndPoint + hash
    with requests.get(endPoint) as request:
        if request.ok:
            data = request.json()
            print('Request block info: OK')
        else:
            print('Request block info: ERRO')
        return data

# Retorna a transação inicial do bloco
def get_coinbase(block):
    return block["tx"][0]

# Escreve txt com as infos coletadas do bloco
def to_file(content, fileName):
    with open(fileName, "w") as file:
        file.write('\n'.join(content))

# Remove os enderecos duplicados da lista de enderecos
def clear_adresses(adressList):
    dic = dict.fromkeys(adressList, "temp")
    return list(dic.keys())

# Obtem os endereços de saída e as taxas de cada transação
def get_out_adresses_and_tx_fees(block):
    outputAdresses = list()
    txFees = list()
    for transaction in block["tx"]:
        txFees.append(transaction["fee"])
        for output in transaction["out"]:
            if 'addr' in output.keys():
                outputAdresses.append(output["addr"])
    to_file(clear_adresses(outputAdresses), "enderecos.txt")
    to_file(txFees, "taxas.txt")

print('Encontrando hash do bloco mais recente...')
latestBlockHash = find_latest_block_hash()
print('delay: 5 sec...')
time.sleep(5)
latestBlockJson = block_info(latestBlockHash)
print('Coinbase:')
print(get_coinbase(latestBlockJson))
print('Escrevendo arquivos...')
get_out_adresses_and_tx_fees(latestBlockJson)