import os
from sympy import *
import math

def derivadaCentrada(pontosX, pontosY, index):
    return (pontosY[index + 1] - 2 * pontosY[index] + pontosY[index - 1]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaProgressiva(pontosX, pontosY, index):
    return (pontosY[index] - 2 * pontosY[index - 1] + pontosY[index - 2]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaRetardada(pontosX, pontosY, index):
    return (pontosY[index + 2] - 2 * pontosY[index + 1] + pontosY[index]) / ((pontosX[index + 1] - pontosX[index]) ** 2)

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
            centrada = derivadaCentrada(pontosX[i], pontosY[i], 1)
            progressiva = derivadaProgressiva(pontosX[i], pontosY[i], 1)
            retardada = derivadaRetardada(pontosX[i], pontosY[i], 1)
            
            arq.write(f'Derivada centrada: {centrada}\n')
            arq.write(f'Derivada progressiva: {progressiva}\n')
            arq.write(f'Derivada retardada: {retardada}\n')
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()