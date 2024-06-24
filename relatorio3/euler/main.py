import os
from sympy import *

# Funcao para calcular o metodo de Euler
def euler(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        y += h * f(x, y)
        x += h
        results.append((x, y))
    
    return results

# Funcao para calcular a solucao exata da EDO
def solucao(func, x0, y0, xFinal):
    x = symbols('x')
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    y_exact = sol.rhs.subs(x, xFinal)
    return y_exact

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
            
            # Le os valores iniciais e parametros
            x0 = float(lines[i + 1].strip())
            y0 = float(lines[i + 2].strip())
            h = float(lines[i + 3].strip())
            n = int(lines[i + 4].strip())

            entradas.append((func, x0, y0, h, n))
            i += 5

    # Calcula o metodo para cada entrada e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for func, x0, y0, h, n in entradas:
            # Converte a funcao simbolica em uma funcao numerica
            f = lambdify((symbols('x'), symbols('y')), func, 'math')
            resultado = euler(f, x0, y0, h, n)
            
            # Escreve o resultado no arquivo de saida
            for x, y in resultado:
                arq.write(f'x: {x}, y: {y}\n')
            
            # Calcular e escrever a solucao exata no arquivo de saida
            x_final = x0 + n * h
            y_exact = solucao(func, x0, y0, x_final)
            arq.write(f'Solucao exata para x={x_final}: y={y_exact}\n')

if __name__ == "__main__":
    main()