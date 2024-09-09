'''Instruções
Clusterizar o endereço: 1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj
Análise econômica do cluster:
Historico do saldo
GINI das transacoes
Benford das transacoes
'''
import json
import glob

# Obtém os endereços de inputs das transações de cada endereço (arquivo)
# se o endereço (arquivo) aparece na lista então adiciona ao cluster
def to_cluster(fileList: list[str]):
    toCluster = {}
    for jsonFile in fileList:
        with open(jsonFile, 'r') as fileData:
            data = json.load(fileData)
            toCluster[data['address']] = []
            for tx in data['txs']:
                inputAddresses = [i['prev_out']['addr'] for i in tx['inputs']]
                if data['address'] in inputAddresses:
                    toCluster[data['address']].append(inputAddresses)
    return toCluster

def intersection(addresses1, addresses2):
    for address in addresses1:
        if address in addresses2:
            return True
    return False

def cluster(toCluster: dict):
    addresses = toCluster.keys()
    for address in addresses:
        clusters = []
        for tx in toCluster[address]:
            c = []
            for i in range(len(clusters)):
                if intersection(clusters[i], tx):
                    c.append(i)
            if len(c) == 0:
                clusters.append(tx)
            else:
                x = c[0]
                del c[0]
                clusters[x].extend(tx)
                for i in c:
                    clusters[x].extend(clusters[i])
                clusters[x] = list(set(clusters[x]))
        print('-------------------------------')
        print(address)
        if (len(clusters) == 1 and len(clusters[0]) < 10):
            print(set(clusters[0]))
        else:
            print(len(clusters[0]))
        if address == '1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj':
            result = clusters[0]
    return result

def firstD(i):
    i = int(i)
    while i >= 10:
        i = i // 10
    return i

def gini(values):
    valuesSorted = sorted(values)
    n = len(values)
    cumulativeSum = sum((i+1)*val for i, val in enumerate(valuesSorted))
    total = sum(valuesSorted)
    if total == 0:
        return 0
    return 1 - (2 * cumulativeSum) / (n * total) + (1/n)

def benford(values):
    h=[0]*9
    for i in values:
        with open(f'./rawaddr/{i}.json') as jsonFile:
            data = json.load(jsonFile)
            for i in range(1, data['n_tx']):
                valortx = sum([o['value'] for o in data['txs'][i]['out']])
                h[firstD(valortx)-1] = h[firstD(valortx)-1] + 1
            print(h)

def analise(cluster):
    address = '1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj'
    with open(f'./rawaddr/{address}.json', 'r') as jsonFile:
        data = json.load(jsonFile)

    inputValues = [] # valores que foram enviados
    outputValues = [] # valores que foram recebidos

    for tx in data['txs']:
        if tx['result'] < 0:
            inputValues.append(tx['result'])
        else:
            outputValues.append(tx['result'])

    print('-----Histórico--------')
    print('VALORES ENVIADOS:')
    print(inputValues)
    print('VALORES RECEBIDOS:')
    print(outputValues)
    print('====================GINI====================')
    print(gini(outputValues))
    print('===================BENFORD==================')
    benford(cluster)

toCluster = to_cluster(glob.glob('./rawaddr/*.json'))
analise(cluster(toCluster))