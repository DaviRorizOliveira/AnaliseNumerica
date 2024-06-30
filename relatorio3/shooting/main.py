import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Function, Eq, dsolve, lambdify, sympify

# Função que plota o gráfico da função exata e a estimada pelo método de shooting
def grafico(func, x0, y0, h, n, yb, shooting_result):
    f = lambdify((symbols('x'), symbols('y')), func, 'numpy')
    
    resultado = shooting_result
    solucao_exata = solucao(func, x0, y0, symbols('x'))
    
    x_vals = np.array([x for x, y in resultado])
    y_aprox = np.array([y for x, y in resultado])
    y_exato = np.array([solucao_exata.subs(symbols('x'), x) for x in x_vals])
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_aprox, marker='o', linestyle='-', color='b', label='Estimativa pelo método de Shooting')
    plt.plot(x_vals, y_exato, linestyle='--', color='r', label='Solução Exata')
    plt.title('Comparação entre Método de Shooting e Solução Exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Função para calcular o método de Runge-Kutta de 4ª ordem
def hungeKutta(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)
        y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
        results.append((x, y))
    
    return results

# Função para calcular a solução exata da EDO utilizando funções do sympy
def solucao(func, x0, y0, x):
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    return sol.rhs

# Função do método de Shooting
def shooting(f, x0, y0, h, n, yb):
    def residual(z):
        results = hungeKutta(f, x0, y0, h, n)
        xb, yb_approx = results[-1]
        return yb_approx - yb
    
    z0 = fsolve(residual, y0)
    return hungeKutta(f, x0, z0[0], h, n)

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
            f = lambdify((symbols('x'), symbols('y')), func, 'numpy')
            
            resultado = shooting(f, x0, y0, h, n, yb)
            solucao_exata = solucao(func, x0, y0, symbols('x'))
            
            arq.write(f'Estimativa pelo método de Shooting:\n')
            for x, y in resultado:
                y_exato = solucao_exata.subs(symbols('x'), x)
                erro = round(float(((y - y_exato) / y_exato) * 100), 2) if y_exato != 0 else 0
                
                arq.write(f'x: {x}, y: {y}\n')
                arq.write(f'y_exato: {y_exato}\n')
                arq.write(f'Erro: {erro}%\n')
            arq.write('\n')

            grafico(func, x0, y0, h, n, yb, resultado)

if __name__ == "__main__":
    main()