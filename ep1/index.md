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

Os detalhes do enunciado, junto com exemplos, podem ser consultados no link abaixo.

**[Link para o enunciado](enunciado.pdf)**

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

Já o tipo ```Complexo``` é mais elaborado, contendo: alguns nomes de classe para verificação de tipo; atributos ```.Re``` e ```.Im``` para partes real e imaginária, sem getters ou setters devido à ausência de acesso por parte do usuário; representações via ```__str__``` e ```__repr__```, sendo esta última necessária para avaliar expressões via ```eval()```; operadores unários ```+``` , ```-``` e ```conj()``` (conjugado, usado para implementar a divisão); operadores binários ```+```, ```-```, ```*``` e ```/```, implementando a checagem de divisão por zero. Na manipulação dos caracteres, para distinguir a adição e a subtração unária, elas foram respectivamente transformadas em ```#``` e ```_```.

Os nomes de classe foram usados não somente na função construtora (aceitando ```int``` ou ```float```), mas também para viabilizar operações com um ```Complexo``` na primeira posição e um ```int``` ou ```float``` na segunda posição. Já a inversão dessas posições (primeiro ```int``` | ```float``` depois ```Complexo```) foi possibilitada apenas na função de cálculo da expressão (```CalcPosFixa```) usando o artifício de transformar esses tipos em ```Complexo```, para evitar a construção de novos objetos estendendo as classes ```int``` e ```float```.

Funções auxiliares foram usadas primordialmente para converter a string fornecida pelo usuário em uma lista contendo operadores e operandos, esses últimos já transformados em ```Complexo``` quando necessário. A função ```TraduzPosFixa()``` recebe a string, chama as funções auxiliares (envolvidas em uma função chamada ```ProcessarInput()```), e opera o algoritmo padrão de tradução para notação pós-fixa, dado no enunciado, retornando uma lista com os operadores e operandos nesta nova ordem. O fluxo da string de input ao passar pela ```TraduzPosFixa()```, incluindo funções auxiliares, é da seguinte forma:

|      |       |        |     |    |    |   |     |  |  |
|:-----:|:--------:|:------:|:----:|:----:|:----:|:---:|:-----:|:---:|:-----:|
| **Função** | | ```Tokenizar``` |  | ```SubsComplexos``` | | ```SubsUnarios``` |  | algoritmo de ```TraduzPosFixa``` |
| **Tipo** | string | $\rightarrow$ | lista | $\rightarrow$ | lista |$\rightarrow$ | lista | $\rightarrow$ | lista |
| **Conceito** | input | $\rightarrow$ | tokens | $\rightarrow$ | complexos detectados | $\rightarrow$ | unários detectados | $\rightarrow$ | pós-fixa |
| **Exemplo** | ```(2 + 3i) * -10``` | $\rightarrow$ | ```['(', '2', '+', '3i' , ')', '*', '-', '10']``` | $\rightarrow$ | ```[Complexo(2, 3), '*', '-', '10']``` | $\rightarrow$ | ```[Complexo(2, 3), '*', '_', '10']``` | $\rightarrow$ | ```[Complexo(2.0, 3.0), '10', '_', '*']```| 

O algoritmo de tradução, principal loop da função ```TraduzPosFixa()```, que percorre a lista de operadores e operandos, foi implementado usando-se duas pilhas: uma estocando operadores e outra estocando a tradução para notação pós-fixa. Operandos são colocados automaticamente na pilha de tradução; já um abre parênteses é colocado automaticamente na pilha de operadores. Um operador de prioridade superior ao atual topo é colocado na pilha de operadores, enquanto um operador com prioridade menor que ou igual à do atual topo desempilha (joga na pilha de tradução) o operador do topo atual, repetindo até esta condição cessar, sendo em seguida empilhado na pilha de operadores. O fecha parênteses desempilha todos os operadores até encontrar o abre parênteses mais próximo ao topo, sendo ambos os parênteses descartados. O que sobrar na pilha de operadores ao final deste processo é desempilhado em sucessão até esvaziar a pilha de operadores. A pilha de expressão pós-fixa está completa e é convertida em lista.

Em seguida, a função obrigatória ```CalcPosFixa()``` pega essa lista e lhe aplica o algoritmo de cálculo de expressão aritmética pós-fixa. Este algoritmo usa uma única pilha, que vai estocando os operandos em ordem até encontrar um operador, momento em que desempilha o(s) operando(s) do topo, lhe(s) aplica a operação, e empilha o resultado. Ao final, sobra um único número na pilha, que é retornado. Visto que o enunciado solicitou que essa função retornasse ```None``` no caso de expressões inválidas, foram implementados condicionais e mecanismos de tratamento de exceções ao longo de todo o fluxo de funções acima, passando ```None``` sempre adiante caso ocorresse um problema em algum ponto.

Duas outras funções auxiliares foram definidas: ```Prioridade()``` e ```ImprimirResultado()```. A primeira estabeleceu a ordem de prioridade dos operadores, prevendo também os casos especiais do operando (prioridade ```0```) e dos parênteses (prioridades elevadas). Esta função foi usada como o principal mecanismo de condicional nos algoritmos. Já a segunda é chamada apenas ao final de ```CalcPosFixa()```, para imprimir o resultado no prompt conforme a especificação.

O usuário que quiser interagir com o programa pode baixar o script no link abaixo e, usando alguma versão compatível de Python, executá-lo no prompt de comando.

**[Link para o script](posfixa.py)**