import os
from sympy import *
import math

# Função que calcula os valores da função nos pontos 'a' e 'b'
def fx(func, valorX):
    aux = func.split('x')
    valorY = ('(' + str(valorX) + ')').join(aux)
    return eval(str(valorY))

# Função com a fórmula do trapézio
def trapezio(func, intervalo):
    h = (float(intervalo[1]) - float(intervalo[0]))
    return (h / 2) * (fx(func, intervalo[0]) + fx(func, intervalo[1]))

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

            entradas.append((func, (a, b)))

    # Calcula a integral para cada entrada e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for func, intervalo in entradas:
            # Função pronta para calcular a integral a fim de mostrar as diferenças
            integral = integrate(func, (x, a, b))
            resultado = trapezio(func, intervalo)
            erro = round(((integral - resultado) / integral) * 100, 2)
            
            arq.write(f'Integral correta: {integral}\n')
            arq.write(f'Estimativa do trapezio simples: {resultado}\n')
            arq.write(f'Erro: {erro}%\n')

if __name__ == "__main__":
    main()