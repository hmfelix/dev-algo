# EP.1) Interpretador de expressões com números complexos


## Objetivo

Criar um programa que seja capaz de receber do usuário uma expressão contendo números complexos e devolver o valor calculado desta expressão, sem fazer uso da classe ```complex``` do Python.

## Conceitos trabalhados

* Objetos
* Polimorfismo por sobrecarga de operador
* Pilhas
* Notação pós-fixa
* Cálculo de expressões aritméticas
* Tratamento de exceções

## Requisitos do enunciado

* O usuário insere uma string em um prompt idêntico ao do Python (que aguarda um input depois de ```>>>```) e recebe o resultado logo em seguida, podendo inserir nova expressão sempre que quiser.
* Todo número complexo será inserido com a sintaxe ```(a + bi)``` (e variações de sinal), com ```a``` e ```b``` sendo ```int``` ou ```float```. Isso difere da sintaxe padrão do Pyhton, que usa ```j``` para sinalizar a parte imaginária.
* Espaços em branco não prejudicam o input.
* Os operadores permitidos no input são as quatro operações binárias da aritmética (```+```, ```-```, ```*``` e ```/```) e os sinais unários (```+``` e ```-```), além de abre e fecha parênteses ```()``` para fins de agrupamento.
* O programa deve definir e usar obrigatoriamente quatro objetos:
    - uma classe chamada ```Complexo``` que construa um número complexo e permita todas as operações acima; 
    - uma classe chamada ```Pilha``` que implemente a estrutura de dado de uma pilha;
    - uma função chamada ```TraduzPosFixa()``` que recebe a expressão aritmética do usuário e a traduz para a notação pós-fixa em formato de lista; e
    - uma função chamada ```CalcPosFixa()``` que recebe uma lista em notação pós-fixa e retorna um ```Complexo()``` contendo o resultado, imprimindo-o na tela no formato ```(a + bi)``` ou ```(a +bi)``` (e variações de sinal).
* Caso o input esteja em formato inválido, deve ser retornado ```None```.
* O programa de estar todo contido em um único script de nome ```posfixa.py```.

[link para o enunciado](enunciado.pdf)

## Descrição da resolução

Textualmente, o código está dividido em cinco partes:

0. dependências
1. classes obrigatórias (```Pilha``` e ```Complexo```)
2. funções obrigatórias (```TraduzPosFixa()``` e ```CalcPosFixa()```)
3. funções acessórias
4. programa

Há somente uma dependência: a biblioteca ```re```, usada para tokenizar o input do usuário. A expressão regular de tokenização foi fornecida pelo enunciado.

Por ser uma atividade mais simples, optou-se por criar apenas classes obrigatórias, escolhendo-se uma abordagem mais procedural para as demais funcionalidades.

De acordo com o enunciado, o tipo ```Pilha``` pode usar as funcionalidades da lista de Python, o que facilitou imensamente sua implementação. Trata-se basicamente de uma lista mais restrita. Optou-se por uma API minimal, contendo apenas o necessário: uma lista de elementos como atributo e os métodos ```__str__()``` (para impressão), ```len()``` (retorna o tamanho da pilha), ```is_empty()``` (```True``` se a lista está vazia, ```False``` se não), ```top()``` (mostra o topo), ```push(x)``` (adiciona elemento), e ```pop()``` (remove e retorna elemento do topo).

Já o tipo ```Complexo``` é mais elaborado, contendo: alguns nomes de classe para verificação de tipo; atributos ```.Re``` e ```.Im``` para partes real e imaginária, sem getters ou setters devido à ausência de acesso por parte do usuário; representações via ```__str__``` e ```__repr```, sendo esta última necessária para avaliar expressões via ```eval()```; operadores unários ```+``` , ```-``` e ```conj()``` (conjugado, usado para implementar a divisão); operadores binários ```+```, ```-```, ```*``` e ```/```, implementando a checagem de divisão por zero.

Os nomes de classe foram usados não somente na função construtora (aceitando ```int``` ou ```float```), mas também para viabilizar operações com um ```Complexo``` na primeira posição e um ```int``` ou ```float``` na segunda posição. Já a inversão dessas posições (primeiro ```int``` | ```float``` depois ```Complexo```) foi possibilitada apenas na função de cálculo da expressão (```CalcPosFixa```) usando o artifício de transformar esses tipos em ```Complexo```, para evitar a construção de novos objetos extendendo as classes ```int``` e ```float```.

Funções auxiliares foram usadas primordialmente para converter a string fornecida pelo usuário em uma lista contendo operadores e operandos, esses últimos já transformados em ```Complexo``` quando necessário. A função ```TraduzPosFixa()``` recebe a string, chama as funções auxiliares (envolvidas em uma função chamada ```ProcessarInput()```), e opera o algoritmo padrão de tradução para notação pós-fixa, dado no enunciado, retornando uma lista com os operadores e operandos nesta nova ordem. O fluxo da string de input ao passar pela ```TraduzPosFixa()```, incluindo funções auxiliares, é da seguinte forma:

|      |       |        |     |    |    |   |     |  |  |
|:-----:|:--------:|:------:|:----:|:----:|:----:|:---:|:-----:|:---:|:-----:|
| **Função** | | ```Tokenizar``` |  | ```SubsComplexos``` | | ```SubsUnarios``` |  | loop de ```TraduzPosFixa``` |
| **Tipo** | string | $\rightarrow$ | lista | $\rightarrow$ | lista |$\rightarrow$ | lista | $\rightarrow$ | lista |
| **Conceito** | input | $\rightarrow$ | tokens | $\rightarrow$ | complexos detectados | $\rightarrow$ | unários detectados | $\rightarrow$ | pós-fixa |
| **Exemplo** | ```(2 + 3i) * -10``` | | ```['(', '2', '+', '3i' , ')', '*', '-', '10']``` | | ```[Complexo(2, 3), '*', '-', '10']``` | | ```[Complexo(2, 3), '*', '_', '10']``` | | ```[Complexo(2.0, 3.0), '10', '_', '*']```| 

O algoritmo de tradução, principal loop da função ```TraduzPosFixa()```, foi implementado usando-se duas pilhas:

Por fim, a função ```CalcPosFixa()```

Duas outras funções auxiliares foram definidas: ```Prioridade()``` e ```ImprimirResultado```




[link para o script](posfixa.py)