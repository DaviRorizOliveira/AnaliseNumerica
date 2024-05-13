import os
from sympy import *

def derivadaCentrada(pontosX, pontosY, index):
    return (pontosY[index + 1] - 2 * pontosY[index] + pontosY[index - 1]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaProgressiva(pontosX, pontosY, index):
    return (pontosY[index] - 2 * pontosY[index - 1] + pontosY[index - 2]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaRetardada(pontosX, pontosY, index):
    return (pontosY[index + 2] - 2 * pontosY[index + 1] + pontosY[index]) / ((pontosX[index + 1] - pontosX[index]) ** 2)

def main():
    # Obtém o diretório atual do arquivo e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    pontosX = []
    pontosY = []

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Lê os pontos X e Y da entrada
            x_aux = list(map(float, lines[i].strip().split()))
            y_aux = list(map(float, lines[i + 1].strip().split()))
            index = int(lines[i + 2].strip())

            pontosX.append(x_aux)
            pontosY.append(y_aux)
            i += 3

    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            centrada = derivadaCentrada(pontosX[i], pontosY[i], index)
            progressiva = derivadaProgressiva(pontosX[i], pontosY[i], index)
            retardada = derivadaRetardada(pontosX[i], pontosY[i], index)
            
            arq.write(f'Derivada centrada: {centrada}\n')
            arq.write(f'Derivada progressiva: {progressiva}\n')
            arq.write(f'Derivada retardada: {retardada}\n')
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()