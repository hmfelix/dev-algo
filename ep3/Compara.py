# -----------
# 0) DEPENDENCIAS E VARIAVEIS GLOBAIS
# -----------
from datetime import date




# -----------
# 1) FUNCOES OBRIGATORIAS
# -----------

def comp1(a, b):
    """
    crescente por nome - crescente por data - crescente por id
    """
    # checa empate em nome
    if a[1] == b[1]:
        da = as_date(a[2])
        db = as_date(b[2])
        # checa empate em data
        if da == db:
            # compara ids
            return a[0] <= b[0]
        else:
            # compara datas
            return da <= db
    else:
        # compara nomes
        return a[1] <= b[1]

def comp2(a, b):
    """
    crescente por nome - decrescente por data - crescente por identidade
    """
    # checa empate em nome
    if a[1] == b[1]:
        da = as_date(a[2])
        db = as_date(b[2])
        # checa empate em data
        if da == db:
            # compara ids
            return a[0] <= b[0]
        else:
            # compara datas
            return da >= db
    else:
        # compara nomes
        return a[1] <= b[1]

def comp3(a, b):
    """
    decrescente por data - crescente por nome - crescente por identidade
    """
    # checa empate em datas
    da = as_date(a[2])
    db = as_date(b[2])
    if da == db:
        # checa empate em nomes
        if a[1] == b[1]:
            # compara ids
            return a[0] <= b[0]
        else:
            # compara nomes
            return a[1] <= b[1]
    else:
        # compara datas
        return da >= db

def comp4(a, b):
    """
    crescente por identidade - crescente por data - crescente por nome
    """
    # checa empate em id
    if a[0] == b[0]:
        da = as_date(a[2])
        db = as_date(b[2])
        # checa empate em data
        if da == db:
            # compara nomes
            return a[1] <= b[1]
        else:
            # compara datas
            return da <= db
    else:
        # compara id
        return a[0] <= b[0]




# -----------
# 2) FUNCAO AUXILIAR
# -----------

def as_date(date_str):
    return date(*reversed([int(e) for e in date_str.split('/')]))
