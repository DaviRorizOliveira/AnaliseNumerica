import os
from sympy import *

# Função que calcula os valores da função em um ponto X determinado
def fx(expression, value):
    expression_parts = expression.split('x')
    evaluated_expression = ('(' + str(value) + ')').join(expression_parts)
    return eval(str(evaluated_expression))

# Função com a fórmula da regra de Simpson 3/8
def simpson(func, intervalo, n):
    a, b = intervalo
    h = (b - a) / n
    result = fx(func, a) + fx(func, b)

    for i in range(1, n, 3):
        result += 3 * (fx(func, a + i * h) + fx(func, a + (i + 1) * h))

    for i in range(3, n - 1, 3):
        result += 2 * fx(func, a + i * h)

    return 3 * h * result / 8

def main():
    # Obtém o diretório atual do arquivo e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    x = Symbol("x")

    # Lista para armazenar as funções e intervalos
    entradas = []

    # Lê as entradas do arquivo de entrada
    with open(inputs, "r") as arq:
        for linha in arq:
            # Divide a linha de leitura em 3 intervalos
            aux = linha.strip().split(";")
            func = aux[0]
            a = float(aux[1])
            b = float(aux[2])
            n = int(aux[3])

            entradas.append((func, (a, b), n))

    # Calcula a integral para cada entrada e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for func, intervalo, n in entradas:
            # Função pronta para calcular a integral a fim de mostrar as diferenças
            integral = integrate(func, (x, a, b))
            resultado = simpson(func, intervalo, n)
            
            arq.write(f'Integral correta: {integral}\n')
            arq.write(f'Estimativa de Simpson 3/8: {resultado}\n')
            if len(func) < len(entradas) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()