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

# Funcao para calcular o erro percentual
def calcular_erro(y_numerico, y_exato):
    return round(((y_numerico - y_exato) / y_exato) * 100, 2)

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

            xExato = x0 + n * h

            resultado = euler(f, x0, y0, h, n)
            yExato = solucao(func, x0, y0, xExato)
            erro = round(((resultado[-1][1] - yExato) / resultado[-1][1]) * 100, 2)

            # Escreve o resultado no arquivo de saida
            arq.write(f'Estimativa pelo metodo de Euler para a funcao: "{func}" com x0 = {x0}, y0 = {y0}, h = {h}, n = {n}:\n')
            for x, y in resultado:
                arq.write(f'x: {x}, y: {y}\n')
            arq.write(f'Solucao exata para x = {xExato}: y = {yExato}\n')
            arq.write(f'Erro: {erro}%\n')
            arq.write(f'\n')

if __name__ == "__main__":
    main()