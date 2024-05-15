import os
from sympy import *

# Funcao com a formula da regra de Simpson 3/8
def simpson(func, intervalo, n):
    a, b = intervalo
    h = (b - a) / n
    result = func.subs(x, a) + func.subs(x, b)

    for i in range(1, n, 3):
        result += 3 * (func.subs(x, a + i * h) + func.subs(x, a + (i + 1) * h))

    for i in range(3, n - 1, 3):
        result += 2 * func.subs(x, a + i * h)

    return 3 * h * result / 8

def main():
    # Obtem o diretorio atual do arquivo e cria os caminhos para os arquivos de entrada e saida
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    # Lista para armazenar as funcoes e intervalos
    entradas = []

    # Le as entradas do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Le a funcao
            func = sympify(lines[i].strip())
            
            # Le os limites do intervalo
            a = float(lines[i + 1].strip())
            b = float(lines[i + 2].strip())
            
            # Le o numero de subdivisoes
            n = int(lines[i + 3].strip())

            entradas.append((func, (a, b), n))
            i += 4

    # Calcula a integral para cada entrada e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for func, intervalo, n in entradas:
            # Funcao pronta para calcular a integral a fim de mostrar as diferencas
            integral = integrate(func, (x, intervalo[0], intervalo[1]))
            arq.write(f'Integral correta: {integral}\n')
            
            # Calcula o resultado final
            resultado = simpson(func, intervalo, n)
            arq.write(f'Estimativa de Simpson 3/8: {resultado}\n')
            
            # Porcentagem de erro em relacao a integral correta
            erro = round(((integral - resultado) / integral) * 100, 2)
            arq.write(f'Erro: {erro}%\n')

if __name__ == "__main__":
    x = Symbol("x")
    main()