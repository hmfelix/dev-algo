# (0) Dependencias
import re


# (1) Classes obrigatorias
class Pilha:
    # construtor
    def __init__(self, lista_elementos=[]):
        if type(lista_elementos) is list:
            self.elementos = lista_elementos[:]
        else:
            raise TypeError('Argumento lista_elementos deve ser de tipo list.')
        return    None
    
    # metodos de consulta
    def __str__(self):
        return 'p' + str(self.elementos)
    
    def len(self):
        return len(self.elementos)
    
    def is_empty(self):
        return self.len() == 0
    
    def top(self):
        if self.is_empty():
            return None
        return self.elementos[-1]
    
    # metodos de modificacao
    def push(self, x):
        self.elementos.append(x)
        return None
    
    def pop(self):
        topo_atual = self.top()
        if topo_atual is None:
            return None
        self.elementos.pop()
        return topo_atual

class Complexo:
    # nomes de toda a classe: tipos aceitos para construcao ou operacao
    __crtypes = (int, float) # tipos de construcao
    def __is_crtype(self, x): # checa se x eh tipo de criacao
        return type(x) in Complexo.__crtypes
    def __is_optype(self, x): # checa se x eh tipo de operacao
        return type(x) in Complexo.__crtypes or type(x) is Complexo
    def __test_optype(self, x): # levanta excecao se x nao for tipo de operacao
        if not self.__is_optype(x):
            raise TypeError('Tentativa de operar Complexo com objetos sem ser int, float ou Complexo.')
        return None
    
    # construtor: aceita ints ou floats
    def __init__(self, real=0, imaginaria=0) -> None:
        if not (self.__is_crtype(real) and self.__is_crtype(imaginaria)):
            raise TypeError('Tipo das partes real e imaginaria devem ser int ou float.')
        self.Re = real
        self.Im = imaginaria

    # metodos de consulta
    # obs.: parte real e imaginaria podem ser consultadas pelo respectivo atributo
    def __str__(self):
        return f'Complexo({self.Re}, {self.Im})'
    
    def __repr__(self):
        return self.__str__()
    
    # operadores unarios
    def __neg__(self):
        return Complexo(-self.Re, -self.Im)
    
    def __pos__(self):
        return Complexo(+self.Re, +self.Im)
    
    def conj(self):
        return Complexo(self.Re, -self.Im)

    # comparacao (com ints, floats ou Complexo)
    def __eq__(c1, c2):
        if not c1.__is_optype(c2):
            return False
        if c1.__is_crtype(c2):
            if c1.Im != 0:
                raise TypeError('Complexo com parte imaginaria nao nula soh pode ser comparado com outro Complexo.')
            return c1.Re == c2
        else:
            return c1.Re == c2.Re and c1.Im == c2.Im

    # operadores binarios (com ints, floats ou Complexos)
    def __add__(c1, c2):
        c1.__test_optype(c2)
        if c1.__is_crtype(c2):
            return Complexo(c1.Re + c2, c1.Im)
        else:
            return Complexo(c1.Re + c2.Re, c1.Im + c2.Im)
        
    def __sub__(c1, c2):
        c1.__test_optype(c2)
        return c1 + (-c2)
    
    def __mul__(c1, c2):
        c1.__test_optype(c2)
        if c1.__is_crtype(c2):
            return Complexo(c1.Re * c2, c1.Im * c2)
        else:
            return Complexo(c1.Re * c2.Re - c1.Im * c2.Im, c1.Re * c2.Im + c1.Im * c2.Re)

    def __truediv__(c1, c2):
        c1.__test_optype(c2)
        if c1.__is_crtype(c2):
            if c2 == 0:
                raise ValueError('Nao pode ser feita divisao por zero.')
            return c1 * c2**(-1)
        else:
            if c2 == Complexo():
                raise ValueError('Nao pode ser feita divisao por zero.')
            denominador_real = c2.Re**2 + c2.Im**2
            numerador_complexo = c1 * c2.conj()
            return Complexo(numerador_complexo.Re / denominador_real, numerador_complexo.Im / denominador_real)


# (2) Funcoes obrigatorias

# recebe a string de input do usuario
# retorna uma lista em notacao pos-fixa ou None se o input for invalido
def TraduzPosFixa(input_str):
    # se o input for vazio, retorna None
    if input_str is None:
        return None

    simbolos = ProcessarInput(input_str) # funcao auxiliar definida mais adiante

    # se o output de ProcessarInput() for None, retorna None
    if simbolos is None:
        return None

    # sao usadas duas pilhas: 
    #  . uma para os operadores
    #  . outra para a expressao pos-fixa
    op = Pilha()
    pos_fixa = Pilha()

    # algoritmo de traducao para pos-fixa
    for simbolo in simbolos:
        nivel_simbolo = Prioridade(simbolo)

        if not nivel_simbolo: # simbolo eh operando
            pos_fixa.push(simbolo)

        elif nivel_simbolo in (1,2,3): # simbolo eh operador
            nivel_topo = Prioridade(op.top())
            if (nivel_simbolo > nivel_topo) or (nivel_topo >= 4): # se tem maior prioridade que o topo...
                                                                  # ...ou se topo eh um parenteses...
                op.push(simbolo) # ...empilha
            else: # se o topo eh um operador de maior prioridade...
                pos_fixa.push(op.pop()) # ...desempilha o topo...
                nivel_inferior = Prioridade(op.top()) 
                while nivel_inferior >= nivel_simbolo and nivel_inferior in (1,2,3):
                # ...checa se novo topo tem maior prioridade e ainda eh um operador...
                    pos_fixa.push(op.pop()) # ...se tiver, desemplilha novamente e repete...
                    nivel_inferior = Prioridade(op.top())
                op.push(simbolo) # ...ao final, empilha o simbolo atual (operador de menor prioridade)

        elif nivel_simbolo == 4: # simbolo eh abre parenteses
            op.push(simbolo)
        
        elif nivel_simbolo == 5: # simbolo eh fecha parenteses
            while Prioridade(op.top()) < 4: # enquanto nao encontra abre parenteses...
                pos_fixa.push(op.pop()) # ...desempilha
                
                # PROBLEMA NESTE LOOP
            
            op.pop() # descarta o abre parenteses encontrado

    # desempilha toda a pilha de operadores
    while not op.is_empty():
        pos_fixa.push(op.pop())

    return pos_fixa.elementos


# recebe lista contendo expressao em notacao pos fixa
# retorna o valor calculado a partir da expressao
# (ou None se houver algum problema)
def CalcPosFixa(pos_fixa):
    # se o output de TraduzPosFixa tiver sido None, retorna None
    if pos_fixa is None:
        return None
    
    # usa-se uma pilha para ir estocando os operandos
    # e aplicando os operadores
    calculo = Pilha()

    try: 
        # algoritmo
        for simbolo in pos_fixa:
            nivel = Prioridade(simbolo)
            if nivel == 0: # se o simbolo eh operando...
                try: # ...se for int ou float, o transforma em Complexo...
                    numero = float(simbolo)
                    simbolo = Complexo(numero)
                
                except TypeError: # ...se jah for Complexo, segue...
                    pass
                calculo.push(simbolo) # ...e o empilha
                
            elif simbolo == '_': # se o simbolo eh negativo unario...
                operando_1 = str(calculo.pop())
                expr_a_avaliar = '-' + operando_1
                elemento_calculado = eval(expr_a_avaliar, globals())
                calculo.push(elemento_calculado)
            else: # se o simbolo eh operador binario...
                operando_2 = str(calculo.pop())
                operando_1 = str(calculo.pop())
                expr_a_avaliar = operando_1 + simbolo + operando_2
                elemento_calculado = eval(expr_a_avaliar, globals())
                calculo.push(elemento_calculado)
        resultado = calculo.elementos[0]
        ImprimirResultado(resultado)
        return resultado
    
    except Exception:
        return None

            
# (3) Funcoes auxiliares        

# usa a expressao regular fornecida pelo enunciado para tokenizar
# a string recebida do usuario
# retorna uma lista de tokens
def Tokenizar(expr):
    reg_expr = r"(\b\d*[\.]?\d+[i]?\b|[\(\)\+\*\-\/\%])"
    return re.findall(reg_expr, expr)

# na lista retornada pela funcao Tokenizar, substitui os
# tokens referentes a numeros complexos por objetos do tipo Complexo
# retorna lista de operadores e operandos, 
# potencialmente contendo objetos do tipo Complexo
# retorna None se houver algum problema
def SubsComplexos(token_list):
    placeholder = '-->to_del<--' # marca elementos a serem deletados ao final
    tl_copy = token_list[:] # copia: evita sobrescrever a lista passada como argumento
    for k, token in enumerate(token_list):
        if 'i' in token: # sempre que encontar i...
            end = k+2 # ...marcar o indice final...
            try: 
                b = float(token_list[k-1] + token[:-1]) # ...parte Im e seu sinal...
            except ValueError:
                return None # (se houver problema no input do usuario, retorna None)
            real_abs = token_list[k-2] # ...valor abs da parte Re...
            real_op = '+' # ...sinal default da parte Re...
            beg = k-3 # ...inicio default do numero na tokenizacao...
            if token_list[k-3] != '(': # ...caso haja sinal da parte Re...
                real_op = token_list[k-3] # ...pega o sinal correto...
                beg = k-4 # ...ajusta o inicio do numero na tokenizacao...
            try: 
                a = float(real_op + real_abs) # ...parte Re e seu sinal...
            except ValueError:
                return None # se houver algum problema no input do usuario, retorna None
            tl_copy[beg:end] = [placeholder] * (end-beg) # ...troca tokens por placeholder...
            tl_copy[k] = Complexo(a, b) # ... insere o numero Complexo no lugar atual
    result = [elem for elem in tl_copy if elem != placeholder] # tira placeholders
    return result

# retorna a prioridade do operador, ou 0 se for operando
def Prioridade(char):
    if char == '+' or char == '-':
        return 1
    elif char == '*' or char == '/':
        return 2
    elif char == '#' or char == '_':
        return 3
    elif char == '(':
        return 4
    elif char == ')':
        return 5
    else:
        return 0

# na lista de operadores e operandos (i.e., lista retornada pela funcao
# SubsComplexos()), substitui + e - unarios respectivamente por # e _
# retorna a lista de operadores e operandos com tais operadores unarios
# renomeados, se houver
def SubsUnarios(op_list):
    # se o output de SubsComplexos() tiver sido None, retorna None
    if op_list is None:
        return None

    substituicao = {'+': '#', '-':'_'}
    ol_copy = op_list[:]
    for k, op in enumerate(op_list):
        # hipotese do unario no inicio da expressao
        if (op == '+' or op == '-') and k == 0:
            ol_copy[k] = substituicao[op]
        # hipotese do unario logo depois de operador ou abre parenteses
        elif (op == '+' or op == '-') and (Prioridade(op_list[k-1]) in (1,2,3,4)):
            ol_copy[k] = substituicao[op]
    return ol_copy

# funcao que apenas junta as funcoes auxiliares acima para produzir uma
# lista apta a ser passada ao algoritmo de transformacao em notacao pos-fixa
def ProcessarInput(input):
    as_tokens = Tokenizar(input)
    as_complexos = SubsComplexos(as_tokens)
    as_unarios = SubsUnarios(as_complexos)

    # se o output de SubsUnarios tiver sido None, retorna None
    if as_unarios is None:
        return None
    return as_unarios

# imprime um numero complexo na forma requerida pelo enunciado
# (chamada ao final da funcao CalPosFixa)
def ImprimirResultado(resultado):
    if type(resultado) is not Complexo:
        resultado_complexo = Complexo(resultado)
    else: 
        resultado_complexo = resultado
    if resultado_complexo.Im > 0:
        a_printar_Im = '+' + str(resultado_complexo.Im)
    else:
        a_printar_Im = resultado_complexo.Im
    print(f'({resultado_complexo.Re} {a_printar_Im}i)')


# (4) Programa
if __name__ == '__main__':
    while True:
        texto = input('>>>')
        pos = TraduzPosFixa(texto)
        calculo = CalcPosFixa(pos)