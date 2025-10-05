import sudoku as sudoku
import re
from os import listdir
from pathlib import Path

diretorio_base = Path(__file__).parent
arquivos = listdir(diretorio_base / 'jogos_validacao')

for arquivo in arquivos:
    with open(diretorio_base / 'jogos_validacao' / arquivo, 'r') as f:
        linhas = [re.split(r'\s+', linha.strip()) for linha in f if linha.strip()]
    Matriz = []
    for linha in linhas:
        Matriz.append([int(valor) for valor in linha])
    print('Jogo:' + arquivo)
    print('Matriz inicial:')
    sudoku.ImprimirMatriz(Matriz)
    print('**********************************************')
    sudoku.Sudoku(Matriz)
    sudoku.ReinicializarVarsGlobais()
    print()
    silent = input('Aperte enter para continuar')