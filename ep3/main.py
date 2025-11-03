# -----------
# 0) DEPENDENCIAS E VARIAVEIS GLOBAIS
# -----------
from Compara import comp1, comp2, comp3, comp4
from math import log2
from time import time




# -----------
# 1) FUNCOES OBRIGATORIAS
# -----------

def ClassificaMerge(TAB, comp):
    
    # variavel geral
    tamanho_TAB = len(TAB)

    # variaveis para o primeiro loop
    tamanho_sublista = 1
    n_sublistas_integras = tamanho_TAB
    ha_sublista_quebrada = False
    tamanho_sublista_quebrada = 0
    fundir_sublista_quebrada = False

    while n_sublistas_integras > 0:
        tamanho_sublista *= 2
        n_sublistas_integras = tamanho_TAB // tamanho_sublista
        ha_sublista_quebrada = (tamanho_TAB % tamanho_sublista > 0)
        if ha_sublista_quebrada: 
            tamanho_sublista_quebrada = tamanho_TAB % tamanho_sublista
            fundir_sublista_quebrada = (tamanho_sublista_quebrada/(tamanho_sublista/2) > 1)
        for i in range(0, tamanho_TAB, tamanho_sublista):
            meio = i+tamanho_sublista//2
            try:
                intercalar(TAB[i:meio], TAB[meio:i+tamanho_sublista], TAB, i, comp)
            except IndexError:
                if fundir_sublista_quebrada:
                    intercalar(TAB[i:i+tamanho_sublista//2], TAB[i+tamanho_sublista//2:], TAB, i, comp)
    return None
        

        


def ClassificaQuick(TAB, comp):
    pass




# -----------
# 2) FUNCOES AUXILIARES
# -----------

def main():
    arquivo = input('Nome do arquivo de origem:')
    if arquivo == 'fim':
        quit()
    TAB = importarTAB(arquivo=arquivo)
    print()
    while True:
        metodo = input('Quick ou Merge (q ou m)? ')
        print()
        ordem = input('Ordem - comp1a4? ')
        print()
        t0 = time()
        despacho_metodo[metodo](TAB, despacho_comp[ordem])
        t1 = time()
        dt = t1 - t0
        imprimir(TAB, metodo=metodo, tempo=dt, ordem=ordem, n_linhas=100)
        print()

def importarTAB(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as a:
        TAB = [linha.strip().split(',') for linha in a.readlines()]
    return TAB

def intercalar(sublista1, sublista2, lista, inicio, comp):
    n, m = len(sublista1), len(sublista2)
    i, j, k = 0, 0, inicio
    while i < n and j < m:
        if comp(sublista1[i], sublista2[j]):
            lista[k] = sublista1[i]
            i = i + 1
        else:
            lista[k] = sublista2[j]
            j = j + 1
        # avança k
        k = k + 1
    while i < n:
        lista[k] = sublista1[i]
        i, k = i + 1, k + 1
    while j < m:
        lista[k] = sublista2[j]
        j, k = j + 1, k + 1

def imprimir(TAB, metodo, tempo, ordem, n_linhas):
    print(f'Tempo do {nome_metodo[metodo]}: {tempo}')
    print()
    print(f'{n_linhas} primeiros registros da tabela')
    print(f'Ordem: {descricao_comp[ordem]}')
    print()
    print(f"{'Indice':<8} {'Identidade':<15} {'Nome':<40} {'Data':<10}")
    for i in range(n_linhas):
        print(f'{i:<8} {TAB[i][0]:<15} {TAB[i][1]:<40} {TAB[i][2]:<10}')




# -----------
# 3) DICTS AUXILIARES
# -----------

despacho_metodo = {
    'm': ClassificaMerge,
    'q': ClassificaQuick
}

despacho_comp = {
    1: comp1,
    2: comp2,
    3: comp3,
    4: comp4
}

nome_metodo = {
    'm': 'Merge',
    'q': 'Quick'
}

descricao_comp = {
    1: 'cresc. por nome - cresc. por data - cresc. por id.',
    2: 'cresc. por nome - decresc. por data - cresc. por id.',
    3: 'decresc. por data - cresc. por nome - cresc. por id.',
    4: 'cresc. por id. - cresc. por data - cresc. por nome'
}


# -----------
# 4) PROGRAMA
# -----------
if __name__ == '__main__':
    from ep3.Compara import comp1, comp2, comp3, comp4    
    
    TAB = importarTAB('ep3/arq10000.txt')
    #def simpcomp(x,y):
    #    return x <= y
    #c = [4,5,2,3,8,1,10]
    #ClassificaMerge(c, simpcomp)
    #c
    ClassificaMerge(TAB, comp4)

    imprimir(TAB, 'q', 10, 4, 20)




