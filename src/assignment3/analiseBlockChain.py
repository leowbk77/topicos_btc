"""Instruções
Utilizando a API do blockchain.info (https://www.blockchain.com/explorer/api/blockchain_api) desenvolva um script para:


Pegar o último bloco da blockchain
Encontrar a transação de Coinbase
Listar os endereços que estão recebendo os Bitcoins minerados + taxas
Imprimir a taxa paga por cada transacao do bloco
Impimir o numero de entradas e o número de saidas de cada transacao
"""
import requests

latestBlockEndPoint = 'https://blockchain.info/latestblock'
blockInfoEndPoint = 'https://blockchain.info/rawblock/'

def find_latest_block():
    with requests.get(latestBlockEndPoint) as request:
        if request.ok:
            data = request.json()
            print('Request latest block: OK')
        else:
            print('Request latest block: Error')
        return data

def block_info(blockHash):
    endPoint = blockInfoEndPoint + blockHash
    with requests.get() as request:
        if request.ok:
            data = request.json()
            print('Request block info: OK')
        else:
            print('Request block info: ERROR')
        return data