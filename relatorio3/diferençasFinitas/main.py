import os
from sympy import *
import math

# Funcao para calcular o metodo de Hunge-Kutta de 4 ordem para sistemas de EDOs
def hungeKuttaSistemasDiferenciais(f1, f2, x0, y0, y1, h, n):
    x = x0
    y = y0
    z = y1
    results = [(x, y, z)]

    for i in range(n):
        k1_y = h * f1(x, y, z)
        k1_z = h * f2(x, y, z)
        
        k2_y = h * f1(x + h / 2, y + k1_y / 2, z + k1_z / 2)
        k2_z = h * f2(x + h / 2, y + k1_y / 2, z + k1_z / 2)
        
        k3_y = h * f1(x + h / 2, y + k2_y / 2, z + k2_z / 2)
        k3_z = h * f2(x + h / 2, y + k2_y / 2, z + k2_z / 2)
        
        k4_y = h * f1(x + h, y + k3_y, z + k3_z)
        k4_z = h * f2(x + h, y + k3_y, z + k3_z)
        
        y += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6
        z += (k1_z + 2 * k2_z + 2 * k3_z + k4_z) / 6
        x += h
        results.append((x, y, z))
    
    return results

# Funcao para calcular a solucao exata da EDO utilizando funcoes prontas do sympy
def solucao(func1, func2, x0, y0, y1):
    x = symbols('x')
    y = Function('y')(x)
    z = Function('z')(x)

    edo1 = Eq(y.diff(x), func1.subs({'y': y, 'z': z}))
    edo2 = Eq(z.diff(x), func2.subs({'y': y, 'z': z}))

    sol = dsolve((edo1, edo2), ics={y.subs(x, x0): y0, z.subs(x, x0): y1})
    sol_y = sol[0].rhs
    sol_z = sol[1].rhs

    return sol_y, sol_z

# Funcao para resolver o problema pelo metodo das diferencas finitas
def finite_difference_method(func1, func2, x0, y0, xb, yb, h, n):
    def f1(x, y, z):
        return func1.subs({'x': x, 'y': y, 'z': z}).evalf()

    def f2(x, y, z):
        return func2.subs({'x': x, 'y': y, 'z': z}).evalf()

    x = [x0 + i * h for i in range(n + 1)]
    y = [0] * (n + 1)
    z = [0] * (n + 1)

    # Condições iniciais
    y[0] = y0
    z[0] = yb

    # Aplicando o método das diferenças finitas
    for i in range(n):
        y[i+1] = y[i] + h * f1(x[i], y[i], z[i])
        z[i+1] = z[i] + h * f2(x[i], y[i], z[i])

    return x, y, z

def calcular_erro(aproximado, exato):
    if exato == 0:
        return 0
    else:
        return abs((aproximado - exato) / exato) * 100

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
            xb = float(lines[i + 4].strip())
            yb = float(lines[i + 5].strip())
            h = float(lines[i + 6].strip())
            n = int(lines[i + 7].strip())

            entradas.append((func1, func2, x0, y0, xb, yb, h, n))
            i += 8

    # Calcula o metodo para cada entrada e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for func1, func2, x0, y0, xb, yb, h, n in entradas:
            x, y, z = finite_difference_method(func1, func2, x0, y0, xb, yb, h, n)
            solucao_exata_y, solucao_exata_z = solucao(func1, func2, x0, y0, yb)
            
            # Escreve os resultados no arquivo de saida
            arq.write(f'Solucao pelo metodo das diferencas finitas:\n')
            for j in range(n + 1):
                yExato = solucao_exata_y.subs(symbols('x'), x[j]).evalf()
                zExato = solucao_exata_z.subs(symbols('x'), x[j]).evalf()
                
                erro_y = calcular_erro(y[j], yExato)
                erro_z = calcular_erro(z[j], zExato)
                
                arq.write(f'x: {x[j]}, y1: {y[j]}, y2: {z[j]}\n')
                arq.write(f'y1_exato: {yExato}, y2_exato: {zExato}\n')
                arq.write(f'Erro y1: {erro_y:.2f}%, Erro y2: {erro_z:.2f}%\n')
            arq.write('\n')

if __name__ == "__main__":
    main()