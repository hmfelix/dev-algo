# -----------
# 0) DEPENDENCIAS
# -----------
from random import sample, randrange, shuffle
from itertools import product
from copy import deepcopy




# -----------
# 1) FUNCOES OBRIGATORIAS
# -----------

def GeraMatrizSudoku(npp):
    """
    Gera matriz solucionável com o número de valores
    pré-preenchidos especificado pelo usuário.
    """
    zeros = [[0]*9 for _ in range(9)]
    if npp == 0:
        return zeros
    linha = randrange(0,9)
    coluna = randrange(0,9)
    zeros[linha][coluna] = randrange(0,9)
    if npp == 1:
        return zeros
    ReinicializarVarsGlobais()
    Sudoku(zeros, imprimir=False)
    ind = randrange(0,len(solucoes_encontradas))
    solucao_provisoria = deepcopy(solucoes_encontradas[ind])
    ReinicializarVarsGlobais()
    a_retirar = sample(list(range(81)), 81-npp)
    for indice in a_retirar:
        coord = indice_flat_dict[indice]
        solucao_provisoria[coord[0]][coord[1]] = 0
    return solucao_provisoria
    
def TestaMatrizSudoku(MatrizSudoku, imprimir=True):
    """
    Testa se a matriz fornecida é uma solução válida de sudoku.
    Retorna True ou False. Imprime a verificação caso 'imprimir'
    seja True.
    """
    # listas de valores booleanos estocam se cada
    # componente testado esta ok
    testes_linhas = []
    testes_colunas = []
    testes_quadrados = []
    # loop que realiza os testes para cada componente
    for i in range(9):
        testes_linhas.append(TestarLinha(i, MatrizSudoku))
        testes_colunas.append(TestarColuna(i, MatrizSudoku))
        testes_quadrados.append(TestarQuadrado(i, MatrizSudoku))
    # conta quantos componentes de cada tipo estao ok
    soma_linhas = sum(testes_linhas)
    soma_colunas = sum(testes_colunas)
    soma_quadrados = sum(testes_quadrados)
    # impressoes sobre cada componente
    if soma_linhas == 9 and imprimir:
        print('linhas OK')
    if soma_colunas == 9 and imprimir:
        print('colunas OK')
    if soma_quadrados == 9 and imprimir:
        print('quadrados OK')
    # avaliacao e impressao geral
    if soma_linhas + soma_colunas + soma_quadrados == 27:
        if imprimir: 
            print('solução completa e consistente')
        return True
    return False

def Sudoku(MatrizSudoku, linha=0, coluna=0, imprimir=True):
    """
    Implementa algoritmo recursivo para solucionar a matriz
    dada, iniciando o algoritmo da célula dada (linha, coluna).
    Imprime as soluções caso imprimir seja True, não imprime
    caso seja False.
    """
    global n_encontradas
    global solucoes_encontradas
    if n_encontradas == 10:
        return None
    if MatrizSudoku[linha][coluna] == 0:
        pp = (linha, coluna)
    else:
        pp = ProxPosicaoVazia(MatrizSudoku, linha, coluna)
    if pp is None:
        n_encontradas += 1
        if imprimir:
            print(f'{n_encontradas}ª solução encontrada:')
            ImprimirMatriz(MatrizSudoku)
            if TestaMatrizSudoku(MatrizSudoku, imprimir=imprimir) is False:
                raise Exception('Algum erro aconteceu: esta não é uma solução.')
            print('**********************************************')
        if n_encontradas == 10:
            if imprimir:
                print('Existem mais soluções além de 10, que não foram imprimidas.')
        else:
            solucoes_encontradas.append(deepcopy(MatrizSudoku))
        return None
    else:
        candidatos = CalcularCandidatos(pp, MatrizSudoku)
        shuffle(candidatos)
        if candidatos == []:
            MatrizSudoku[linha][coluna] = 0
            return None
        for candidato in candidatos:
            MatrizSudoku[pp[0]][pp[1]] = candidato
            Sudoku(MatrizSudoku, pp[0], pp[1], imprimir=imprimir)
        MatrizSudoku[pp[0]][pp[1]] = 0
        return None




# -----------
# 2) DICIONARIOS AUXILIARES
# -----------

# dicionarios usados pela funcao ProxPosicao para averiguar proxima
# posicao vazia. mapeiam uma coordenada em Z^2 (linha, coluna) a uma
# coordenada em Z (indice) e vice-versa, permitindo percorrer a 
# matriz como se fosse uma lista.
dim_1 = list(range(9))
dim_2 = list(product(dim_1, dim_1))
coord_2D_flat_dict = {chave: i for i, chave in enumerate(dim_2)}
indice_flat_dict = {i: coord for i, coord in enumerate(dim_2)}

# dicionarios usados para lidar com os quadrados internos
# da matriz, mapeando cada celula a um quadrado e
# cada quadrado a sua celula central.
quadrados_internos_dict = {
    (0,0): 1, (1,0): 1, (2,0): 1, (3,0): 2, (4,0): 2, (5,0): 2, (6,0): 3, (7,0): 3, (8,0): 3,
    (0,1): 1, (1,1): 1, (2,1): 1, (3,1): 2, (4,1): 2, (5,1): 2, (6,1): 3, (7,1): 3, (8,1): 3,
    (0,2): 1, (1,2): 1, (2,2): 1, (3,2): 2, (4,2): 2, (5,2): 2, (6,2): 3, (7,2): 3, (8,2): 3,
    (0,3): 4, (1,3): 4, (2,3): 4, (3,3): 5, (4,3): 5, (5,3): 5, (6,3): 6, (7,3): 6, (8,3): 6,
    (0,4): 4, (1,4): 4, (2,4): 4, (3,4): 5, (4,4): 5, (5,4): 5, (6,4): 6, (7,4): 6, (8,4): 6,
    (0,5): 4, (1,5): 4, (2,5): 4, (3,5): 5, (4,5): 5, (5,5): 5, (6,5): 6, (7,5): 6, (8,5): 6,
    (0,6): 7, (1,6): 7, (2,6): 7, (3,6): 8, (4,6): 8, (5,6): 8, (6,6): 9, (7,6): 9, (8,6): 9,
    (0,7): 7, (1,7): 7, (2,7): 7, (3,7): 8, (4,7): 8, (5,7): 8, (6,7): 9, (7,7): 9, (8,7): 9,
    (0,8): 7, (1,8): 7, (2,8): 7, (3,8): 8, (4,8): 8, (5,8): 8, (6,8): 9, (7,8): 9, (8,8): 9
}
celulas_centrais_dict = {
    0: (1,1), 1: (4,1), 2: (7,1), 3: (1,4), 4: (4,4), 5: (7,4), 6: (1,7), 7: (4,7), 8: (7,7)
}




# -----------
# 3) FUNCOES AUXILIARES
# -----------

def main():
    """
    Função principal que roda quando começa o programa.
    """
    while True:
        # coleta o input
        npp = input('Entre com o número de posições a preencher inicialmente:')
        # verifica valor de input, implementando condicao de saida
        verificacao = VerificarConsistencias(npp)
        # lida com problemas de input
        if verificacao == -1:
            print('Input deve ser número inteiro.')
            continue
        if verificacao == -2:
            print('O número de posições não pode ser menor que 0 ou maior que 81.')
            continue
        # cria a matriz a ser solucionada
        Matriz = GeraMatrizSudoku(int(npp))
        print('Matriz inicial')
        ImprimirMatriz(Matriz)
        print('**********************************************')
        ReinicializarVarsGlobais()
        Sudoku(Matriz)
        if n_encontradas <= 10:
            print('Estas são todas as soluções existentes.')
        print()

def ReinicializarVarsGlobais():
    """
    Reinicializa as variáveis globais que permitem o backtracking
    e guardam as soluções encontradas.
    """
    global n_encontradas
    global solucoes_encontradas
    n_encontradas = 0
    solucoes_encontradas = []
    return

def VerificarConsistencias(npp):
    """
    Lida com a condição de saída do programa e com a verificação de
    consistências do input do usuário.
    """
    # condicao de saida
    if npp == 'fim':
        quit()
    # input deve ser numero inteiro
    try:
        npp_as_int = int(npp)
        npp_as_complex = complex(npp)
        if npp_as_int == npp_as_complex: # se for float ou complex e for inteiro, aqui avalia para True
            npp = npp_as_int # garante que o inteiro fornecido tera o tipo int
        else: # se nao for numero inteiro
            return -1
    except Exception: # caso haja algum outro problema, permite a continuacao do programa
        return -1
    # input deve estar entre 0 e 81
    if npp > 81 or npp < 0:
        return -2
    return

def PegarColuna(coluna, MatrizSudoku):
    """
    Como a matriz é estocada em formato de lista de linhas, obter uma
    coluna da matriz não é um processo tão direto quanto obter uma linha.
    Esta função retorna uma lista com o conteúdo da coluna desejada.
    """
    return [linha[coluna] for linha in MatrizSudoku]

def PegarQuadradoInterno(celula, MatrizSudoku):
    """
    Retorna uma lista dos valores contidos no quadrado interno da célula
    fornecida.
    """
    quadrado_interno = quadrados_internos_dict[celula]
    return [MatrizSudoku[local[0]][local[1]] for local, regiao in quadrados_internos_dict.items() if regiao == quadrado_interno]

def ContarZeros(MatrizSudoku):
    """
    Conta o número de células ainda vazias na matriz dada. Usada para
    checar se foi encontrada uma solução
    """
    zeros = sum(1 for linha in MatrizSudoku for valor in linha if valor == 0)
    return zeros

def CalcularCandidatos(celula, MatrizSudoku):
    """
    Retorna lista com números que ainda podem ser preenchidos em uma célula.
    - 'celula' deve ser uma tupla no formato (linha, coluna)
    - 'matriz' deve ser uma lista de listas cujos elementos são as colunas
    """
    linha, coluna = celula
    vetor_linha = MatrizSudoku[linha]
    vetor_coluna = PegarColuna(coluna, MatrizSudoku)
    vetor_quadrado_interno = PegarQuadradoInterno(celula, MatrizSudoku)
    valores_usados = set(vetor_linha + vetor_coluna + vetor_quadrado_interno)
    algarismos = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    valores_disponiveis = algarismos - valores_usados
    valores_disponiveis.discard(0)
    return list(valores_disponiveis)

def TestarLinha(linha, MatrizSudoku):
    """
    Testa se uma linha está adequada para a solução.
    Retorna True se a linha não possui algarismos repetidos
    e False se possui (ou se possui 0).
    """
    vetor_linha = MatrizSudoku[linha]
    if set(vetor_linha) == {1, 2, 3, 4, 5, 6, 7, 8, 9}:
        return True
    return False

def TestarColuna(coluna, MatrizSudoku):
    """
    Testa se uma coluna está adequada para a solução.
    Retorna True se a coluna não possui algarismos repetidos
    e False se possui (ou se possui 0).
    """
    vetor_coluna = PegarColuna(coluna, MatrizSudoku)
    if set(vetor_coluna) == {1, 2, 3, 4, 5, 6, 7, 8, 9}:
        return True
    return False

def TestarQuadrado(quadrado, MatrizSudoku):
    """
    Testa se um quadrado interno está adequado para a solução.
    Retorna True se o quadrado não possui algarismos repetidos
    e False se possui (ou se possui 0).
    """
    celula = celulas_centrais_dict[quadrado]
    vetor_quadrado_interno = PegarQuadradoInterno(celula, MatrizSudoku)
    if set(vetor_quadrado_interno) == {1, 2, 3, 4, 5, 6, 7, 8, 9}:
        return True
    return False

def ImprimirMatriz(MatrizSudoku):
    """
    Imprime uma matriz no prompt, separada por seus quadrados internos.
    (Não adiciona quebras de linha antes nem depois.)
    """
    barra_horizontal = '---------------------'
    linhas = []
    for i in range(9):
        linha_sem_barras_verticais = ' '.join([str(algarismo) for algarismo in MatrizSudoku[i]])
        linha_com_barras_verticais = linha_sem_barras_verticais[:6] + '| ' + linha_sem_barras_verticais[6:12] + '| ' + linha_sem_barras_verticais[12:]
        linhas.append(linha_com_barras_verticais)
    print(linhas[0])
    print(linhas[1])
    print(linhas[2])
    print(barra_horizontal)
    print(linhas[3])
    print(linhas[4])
    print(linhas[5])
    print(barra_horizontal)
    print(linhas[6])
    print(linhas[7])
    print(linhas[8])

def ProxPosicaoVazia(MatrizSudoku, linha=0, coluna=0):
    """
    Retorna a próxima posição vazia na matriz sudoku fornecida,
    ou None caso não haja. Usada na função obrigatória Sudoku().
    """
    prox_indice = coord_2D_flat_dict[(linha, coluna)] + 1
    if prox_indice == 81:
        return None
    prox_coord = indice_flat_dict[prox_indice]
    while MatrizSudoku[prox_coord[0]][prox_coord[1]] > 0:
        prox_indice += 1
        if prox_indice == 81:
            return None
        prox_coord = indice_flat_dict[prox_indice]
    return prox_coord






# -----------
# 4) PROGRAMA
# -----------

if __name__ == '__main__':
    n_encontradas = 0
    solucoes_encontradas = []
    main()

        