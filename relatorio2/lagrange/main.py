import os
from sympy import *

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

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        for linha in arq:
            aux = linha.strip().split(";")
            x_aux = aux[0].split(",")
            y_aux = aux[1].split(",")

            pontosX.append(list(map(float, x_aux)))
            pontosY.append(list(map(float, y_aux)))
    
    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            resultado = lagrange(pontosX[i], pontosY[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()