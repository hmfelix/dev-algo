# EP.3) Classificador de tabelas


## Objetivo

Escrever um programa que classifica uma tabela fornecida pela pessoa usuária usando os algoritmos *quick* e *merge*.

## Conceitos trabalhados

* Algoritmos de classificação
* Mensuração de tempo de execução e *benchmarking*
* Análise de complexidade de algoritmos
* Funções de ordenamento de tabelas
* Estabilidade de classificações
* Tabelas ou dicionários de despacho
* Modularização de programas
* Formato de datas

## Requisitos do enunciado

* Trabalha-se com o formato de tabelas csv (embora com extensão `.txt`), sem cabeçalhos, contendo três colunas:
    - Número de identificação (id)
    - Nome
    - Data
* A pessoa usuária fornece o nome de um arquivo localizado no mesmo diretório do programa contendo uma tabela no formato acima, cujas linhas podem estar em qualquer ordem. O programa importa a tabela sob a forma de uma lista de listas (linhas), sob o nome `TAB`.
* Depois, quantas vezes quiser, a pessoa usuária fornece o algoritmo de classificação (`q` para *quick* ou `m` para *merge*) e uma função de ordenação com sufixo `1` a `4`, conforme opções a seguir:
    - `comp1`: cresc. por nome - cresc. por data - cresc. por id.
    - `comp2`: cresc. por nome - decresc. por data - cresc. por id.
    - `comp3`: decresc. por data - cresc. por nome - cresc. por id.
    - `comp4`: cresc. por id. - cresc. por data - cresc. por nome
* O programa deve obrigatoriamente definir duas funções de classificação: `ClassificaMerge` e `ClassificaQuick`, implementando uma versão não recursiva dos algoritmos homônimos, e contar o tempo de execução do algoritmo. Aplicada a classificação, deve-se imprimir o tempo e os 100 primeiros elementos na tela.
* Inserir `fim` em qualquer estágio fecha o programa.
* O programa deve estar contido em dois scripts (neste projeto localizados na pasta ep3):
    - `Compara.py`, que contém apenas as funções de ordenação; e
    - `main.py`, que contém todo o resto do código e o programa em si.
* Foi fornecido um script para gerar automaticamente arquivos de tabelas já no formato dado. Este script foi adaptado sob o nome `gerador_testes.py` para gerar três arquivos cujo sufixo é o número de linhas (`arq[Nlinhas].txt`), todos salvos no mesmo diretório deste EP.

Este último ponto é apenas uma ferramenta e não fez parte da entrega.

Os detalhes do enunciado podem ser consultados no link abaixo.

**[Link para o enunciado](enunciado.pdf)**

Já o script gerador de arquivos de teste pode ser acessado abaixo:

**[Link para o script de gerador de tabelas](gerador_testes.py)**

## Descrição da resolução

Textualmente, o código de `main.py` está dividido em cinco partes:

0. dependências
1. funções obrigatórias
2. funções acessórias
3. dicionários auxiliares
4. programa

As dependências são apenas o script `Compara.py`, contendo as funções de ordenação, e a função `time` do módulo `time` da biblioteca padrão, usada para contagem do tempo de execução.

Os algoritmos aqui trabalhados são amplamente conhecidos.

O algoritmo *merge* parte de duas sublistas já ordenadas e **intercala** seus elementos para formar uma terceira lista, contendo todos os elementos das duas primeiras dispostos de maneira ordenada. Ao partir das menores sublistas possíveis, isto é, aquelas contendo um único elemento, o algoritmo vai intercalando sublistas cada vez maiores, chegando por fim em duas sublistas que dividem a totalidade da lista a ser classificada. A intercalação em si é feita pela função `intercalar`, cujas chamadas são coordenadas por `ClassificaMerge`. Como o enunciado exige que a lista `TAB` original seja modificada, foi necessário pensar em trocas de ordem, e não meramente na construção de uma nova lista, de forma que a `ClassificaMerge` recebe como argumentos a lista a ser alterada e suas duas sublistas, que juntas forma toda a lista.

Já o algoritmo *quick* elege um elemento como pivô e vai percorrendo a lista a partir dos extremos, trocando um elemento e o pivô de lugar e alternando o sentido do percurso sempre o pivô for maior (no sentido de percurso esq $\rightarrow$ dir) ou menor (dir $\rightarrow$ esq) que o elemento em questão. Depois de percorrer toda a lista, o pivô está em seu lugar final, visto que todos os elementos antes dele são menores e todos depois são maiores. Assim, restam sublistas à esquerda e à direita do pivô carecendo de classificação, chamadas de **partições**. Procedendo desta maneira, classificando sublistas cada vez menores, o algoritmo classifica toda a lista. O percurso e a troca de ordem na verdade são executados pela função acessória `particionar`, que retorna à `ClassificaQuick` o índice final do pivô, para futuro particionamento em sublistas.

Percebe-se que ambos os algoritmos têm um raciocínio recursivo. No entanto, o enunciado solicita uma implementação não recursiva. Para isso, na função `ClassificaMerge` foram usados laços que partem de sublistas contendo um elemento e vão intercalando a lista de cima para baixo, usando divisões por potências de $2$ e seus restos como critérios de condicional e controle de fluxo. A `ClassificaQuick`, por sua vez, usa uma pilha para estocar as sucessivas sublistas criadas a cada particionamento, e resolve a pilha com um laço de desempilhamento.

Tanto o *quick* como o *merge* variam em eficiência, tendo no caso médio complexidade $\mathcal{O}(n\log n)$. Não obstante, enquanto o primeiro possui complexidade $\mathcal{O}(n^2)$ no pior caso, o segundo continua tendo complexidade $\mathcal{O}(n\log n)$. De fato, em testes foi possível perceber a maior eficiência do *merge* em alguns casos.

As funções acessórias incluíram ainda:
* uma utilidade de impressão (`imprimir_classificacao`), que permite conferir o tempo, os parâmetros de classificação e os primeiros elementos classificados;
* a função de importação da tabela (`importarTAB`), que a converte para uma lista de listas; e
* a função `main`, que só é executada se o módulo `main.py` for executado e que interage com a pessoa usuária solicitando o arquivo e os parâmetros de classificação, chamando a função de classificação apropriada e imprimindo o resultado.

Finalmente, foram definidos dicionários acessórios, que permitiram despachar as funções de classificação (`despacho_metodo`) e ordenação (`despacho_comp`) conforme a escolha da pessoa usuária e imprimir corretamente o nome do método (`nome_metodo`) e a descrição da ordenação (`descricao_comp`).

Por sua vez, o script `Compara.py` está dividido em apenas três partes:

0. dependências
1. funções obrigatórias
2. função auxiliar

A única dependência é a classe `date` do módulo `datetime` (biblioteca padrão), usada pela única função auxiliar `as_date`, que converte a string de data em um objeto `date` para permitir sua ordenação.

Já as funções obrigatórias incluem as diferentes funções de ordenação que podem ser escolhidas pelo usuário (`compX`, onde `X` vai de `1` a `4`). A ordenação desejada é passada como argumento das funções de classificação e seus motores internos (`intercalar` ou `particionar`).

A vantagem dos scripts aqui desenvolvidos é que se pode definir qualquer função de ordenação no estilo das `compX`, e aplicá-la a qualquer tabela csv sem cabeçalhos, desde que esses dois elementos sejam interoperáveis, adequando-se a função de impressão caso se deseje usar a versão iterativa do programa.

O usuário que quiser interagir com o programa pode baixar os arquivos nos links abaixo, colocando-os em um mesmo repositório, e, usando alguma versão compatível de Python, executar o script principal no prompt de comando.

**[Link para o script principal](main.py)**

**[Link para a dependência - funções de comparação](Compara.py)**

**[Link para arquivo de tabela aleatória com 10.000 entradas](arq10000.txt)**

