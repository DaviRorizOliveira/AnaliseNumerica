import os
from sympy import *
import matplotlib.pyplot as plt

# Funcao que plota o grafico da funcao exata e encontrada pelo metodo
def grafico(func, x0, y0, h, n):
    # Converte a função simbólica em uma função numérica
    f = lambdify((symbols('x'), symbols('y')), func, 'numpy')
    
    # Resultados de todos os métodos
    resultados = {
        'Euler': euler(f, x0, y0, h, n),
        'Heun': heun(f, x0, y0, h, n),
        'Euler Modificado': euler_modificado(f, x0, y0, h, n),
        'Ralston': ralston(f, x0, y0, h, n),
        'Hunge-Kutta 3': hungeKutta3(f, x0, y0, h, n),
        'Hunge-Kutta 4': hungeKutta(f, x0, y0, h, n)
    }
    
    # Calculando a solução exata
    solucao_exata = solucao(func, x0, y0, symbols('x'))
    x_vals = [x for x, y in resultados['Euler']]  # Pegando os valores de x de qualquer um dos métodos

    # Plotando os resultados
    plt.figure(figsize=(12, 7))
    
    # Plotando a solução exata
    plt.plot(x_vals, [solucao_exata.subs(symbols('x'), x) for x in x_vals], 'k--', label='Solução Exata')
    
    # Plotando os resultados de cada método
    for metodo, resultado in resultados.items():
        y_vals = [y for x, y in resultado]
        plt.plot(x_vals, y_vals, marker='o', linestyle='-', label=metodo)

    plt.title('Comparação entre Métodos Numéricos e Solução Exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

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

# Funcao para calcular o metodo de Heun
def heun(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h, y + k1)
        y += (k1 + k2) / 2
        x += h
        results.append((x, y))
    
    return results

# Funcao para calcular o metodo de Euler Modificado
def euler_modificado(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        y += k2
        x += h
        results.append((x, y))
    
    return results

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

# Funcao para calcular o metodo de Hunge-Kutta de 3 ordem
def hungeKutta3(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h, y - k1 + 2 * k2)
        y += (k1 + 4 * k2 + k3) / 6
        x += h
        results.append((x, y))
    
    return results

# Funcao para calcular o metodo de Hunge-Kutta de 4 ordem
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

    for func, x0, y0, h, n in entradas:
        # Plotar os graficos
        grafico(func, x0, y0, h, n)

if __name__ == "__main__":
    main()