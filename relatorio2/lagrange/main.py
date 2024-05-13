import os
from sympy import *
import numpy as np
import matplotlib.pyplot as plt

# Função que plota o grafico com o f(x) e os pontos
def grafico(pontosX, pontosY, func):
    x_vals = np.linspace(min(pontosX), max(pontosX), 100)
    y_vals = [func.subs(Symbol("x"), x_val) for x_val in x_vals]

    plt.plot(x_vals, y_vals, label = func)
    plt.scatter(pontosX, pontosY, color = 'red', label = 'Pontos de dados')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Interpolação de Lagrange')
    plt.grid(True)

    # Configurando os limites do eixo Y
    plt.ylim(min(pontosY), max(pontosY))

    plt.show()

def lagrange(pontosX, pontosY):
	n = len(pontosX)

    # Polinômio interpolador Pn(x)
	Pn = 0

    # Faz o somatório de: lk(x) * fk
	for i in range(n):
		Pn += interpolador(i, pontosX, n) * pontosY[i]

	Pn = Pn.args[0]
	return f"f(x) = {Pn}"

def interpolador(k, pontosX, n):
    # Define o símbolo da variável X para montar a fórmula de f(x)
	x = Symbol("x")

    # Faz o calculo de lk(x)
	lk = 1
	for i in range(n):
		if (i != k):
			lk *= Poly((x - pontosX[i]) / (pontosX[k] - pontosX[i]))
	return lk

def main():
    # Obtém o diretório atual do arquivo, e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    pontosX = []
    pontosY = []
    polinomios = []

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Lê os pontos X e Y da entrada
            x_aux = list(map(float, lines[i].strip().split()))
            y_aux = list(map(float, lines[i + 1].strip().split()))

            pontosX.append(x_aux)
            pontosY.append(y_aux)
            i += 2
    
    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            resultado = lagrange(pontosX[i], pontosY[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")
            polinomios.append(resultado)

    # Plotar gráficos
    for i in range(len(pontosX)):
        Pn = sympify(polinomios[i].split('=')[1].strip())
        grafico(pontosX[i], pontosY[i], Pn)

if __name__ == "__main__":
    main()