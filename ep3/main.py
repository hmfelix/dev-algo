# -----------
# 0) DEPENDENCIAS
# -----------
from Compara import comp1, comp2, comp3, comp4
from time import time




# -----------
# 1) FUNCOES OBRIGATORIAS
# -----------

def ClassificaMerge(TAB, comp_fn):
    """
    Reordena a lista TAB dada usando a função
    de comparação comp_fn e o algoritmo merge.
    Chama a função auxiliar intercalar,
    definida adiante, para executar a troca de
    ordem entre elementos.
    """
    # variavel geral
    tamanho_TAB = len(TAB)
    # variaveis para o primeiro loop
    tamanho_sublista = 1
    n_sublistas_integras = tamanho_TAB
    ha_sublista_quebrada = False
    tamanho_sublista_quebrada = 0
    fundir_sublista_quebrada = False
    # loop de classificacao
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
                intercalar(TAB[i:meio], TAB[meio:i+tamanho_sublista], TAB, i, comp_fn)
            except IndexError:
                if fundir_sublista_quebrada:
                    intercalar(TAB[i:i+tamanho_sublista//2], TAB[i+tamanho_sublista//2:], TAB, i, comp_fn)
    return None
        
def ClassificaQuick(TAB, comp_fn):
    """
    Reordena a lista TAB dada usando a função
    de comparação comp_fn e o algoritmo quick.
    Chama a função auxiliar particionar,
    definida adiante, para executar a troca de
    ordem entre elementos.
    (Implementação inspirada na versão dada
    em sala pelo professor, com adaptações.)
    """
    # pilha para viabilizar versao nao recursiva
    pilha = list()
    # primeira tupla de inicio e fim
    pilha.append((0, len(TAB) - 1))
    # loop de classificacao
    while len(pilha) > 0:
        inicio, fim = pilha.pop()
        if fim - inicio > 0:
            k = particionar(TAB, inicio, fim, comp_fn)
            pilha.append((inicio, k - 1))
            pilha.append((k + 1, fim))




# -----------
# 2) FUNCOES AUXILIARES
# -----------

def main():
    """
    Programa principal, seguindo o fluxo dado
    pelo enunciado.
    """
    print()
    # importacao inicial
    arquivo = input('Nome do arquivo de origem: ')
    if arquivo == 'fim': # condicao de saida
        quit()
    TAB = importarTAB(arquivo=arquivo)
    print()
    # comparacoes
    while True:
        # solicita metodo
        metodo = input('Quick ou Merge (q ou m)? ')
        if metodo == 'fim': # condicao de saida
            quit()
        print()
        # solicita ordem
        ordem = input('Ordem - comp1a4? ')
        if ordem == 'fim': # condicao de saida
            quit()
        print()
        # inicio da contagem de tempo
        t0 = time()
        # funcao de classificacao
        despacho_metodo[metodo](TAB, comp_fn=despacho_comp[ordem])
        # fim da contagem de tempo
        t1 = time()
        dt = t1 - t0
        # impressao do resultado
        imprimir_classificacao(TAB, metodo=metodo, tempo=dt, ordem=ordem, n_linhas=100)
        print()

def importarTAB(arquivo):
    """
    Lê a tabela contida no caminho 'arquivo' e
    retorna uma lista de listas (linhas da tabela).
    Caso o formato do arquivo não esteja de acordo
    com o enunciado, levanta uma exceção.    
    """
    with open(arquivo, 'r', encoding='utf-8') as a:
        try:
            TAB = [linha.strip().split(',') for linha in a.readlines()]
        except Exception:
            raise ImportError("erro na importação do arquivo, verifique se o formato está adequado e tente novamente.")
    return TAB

def imprimir_classificacao(TAB, metodo, tempo, ordem, n_linhas):
    """
    Imprime os resultados de uma classificação
    seguindo o formato do enunciado.
    Argumentos:
    TAB:      a tabela classificada, no mesmo formato
              do retorno da funcao importarTAB.
    metodo:   'q' ou 'm' (quick ou merge).
    tempo:    o tempo que o algoritmo demorou.
    ordem:    numero int de 1 a 4 denotando a funcao
              de comparacao escolhida.
    n_linhas: numero de linhas de TAB a ser impresso
              apos realizada a classificacao.
    """
    print(f'Tempo do {nome_metodo[metodo]}: {round(tempo, 6)}')
    print()
    print(f'{n_linhas} primeiros registros da tabela')
    print(f'Ordem: {descricao_comp[ordem]}')
    print()
    print(f"{'Indice':<8} {'Identidade':<15} {'Nome':<40} {'Data':<10}")
    for i in range(n_linhas):
        print(f'{i+1:<8} {TAB[i][0]:<15} {TAB[i][1]:<40} {TAB[i][2]:<10}')

def intercalar(sublista1, sublista2, lista, inicio, comp_fn):
    """
    Executa a intercalação de elementos entre
    duas sublistas, escrevendo sobre uma
    terceira lista. É o motor principal do
    algoritmo merge (função ClassificaMerge).
    Usa a função de comparaçao dada por comp_fn,
    e parte do índice de lista dado por inicio.
    (Implementação inspirada na versão dada
    em sala pelo professor, com adaptações.)
    """
    n, m = len(sublista1), len(sublista2)
    i, j, k = 0, 0, inicio
    while i < n and j < m:
        if comp_fn(sublista1[i], sublista2[j]):
            lista[k] = sublista1[i]
            i = i + 1
        else:
            lista[k] = sublista2[j]
            j = j + 1
        k = k + 1
    while i < n:
        lista[k] = sublista1[i]
        i, k = i + 1, k + 1
    while j < m:
        lista[k] = sublista2[j]
        j, k = j + 1, k + 1

def particionar(lista, inicio, fim, comp_fn):
    """
    Percorre a lista executando a troca de ordem
    entre o pivô e os demais elementos, motor
    principal do algoritmo quick
    (função ClassificaQuick).
    Usa a função de comparaçao dada por comp_fn,
    e parte dos índices de lista dados por
    inicio e fim.
    (Implementação inspirada na versão dada
    em sala pelo professor, com adaptações.)
    """
    i, j = inicio, fim
    pivo = lista[fim]
    while True:
        while i < j and comp_fn(lista[i], pivo):
            i = i + 1
        if i < j:
            lista[i], lista[j] = pivo, lista[i]
        else:
            break
        while i < j and not comp_fn(lista[j], pivo):
            j = j - 1
        if i < j:
            lista[i], lista[j] = lista[j], pivo
        else:
            break
    return i




# -----------
# 3) DICTS AUXILIARES
# -----------

# permite selecionar a funcao de classificacao
# a ser aplicada a partir do input do usuario
despacho_metodo = {
    'm': ClassificaMerge,
    'q': ClassificaQuick
}

# permite selecionar a funcao de comparacao
# a ser aplicada a partir do input do usuario
despacho_comp = {
    '1': comp1,
    '2': comp2,
    '3': comp3,
    '4': comp4
}

# utilidade para a funcao de impressao imprimir
# corretamente o nome do metodo
nome_metodo = {
    'm': 'Merge',
    'q': 'Quick'
}

# utilidade para a funcao de impressao imprimir
# corretamente a descricao da ordem de comparacao
descricao_comp = {
    '1': 'cresc. por nome - cresc. por data - cresc. por id.',
    '2': 'cresc. por nome - decresc. por data - cresc. por id.',
    '3': 'decresc. por data - cresc. por nome - cresc. por id.',
    '4': 'cresc. por id. - cresc. por data - cresc. por nome'
}




# -----------
# 4) PROGRAMA
# -----------
if __name__ == '__main__':
    main()
