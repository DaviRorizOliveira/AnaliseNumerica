import os
from sympy import *

# Função que calcula os valores da função nos pontos 'a' e 'b'
def fx(func, valorX):
    aux = func.split('x')
    valorY = ('(' + str(valorX) + ')').join(aux)
    return eval(str(valorY))

# Função com a fórmula do trapézio (Modificada para retornar a altura)
def trapezio(func, intervalo, n):
    a, b = intervalo
    h = (b - a) / n
    result = 0.5 * (fx(func, a) + fx(func, b))

    for i in range(1, n):
        result += fx(func, a + i * h)

    return h * result, h

# Função com a fórmula da extrapolação de Richards, que tem como parâmetros os valores de dois trapézios e suas respectivas alturas
def richards(trap1, h1, trap2, h2):
    return trap2 + (1 / ((h1 / h2) * (h1 / h2) - 1)) * (trap2 - trap1)

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
            arq.write(f'Integral correta: {integral}\n')
            
            # Calcula um total de 3 trapézios para atingir um valor mais exato
            trap1, h1 = trapezio(func, intervalo, n)
            trap2, h2 = trapezio(func, intervalo, n * 2)
            trap3, h3 = trapezio(func, intervalo, n * 4)
            
            # Calcula a extrapolação de Richards entre o trap1 com o trap2, e o trap2 com o trap3
            result1 = richards(trap1, h1, trap2, h2)
            result2 = richards(trap2, h2, trap3, h3)
            
            # Calcula o resultado final
            resultado = richards(result1, h1, result2, h3)
            arq.write(f'Estimativa da extrapolacao de richards: {resultado}\n')
            
            erro = round(((integral - resultado) / integral) * 100, 2)
            arq.write(f'Erro: {erro}%\n')

if __name__ == "__main__":
    main()