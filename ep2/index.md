# EP.2) Solucionador de Sudoku


## Objetivo

Escrever um programa que recebe da pessoa usuária um número entre 0 e 81, cria um jogo Sudoku solucionável com este número de valores pré-preenchidos, e resolve o jogo criado.

## Conceitos trabalhados

* Recursividade
* Algoritmos de *backtracking*
* Regras de escopo e o comando `global`
* Cópias profundas (`copy.deepcopy`)
* Teste e validação de programas
* Verificação de consistências
* Leitura de arquivos
* Fluxo de início e fim de programas

## Requisitos do enunciado

* A pessoa usuária insere um número de valores a serem pré-preenchidos em um jogo de Sudoku, recebendo de volta um jogo aleatório nesta configuração e uma lista de no máximo $10$ soluções.
* O programa automaticamente volta ao começo, soliticitando mais um número. Inserir `fim` fecha o programa.
* Deve-se definir e usar obrigatoriamente pelo menos as três funções abaixo:
    - `GeraMatrizSudoku(npp)` recebe o número `npp` inserido pelo usuário e gera uma matriz solucionável com `npp` valores pré-preenchidos;
    - `TestaMatrizSudoku(MatrizSudoku)` verifica se a `MatrizSudoku` fornecida é uma solução válida de algum jogo Sudoku, mostrando o resultado da checagem separadamente para linhas, colunas e quadrados internos; e
    - de maneira recursiva, `Sudoku(MatrizSudoku, linha, coluna)` encontra soluções o jogo gerado por `GeraMatrizSudoku`, usando `TestaMatrizSudoku` para checar cada solução e parando em no máximo $10$ soluções
* O programa deve estar inteiramente contido em um único script (no caso, o arquivo `ep2/sudoku.py`)
* Foram fornecidos arquivos contendo matrizes solucionáveis, neste projeto salvos na pasta `ep2/jogos_validacao/`, a serem opcionalmente solucionadas como forma de validação do programa.

Este último ponto não faz parte da entrega. Portanto, para validar o programa foi criado um script à parte chamado `ep2/validacao.py`.

Os detalhes do enunciado podem ser consultados no link abaixo.

**[Link para o enunciado](enunciado.pdf)**

## O jogo Sudoku

A título de recapitulação, o jogo Sudoku consiste em uma matriz $9\times 9$ subdividida em $9$ matrizes $3\times 3$ (quadrados internos). O objetivo é preencher toda a matriz com números de $1$ a $9$ de acordo com a regra de que o mesmo número não pode aparecer duas vezes nem na mesma linha, nem na mesma coluna, nem no mesmo quadrado interno. 

Geralmente, o jogo já vem pré-preenchido com alguns valores, cabendo à pessoa jogadora terminar de resolvê-lo. Vale atentar ao fato de que este preenchimento inicial não pode ser apenas aleatório. Mesmo que não viole as regras do jogo, é possível que um preenchimento inicial descuidado gere um jogo que venha a não ter solução. (O número de soluções possíveis para um jogo de Sudoku em determinada configuração inicial é complexo e figura como tópico de estudo da matemática discreta.)

## Descrição da resolução

Textualmente, o código está dividido em cinco partes:

0. dependências
1. funções obrigatórias (`GeraMatrizSudoku`, `TestaMatrizSudoku` e `Sudoku`)
2. dicionários auxiliares
3. funções acessórias
4. programa

As dependências são: 
* a função `deepcopy` da biblioteca `copy` para fazer cópias profundas da matriz trabalhada, que é uma lista de listas;
* a função `product` da biblioteca `itertools` para gerar o produto cartesiano ${0,...,9}^2$, facilitando gerar índices de células da matriz (pares ordenados); e
* da biblioteca `random`, as funções:
    - `sample` usada na função obrigatória `GeraMatrizSudoku`;
    - `randrange`, usada para gerar valores aleatórios dentre $9$ valores; e
    - `shuffle`, para introduzir aleatoriedade na criação de jogos e soluções.

O enunciado pede para que a função `GeraMatrizSudoku` preencha a matriz de maneira aleatória, cuidando para que não sejam violadas as regras do jogo. Porém, ao implementar desta forma, percebi que mesmo um número muito pequeno de valores pré-preenchidos (e.g. $2$) já podem ser suficientes para gerar um jogo insolúvel. Por isso, adotei a abordagem mais correta de encontrar uma solução e só depois ir retirando valores de modo a restar apenas com o número `npp` solicitado pela pessoa usuária.

Para tanto, se `npp` for maior que $1$, `GeraMatrizSudoku` chama `Sudoku` para gerar alguma solução aleatória e vai zerando células desta solução aleatoriamente (usando `sample`), até restarem `npp` valores. Caso contrário, se `npp ==0`, apenas se retorna uma matriz de zeros ou, se `npp == 1`, preencher aleatoriamente apenas um número, o que garante que a matriz terá solução.

Por sua vez, a função obrigatória principal `Sudoku` recebe três argumentos: uma referência para a matriz trabalhada, uma linha e uma coluna, sendo essas últimas as coordenadas por onde a função deve começar operando. O algoritmo então executado é um backtracking recursivo que funciona da seguinte forma:
* A partir da posição recebida, procura-se a próxima posição vazia, incluindo se for o caso a própria posição recebida.
* Se não houver mais nenhuma posição vazia, achou uma solução. Imprime e estoca essa solução e retorna da chamada atual.
* Se houver, sonda quais são os candidatos para preencher esta posição, usando a função auxiliar `CalcularCandidatos`. Os candidatos são os números que não violariam as regras do jogo.
* Se não houver mais candidatos, retorna da chamada atual.
* Se houver candidatos, inicia um loop para preencher a célula vazia com cada candidato, em ordem aleatória.
* Dentro deste loop, chama recursivamente a si mesma, agora iniciando da posição preenchida.
* Terminado o loop, zera a posição atual, que havia sido preenchida com o último candidato, permitindo assim o backtracking.

Nota-se que a escolha do candidato a ser preenchido representa as ramificações da árvore de busca, enquanto a inexistência de células vazias ou de candidatos representa as folhas (respectivamente, encontrando solução ou encontrando caminho insolúvel). Ao iterar sobre os candidatos, garantimos que todas as ramificações serão exploradas.

Para contar e registrar as soluções encontradas, observando o limite máximo de $10$ soluções, foram criadas duas variáveis globais, `n_encontradas` (`int`) e `solucoes_encontradas` (`list`), que a função `Sudoku` pode sobrescrever via `global`. Quando `n_encontradas == 10`, `Sudoku` passa a retornar exclusivamente `None`, eventualmente saindo da recursão. O estoque de soluções é feito fazendo-se uma cópia profunda de cada solução encontrada, pois o algoritmo procede sobrescrevendo a matriz fornecida, que é um objeto mutável, de modo que o backtracking zera essa matriz ao final do algoritmo. A função acessória `ReinicializarVarsGlobais` acessa via `global` e modifica tais variáveis globais sempre que necessário para garantir que sejam resetadas. O estoque de soluções é usado somente na geração de matriz inicial, visto que o enunciado pede apenas que soluções sejam impressas.

Quando uma solução é encontrada, `Sudoku` imprime a solução e chama a função obrigatória `TestaMatrizSudoku`, que por sua vez invoca as acessórias `TestarLinha`, `TestarColuna` e `TestarQuadrado` para verificar se uma solução cumpre as regras do jogo, conforme especificação do enunciado, imprimindo um relatório na tela. `Sudoku` avisa se encontrar alguma matriz que não é solução (comportamento que não deve acontecer e não aconteceu nos testes).

Visto que não podemos usar bibliotecas fora da biblioteca-padrão, criei uma série rotinas para facilitação e modularização:
* Uma função acessória `ProxPosicaoVazia` usa dois dicionários auxiliares que achatam a matriz em uma lista de índices em uma dimensão, e vice-versa, permitindo encontrar com facilidade a próxima célula vazia.
* Encontrar uma solução usa a acessória `ContarZeros`, que checa se ainda há posições vazias na matriz. 
* As funções acessórias `PegarColuna` e `PegarQuadradoInterno`, usadas para verificação de soluções e cálculo de candidatos, retornam o conteúdo da coluna e do quadrado interno onde uma célula está localizada, sendo que este último necessita de dicionários auxiliares para ser mapeado.
* A função acessória `ImprimirMatriz` imprime uma matriz separando seus quadrados internos.
* A acessória `main` roda o programa, com a seguinte estrutura dentro de um loop `while True`:
    - Chama a acessória `VerificarConsistencias` para checar se o input do usuário é válido (e retornando a mensagem adequada);
    - Implementa a condição de saída caso o input seja `fim`;
    - Chama `GeraMatrizSudoku` para gerar a matriz e imprimi-la usando `ImprimirMatriz`; e
    - Por fim, chama `Sudoku` depois de `ReinicializarVarsGlobais`, avisando caso existam mais de $10$ soluções.

Nas funções `Sudoku`e `TestaMatrizSudoku` foi incluído um argumento booleano adicional `imprimir`. Quando `GeraMatrizSudoku` é invocada, usa-se `imprimir=False`, fazendo tudo silenciosamente. Quando `main` é quem chama `Sudoku`, `imprimir=True`. Abaixo segue um exemplo da impressão de uma rodada do programa:

```
Entre com o número de posições a preencher inicialmente:40
Matriz inicial
1 9 0 | 0 0 6 | 8 0 0
0 3 0 | 2 1 0 | 0 4 0
8 2 0 | 0 0 0 | 6 3 1
---------------------
0 5 0 | 0 8 4 | 3 1 0
0 0 0 | 5 2 1 | 0 0 4
0 4 0 | 0 9 3 | 2 8 5
---------------------
4 1 9 | 3 0 2 | 0 7 8
0 0 8 | 0 5 0 | 0 0 0
0 7 5 | 0 4 0 | 0 0 0
**********************************************
1ª solução encontrada:
1 9 7 | 4 3 6 | 8 5 2
5 3 6 | 2 1 8 | 9 4 7
8 2 4 | 9 7 5 | 6 3 1
---------------------
6 5 2 | 7 8 4 | 3 1 9
9 8 3 | 5 2 1 | 7 6 4
7 4 1 | 6 9 3 | 2 8 5
---------------------
4 1 9 | 3 6 2 | 5 7 8
2 6 8 | 1 5 7 | 4 9 3
3 7 5 | 8 4 9 | 1 2 6
linhas OK
colunas OK
quadrados OK
solução completa e consistente
**********************************************
2ª solução encontrada:
1 9 7 | 4 3 6 | 8 5 2
5 3 6 | 2 1 8 | 9 4 7
8 2 4 | 9 7 5 | 6 3 1
---------------------
7 5 2 | 6 8 4 | 3 1 9
9 8 3 | 5 2 1 | 7 6 4
6 4 1 | 7 9 3 | 2 8 5
---------------------
4 1 9 | 3 6 2 | 5 7 8
2 6 8 | 1 5 7 | 4 9 3
3 7 5 | 8 4 9 | 1 2 6
linhas OK
colunas OK
quadrados OK
solução completa e consistente
**********************************************
3ª solução encontrada:
1 9 7 | 4 3 6 | 8 5 2
5 3 6 | 2 1 8 | 9 4 7
8 2 4 | 9 7 5 | 6 3 1
---------------------
9 5 2 | 7 8 4 | 3 1 6
6 8 3 | 5 2 1 | 7 9 4
7 4 1 | 6 9 3 | 2 8 5
---------------------
4 1 9 | 3 6 2 | 5 7 8
3 6 8 | 1 5 7 | 4 2 9
2 7 5 | 8 4 9 | 1 6 3
linhas OK
colunas OK
quadrados OK
solução completa e consistente
**********************************************
4ª solução encontrada:
1 9 7 | 4 3 6 | 8 5 2
5 3 6 | 2 1 8 | 7 4 9
8 2 4 | 9 7 5 | 6 3 1
---------------------
9 5 2 | 6 8 4 | 3 1 7
7 8 3 | 5 2 1 | 9 6 4
6 4 1 | 7 9 3 | 2 8 5
---------------------
4 1 9 | 3 6 2 | 5 7 8
2 6 8 | 1 5 7 | 4 9 3
3 7 5 | 8 4 9 | 1 2 6
linhas OK
colunas OK
quadrados OK
solução completa e consistente
**********************************************
```

O usuário que quiser interagir com o programa pode baixar o script no link abaixo e, usando alguma versão compatível de Python, executá-lo no prompt de comando.

**[Link para o script principal](sudoku.py)**

## Inserção de matrizes pré-preenchidas e validação do programa

Além de testes com a versão interativa do programa, entregue a título de resolução, também segui a sugestão do enunciado de fazer uma validação usando um conjunto de jogos fornecidos pelo professor.

Esta validação foi feita separadamente no script `ep2/validacao.py`. Ela acessa os jogos em formato de texto puro, com células separadas por espaços e preenchidas com zero no caso de células vazias, salvos na pasta `ep2/jogos_validacao`. Um loop itera sobre os arquivos dessa pasta e mostra as soluções de um jogo cada vez que o botão enter é apertado.

No meu caso, para validar o programa comparei manualmente as soluções de cada jogo com soluções dadas por outros solucionadores conhecidos de Sudoku. Todas as soluções encontradas foram iguais às desses solucionadores.

A pessoa que quiser usar este programa para resolver algum(ns) jogo(s) pode simplesmente substituir o(s) arquiv(os) na pasta em questão (esta pasta deve conter apenas jogos de Sudoku no formato correto). O script pode ser conferido no link abaixo:

**[Link para o script que resolve jogos fornecidos em arquivo](validacao.py)**