import os
from sympy import symbols, Function, Eq, dsolve, lambdify, sympify
from scipy.optimize import root

# Função para calcular o método de Runge-Kutta de quarta ordem para sistemas de EDOs
def hungeKutta_system(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = [h * fi(*y) for fi in f]
        k2 = [h * fi(*(y + 0.5 * k1_i for y, k1_i in zip(y, k1))) for fi in f]
        k3 = [h * fi(*(y + 0.5 * k2_i for y, k2_i in zip(y, k2))) for fi in f]
        k4 = [h * fi(*(y + k3_i for y, k3_i in zip(y, k3))) for fi in f]
        y = [y + (k1_i + 2 * k2_i + 2 * k3_i + k4_i) / 6 for y, k1_i, k2_i, k3_i, k4_i in zip(y, k1, k2, k3, k4)]
        x += h
        results.append((x, y))

    return results

# Função para calcular a solução exata da EDO utilizando funções prontas do sympy
def solucao(func, x0, y0, x):
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    return sol.rhs

# Função para o método de shooting
def shooting(f, x0, y0, xf, yf, h):
    def objective(shooting_param):
        result = hungeKutta_system(f, x0, [y0, shooting_param], h, int((xf - x0) / h))
        return result[-1][1][0] - yf

    # Encontrar o valor inicial correto para y'
    shooting_param = root(objective, 0).x[0]
    
    return hungeKutta_system(f, x0, [y0, shooting_param], h, int((xf - x0) / h))

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
            # Le as funcoes
            func1 = sympify(lines[i].strip())
            func2 = sympify(lines[i + 1].strip())
            
            # Le os valores iniciais e parametros
            x0 = float(lines[i + 2].strip())
            y0 = float(lines[i + 3].strip())
            xf = float(lines[i + 4].strip())
            yf = float(lines[i + 5].strip())
            h = float(lines[i + 6].strip())

            entradas.append(([func1, func2], x0, y0, xf, yf, h))
            i += 7

    # Calcula o metodo para cada entrada e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for funcs, x0, y0, xf, yf, h in entradas:
            # Converte a função simbólica em uma função numérica
            f = [lambdify((symbols('T'), symbols('z')), func, 'math') for func in funcs]
            
            resultado = shooting(f, x0, y0, xf, yf, h)
            
            arq.write(f'Estimativa pelo método de Shooting:\n')
            for x, y in resultado:
                arq.write(f'x: {x}, T: {y[0]}, z: {y[1]}\n')
            arq.write('\n')

if __name__ == "__main__":
    main()