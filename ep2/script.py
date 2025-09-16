# 0) dependencias
from random import randrange





# 1) funcoes obrigatorias

def GeraMatrizSudoku(npp):
    # verificacao de consistencia: input deve ser numero inteiro
    try:
        npp_as_int = int(npp)
        npp_as_complex = complex(npp)
        if npp_as_int == npp_as_complex: # se for float ou complex e for inteiro, aqui avalia para True
            npp = npp_as_int # garante que o inteiro fornecido tera o tipo int
        else: # se nao for numero inteiro
            return None
    except Exception: # caso haja algum outro problema, permite a continuacao do programa
        return None
    # verificacao de consistencia: input deve estar entre 0 e 81
    if npp > 81 or npp < 0:
        return -1
    # pre-alocando memoria com matriz de zeros
    pre_aloc_matriz = [[0] * 9 for k in range(9)]
    # retornando essa matriz no caso trivial
    if npp == 0:
        return pre_aloc_matriz
    # algoritmo para criar matriz valida
    ## primeira posicao eh arbitraria
    primeiro_sorteio = SortearCelula() # funcao auxiliar definida abaixo, usa random.randrange()
    ## lista para estocar celulas ja preenchidas
    lista_sorteadas = {primeiro_sorteio}
    ## primeira posicao admite qualquer algarismo
    linha, coluna =  primeiro_sorteio
    pre_aloc_matriz[coluna][linha] = randrange(1, 10)
    ## algoritmo principal
    for i in range(npp-1):
        # (i) procura celula vazia
        nova_celula = SortearCelula() # sorteia uma celula
        while nova_celula in lista_sorteadas: # sorteia de novo caso ja esteja ocupada
            nova_celula = SortearCelula()
        lista_sorteadas.add(nova_celula)
        nova_linha, nova_coluna = nova_celula
        # (ii) procura algarismo ainda disponivel
        novo_algarismo = randrange(1, 10)
        candidatos = CalcularCandidatos(nova_celula, pre_aloc_matriz) # funcao auxiliar definida abaixo
        while novo_algarismo not in candidatos:
            novo_algarismo = randrange(1, 10)
        # (iii) escreve o algarismo escolhido na celula escolhida
        pre_aloc_matriz[nova_coluna][nova_linha] = novo_algarismo
    return pre_aloc_matriz




        

    # sorteia
    # checa se tem algo lá
    #   se sim, sorteia de novo ate





def TestaMatrizSudoku(MatrizSudoku):
    pass





# 2) funcoes auxiliares

def SortearCelula():
    """
    Apenas sorteia dois numeros entre 1 e 9,
    retornando uma tupla que representa uma celula da matriz.
    """
    linha = randrange(0,9)
    coluna = randrange(0,9)
    return (linha, coluna)

def PegarLinha(linha, matriz):
    """
    Como a matriz eh estocada em formato de lista de colunas, obter uma
    linha da matriz nao eh um processo tao direto quanto obter uma coluna.
    Esta funcao coleta retorna uma lista com a linha desejada.
    """
    return [coluna[linha] for coluna in matriz]

def PegarQuadradoInterno(celula, matriz):
    """
    Retorna uma lista dos valores contidos no quadrado interno da celula
    fornecida.
    """
    quadrado_interno = quadrados_internos_dict[celula]
    return [matriz[local[1]][local[0]] for local, regiao in quadrados_internos_dict.items() if regiao == quadrado_interno]

def CalcularCandidatos(celula, matriz):
    """
    Retorna lista com numeros que ainda podem ser preenchidos em uma celula.
    - 'celula' deve ser uma tupla no formato (linha, coluna)
    - 'matriz' deve ser uma lista de listas cujos elementos sao as colunas
    """
    linha, coluna = celula
    vetor_linha = PegarLinha(linha, matriz)
    vetor_coluna = matriz[coluna]
    vetor_quadrado_interno = PegarQuadradoInterno(celula, matriz)
    valores_usados = set(vetor_coluna + vetor_linha + vetor_quadrado_interno)
    algarismos = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    valores_disponiveis = algarismos - valores_usados
    valores_disponiveis.discard(0)
    return list(valores_disponiveis)

def ImprimirMatriz(matriz):
    barra_horizontal = '---------------------'
    linhas = []
    for i in range(9):
        linha_sem_barras_verticais = ' '.join([str(algarismo) for algarismo in PegarLinha(i, matriz)])
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



# 3) dicionario de quadrados internos

## permite determinar a qual regiao da matriz pertence uma celula
## a matriz possui 9 regioes, cada uma como uma sub-matriz 9x9,
## como segue:
##  1 | 4 | 7 
## -----------
##  2 | 5 | 8 
## -----------
##  3 | 6 | 9

quadrados_internos_dict = {
    (0,0): 1,
    (1,0): 1,
    (2,0): 1,
    (3,0): 2,
    (4,0): 2,
    (5,0): 2,
    (6,0): 3,
    (7,0): 3,
    (8,0): 3,
    (0,1): 1,
    (1,1): 1,
    (2,1): 1,
    (3,1): 2,
    (4,1): 2,
    (5,1): 2,
    (6,1): 3,
    (7,1): 3,
    (8,1): 3,
    (0,2): 1,
    (1,2): 1,
    (2,2): 1,
    (3,2): 2,
    (4,2): 2,
    (5,2): 2,
    (6,2): 3,
    (7,2): 3,
    (8,2): 3,
    (0,3): 4,
    (1,3): 4,
    (2,3): 4,
    (3,3): 5,
    (4,3): 5,
    (5,3): 5,
    (6,3): 6,
    (7,3): 6,
    (8,3): 6,
    (0,4): 4,
    (1,4): 4,
    (2,4): 4,
    (3,4): 5,
    (4,4): 5,
    (5,4): 5,
    (6,4): 6,
    (7,4): 6,
    (8,4): 6,
    (0,5): 4,
    (1,5): 4,
    (2,5): 4,
    (3,5): 5,
    (4,5): 5,
    (5,5): 5,
    (6,5): 6,
    (7,5): 6,
    (8,5): 6,
    (0,6): 7,
    (1,6): 7,
    (2,6): 7,
    (3,6): 8,
    (4,6): 8,
    (5,6): 8,
    (6,6): 9,
    (7,6): 9,
    (8,6): 9,
    (0,7): 7,
    (1,7): 7,
    (2,7): 7,
    (3,7): 8,
    (4,7): 8,
    (5,7): 8,
    (6,7): 9,
    (7,7): 9,
    (8,7): 9,
    (0,8): 7,
    (1,8): 7,
    (2,8): 7,
    (3,8): 8,
    (4,8): 8,
    (5,8): 8,
    (6,8): 9,
    (7,8): 9,
    (8,8): 9
}



# 4) programa

if __name__ == '__main__':
    while True:
        npp = input('Entre com o número de posições a preencher inicialmente:')
        Matriz = GeraMatrizSudoku(npp)
        if Matriz is None:
            print('Input deve ser numero inteiro.')
            continue
        if Matriz == -1:
            print('O número de posições não pode ser menor que 0 ou maior que 81.')