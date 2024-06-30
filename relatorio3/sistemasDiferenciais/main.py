import os
from sympy import *
import matplotlib.pyplot as plt

# Funcao que plota o grafico da funcao exata e encontrada pelo metodo
def grafico(resultado, solucao_exata_y, solucao_exata_z):
    x_vals = [x for x, y, z in resultado]
    y_aprox = [y for x, y, z in resultado]
    z_aprox = [z for x, y, z in resultado]
    y_exato = [solucao_exata_y.subs(symbols('x'), x).evalf() for x in x_vals]
    z_exato = [solucao_exata_z.subs(symbols('x'), x).evalf() for x in x_vals]

    # Plotando os resultados
    plt.figure(figsize=(12, 6))

    # Grafico para y
    plt.subplot(1, 2, 1)
    plt.plot(x_vals, y_aprox, marker='o', linestyle='-', color='b', label='Estimativa y pelo método dos SED')
    plt.plot(x_vals, y_exato, linestyle='--', color='r', label='Solução Exata para y')
    plt.title('Comparação entre Método dos SED e Solução Exata (y)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)

    # Grafico para z
    plt.subplot(1, 2, 2)
    plt.plot(x_vals, z_aprox, marker='o', linestyle='-', color='b', label='Estimativa z pelo método dos SED')
    plt.plot(x_vals, z_exato, linestyle='--', color='r', label='Solução Exata para z')
    plt.title('Comparação entre Método dos SED e Solução Exata (z)')
    plt.xlabel('x')
    plt.ylabel('z')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

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
            y1 = float(lines[i + 4].strip())
            h = float(lines[i + 5].strip())
            n = int(lines[i + 6].strip())

            entradas.append((func1, func2, x0, y0, y1, h, n))
            i += 7

    # Calcula o metodo para cada entrada e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for func1, func2, x0, y0, y1, h, n in entradas:
            # Converte as funcoes simbolicas em funcoes numericas
            f1 = lambdify((symbols('x'), symbols('y'), symbols('z')), func1, 'math')
            f2 = lambdify((symbols('x'), symbols('y'), symbols('z')), func2, 'math')
            
            resultado = hungeKuttaSistemasDiferenciais(f1, f2, x0, y0, y1, h, n)
            solucao_exata_y, solucao_exata_z = solucao(func1, func2, x0, y0, y1)
            
            arq.write(f'Estimativa pelo metodo de Sistemas de Equacoes Diferenciais:\n')
            for x, y, z in resultado:
                yExato = solucao_exata_y.subs(symbols('x'), x).evalf()
                zExato = solucao_exata_z.subs(symbols('x'), x).evalf()
                
                erro_y = round(((y - yExato) / yExato) * 100, 2)
                erro_z = round(((z - zExato) / zExato) * 100, 2)
                
                arq.write(f'x: {x}, y1: {y}, y2: {z}\n')
                arq.write(f'y1_exato: {yExato}, y2_exato: {zExato}\n')
                arq.write(f'Erro y1: {erro_y}%, Erro y2: {erro_z}%\n')
            arq.write('\n')

            # Plotar os graficos
            grafico(resultado, solucao_exata_y, solucao_exata_z)

if __name__ == "__main__":
    main()