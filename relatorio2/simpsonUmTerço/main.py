import os
from sympy import *

# Função que calcula os valores da função nos pontos 'a' e 'b'
def fx(func, valorX):
    aux = func.split('x')
    valorY = ('(' + str(valorX) + ')').join(aux)
    return eval(str(valorY))

# Função com a fórmula da regra de Simpson de 1/3
def simpson(func, intervalo, n):
    a, b = intervalo
    h = (b - a) / n
    result = fx(func, a) + fx(func, b)

    for i in range(1, n, 2):
        result += 4 * fx(func, a + i * h)

    for i in range(2, n - 1, 2):
        result += 2 * fx(func, a + i * h)

    return h * result / 3

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
            arq.write(f'Estimativa de Simpson 1/3: {resultado}\n')
            if len(func) < len(entradas) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()