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

<div align="right" style="font-size: smaller;"><a ref="enunciado.pdf"><b>ENUNCIADO COMPLETO EM PDF</b></a></div>
<p></p>

* O usuário insere uma string em um prompt idêntico ao do Python (que aguarda um input depois de ```>>>```) e recebe o resultado logo em seguida, podendo inserir nova expressão sempre que quiser.
* Todo número complexo será inserido com a sintaxe ```(a + bi)``` (e variações de sinal), com ```a``` e ```b``` sendo ```int``` ou ```float```. Isso difere da sintaxe padrão do Pyhton, que usa ```j``` para sinalizar a parte imaginária.
* Espaços em branco não prejudicam o input.
* Os operadores permitidos no input são as quatro operações binárias da aritmética (```+```, ```-```, ```*``` e ```/```) e os sinais unários (```+``` e ```-```), além de abre e fecha parênteses ```()``` para fins de agrupamento.
* O programa deve definir e usar obrigatoriamente quatro objetos:
    - uma classe chamada ```Complexo``` que construa um número complexo e permita todas as operações acima; 
    - uma classe chamada ```Pilha``` que implemente a estrutura de dado de uma pilha, com API minimal;
    - uma função chamada ```TraduzPosFixa()``` que recebe a expressão aritmética do usuário e a traduz para a notação pós-fixa em formato de lista; e
    - uma função chamada ```CalcPosFixa()``` que recebe uma lista em notação pós-fixa e retorna um ```Complexo()``` contendo o resultado, imprimindo-o na tela no formato ```(a + bi)``` ou ```(a +bi)``` (e variações de sinal).
* Caso o input esteja em formato inválido, deve ser retornado ```None```.
* O programa de estar todo contido em um único script de nome ```posfixa.py```.

## Descrição da resolução

<div align="right" style="font-size: smaller;"><a ref="posfixa.py"><b>SCRIPT COMPLETO EM .PY</b></a></div>
<p></p>