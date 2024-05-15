import os
from sympy import *
import numpy as np
import matplotlib.pyplot as plt

# Funcao que plota o grafico com o f(x) e os pontos
def grafico(pontosX, pontosY, func):
    x_vals = np.linspace(min(pontosX), max(pontosX), 100)
    y_vals = [func.subs(Symbol("x"), x_val) for x_val in x_vals]

    plt.plot(x_vals, y_vals, label = func)
    plt.scatter(pontosX, pontosY, color = 'red', label = 'Pontos de dados')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Caso contínuo')
    plt.grid(True)

    # Configurando os limites do eixo Y
    plt.ylim(min(pontosY), max(pontosY))

    plt.show()

# Funcao que calcula o caso continuo
def continuo(pontosX, pontosY, grau):
    x = Symbol("x")
    n = len(pontosX)
    A = np.zeros((grau + 1, grau + 1))

    # Construindo a matriz A
    for i in range(grau + 1):
        for j in range(grau + 1):
            A[i][j] = sum(pontosX[k] ** (i + j) for k in range(n))

    # Construindo o vetor b
    b = np.array([sum(pontosY[k] * pontosX[k] ** i for k in range(n)) for i in range(grau + 1)])

    # Resolvendo o sistema de equacoes lineares
    coeficientes = np.linalg.solve(A, b)

    polinomio = sum(coeficientes[i] * x ** i for i in range(grau + 1))

    return f"f(x) = {polinomio}"

def main():
    # Obtem o diretorio atual do arquivo, e cria os caminhos para os arquivos de entrada e saida
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    pontosX = []
    pontosY = []
    grau = []
    polinomios = []

    # Le os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Le os pontos X e Y da entrada
            x_aux = list(map(float, lines[i].strip().split()))
            y_aux = list(map(float, lines[i + 1].strip().split()))
            grau_aux = int(lines[i + 2].strip())

            pontosX.append(x_aux)
            pontosY.append(y_aux)
            grau.append(grau_aux)
            i += 3
    
    # Realiza o calculo da funcao e escreve os resultados no arquivo de saida
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            resultado = continuo(pontosX[i], pontosY[i], grau[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")
            polinomios.append(resultado)

    # Plotar os graficos
    for i in range(len(pontosX)):
        Pn = sympify(polinomios[i].split('=')[1].strip())
        grafico(pontosX[i], pontosY[i], Pn)

if __name__ == "__main__":
    main()