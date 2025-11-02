# -----------
# 0) DEPENDENCIAS E VARIAVEIS GLOBAIS
# -----------
from Compara import comp1, comp2, comp3, comp4





# -----------
# 1) FUNCOES OBRIGATORIAS
# -----------

def ClassificaQuick(TAB,comp):
    pass

def ClassificaMerge(TAB,comp):
    pass




# -----------
# 2) FUNCOES AUXILIARES
# -----------

def importarTAB(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as a:
        TAB = [linha.strip().split(',') for linha in a.readlines()]
    return TAB




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




# -----------
# 4) PROGRAMA
# -----------
if __name__ == '__main__':
    arquivo = input('Nome do arquivo de origem:')
    TAB = importarTAB(arquivo)
    print()
    metodo = input('Quick ou Merge (q ou m)? ')
    print()
    ordem = input('Ordem - comp1a4? ')



