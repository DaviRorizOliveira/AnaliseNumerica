import os
from sympy import *
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Função que plota o gráfico da função exata e encontrada pelo método
def grafico(func, x0, y0, h, n, yb, shooting_result):
    f = lambdify((symbols('x'), symbols('y')), func, 'math')
    
    resultado = shooting_result
    solucao_exata = solucao(func, x0, y0, symbols('x'))
    
    x_vals = [x for x, y in resultado]
    y_aprox = [y for x, y in resultado]
    y_exato = [solucao_exata.subs(symbols('x'), x) for x in x_vals]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_aprox, marker='o', linestyle='-', color='b', label='Estimativa pelo metodo das diferencas finitas')
    plt.plot(x_vals, y_exato, linestyle='--', color='r', label='Solucao Exata')
    plt.title('Comparacao entre Metodo das diferencas finitas e Solucao Exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Função para calcular a solução exata da EDO utilizando funções prontas do sympy
def solucao(func, x0, y0, x):
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    return sol.rhs

# Função do método das diferenças finitas
def diferencasFinitas(f, x0, y0, h, n, yb):
    def boundary_condition(z):
        y = [0] * (n + 1)
        y[0] = y0
        for i in range(1, n + 1):
            y[i] = y[i - 1] + h * f(x0 + (i - 1) * h, y[i - 1])
        return y[-1] - yb
    
    z0 = fsolve(boundary_condition, [y0])
    y = [0] * (n + 1)
    y[0] = y0
    for i in range(1, n + 1):
        y[i] = y[i - 1] + h * f(x0 + (i - 1) * h, y[i - 1])
    
    results = [(x0 + i * h, y[i]) for i in range(n + 1)]
    return results

def main():
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    entradas = []

    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            func = sympify(lines[i].strip())
            x0 = float(lines[i + 1].strip())
            y0 = float(lines[i + 2].strip())
            h = float(lines[i + 3].strip())
            n = int(lines[i + 4].strip())
            yb = float(lines[i + 5].strip())

            entradas.append((func, x0, y0, h, n, yb))
            i += 6

    with open(outputs, "w") as arq:
        for func, x0, y0, h, n, yb in entradas:
            f = lambdify((symbols('x'), symbols('y')), func, 'math')
            
            resultado = diferencasFinitas(f, x0, y0, h, n, yb)
            solucao_exata = solucao(func, x0, y0, symbols('x'))
            
            arq.write(f'Estimativa pelo metodo das diferencas finitas:\n')
            for x, y in resultado:
                yExato = solucao_exata.subs(symbols('x'), x)
                erro = round(float(((y - yExato) / yExato) * 100), 2) if yExato != 0 else 0
                
                arq.write(f'x: {x}, y: {y}\n')
                arq.write(f'y_exato: {yExato}\n')
                arq.write(f'Erro: {erro}%\n')
            arq.write('\n')

            grafico(func, x0, y0, h, n, yb, resultado)

if __name__ == "__main__":
    main()