"""Instruções:
Pegar a lista com os Ids dos mineradores. Essa lista tem um ano de mineração. 
Dividir a lista em meses: 1/12 
Escolher o mes do seu aniversário
Gerar o grafico com o poder computacional de cada minerador por dia
Determinar o mais poderoso(MP) do mes
Contar as minerações em sequencia do MP
Gerar 1000 permutações da lista e contar as minerações em sequencia do MP em cada permutação
Determinar a posição do MP nesta lista de 1000 (isso é o pvalue) <======

Entregar relatorio em PDF com resultados e o codigo fonte
"""
import numpy as np
import matplotlib.pyplot as plt

#faz a leitura da lista
def read_npy(path):
    array = []
    with open(path, 'rb') as minersFile:
        array = np.load(minersFile)
    print(f'Lido: {path}')
    return array

#contabiliza o numero de blocos de cada minerador (array[x])
def block_counter(array, startPoint, endPoint):
    mined = dict()
    for x in range(startPoint, endPoint):
        if array[x] not in mined:
            mined[array[x]] = 1
        else:
            mined[array[x]] += 1
    return mined

#cria o grafico de blocos minerados
def plot_blocks(mined, filename):
    miners = list(mined.keys())
    blocks = list(mined.values())
    plt.bar(miners, blocks, width=0.2)
    plt.ylabel('blocos minerados')
    plt.xlabel('minerador')
    plt.xticks(miners, fontsize=7, rotation=40)
    plt.yticks(blocks, fontsize=7)
    plt.title(f'{filename}')
    plt.savefig(f'{filename}.png')
    plt.close('all')

#gera os graficos de determinado mes (inicio)
def generate_graphs(array, inicio, blocosPorDia):
    fim = inicio + blocosPorDia
    for i in range(30):
        mined = block_counter(array, inicio, fim)
        plot_blocks(mined, f'dia_{i+1}')
        inicio += blocosPorDia
        fim += blocosPorDia
        print(f'dia {i+1} criado.')

#contabiliza o numero de sequencias do mp
def mp_sequence(array, mp, inicio, mensal):
    sequencia = 0
    for i in range(inicio, inicio+mensal):
        if array[i] == mp:
            if array[i+1] == mp:
                sequencia += 1
    return sequencia

#realiza permutacoes na lista e contabiliza as sequencias em um txt
def permute_and_count(array, vezes, mp, inicio, mensal):
    with open('permutacoesMp.txt', 'w') as txt:
        for x in range(vezes):
            np.random.shuffle(array)
            seq = mp_sequence(array, mp, inicio, mensal)
            txt.write(f'permutacao {x}: {seq} sequencias do mp {mp}')
            txt.write('\n')

array = read_npy("block_integer_array.npy")
mensal = int(array.size / 12)
setembro = mensal * 9
blocosPorDia = int(mensal / 30)
print(f'blocos mensais: {mensal}; Setembro: {setembro}; Blocos/dia: {blocosPorDia}')
#generate_graphs(array, setembro, blocosPorDia) // setembro teve o minerador 2 Mp
#seq = mp_sequence(array, 2, setembro, mensal) # 98 sequencias no minerador 2
print(f'sequencia do MP: {seq}')
#permute_and_count(array, 1000, 2, setembro, mensal)