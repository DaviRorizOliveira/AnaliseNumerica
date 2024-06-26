import os
from sympy import *

# Funcao para calcular o metodo de Ralston
def ralston(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + 3 * h / 4, y + 3 * k1 / 4)
        y += (k1 + 2 * k2) / 3
        x += h
        results.append((x, y))
    
    return results

# Funcao para calcular a solucao exata da EDO utilizando funcoes prontas do sympy
def solucao(func, x0, y0, x):
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    return sol.rhs

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
            
            resultado = ralston(f, x0, y0, h, n)
            solucao_exata = solucao(func, x0, y0, symbols('x'))
            
            arq.write(f'Estimativa pelo metodo de Ralston:\n')
            for x, y in resultado:
                yExato = solucao_exata.subs(symbols('x'), x)
                erro = round(((y - yExato) / yExato) * 100, 2)
                
                arq.write(f'x: {x}, y: {y}\n')
                arq.write(f'y_exato: {yExato}\n')
                arq.write(f'Erro: {erro}%\n')
            arq.write('\n')

if __name__ == "__main__":
    main()