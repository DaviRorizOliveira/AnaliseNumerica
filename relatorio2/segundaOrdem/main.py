import os
from sympy import *

def derivadaCentrada(pontosX, pontosY, index):
    return (pontosY[index + 1] - 2 * pontosY[index] + pontosY[index - 1]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaProgressiva(pontosX, pontosY, index):
    return (pontosY[index] - 2 * pontosY[index - 1] + pontosY[index - 2]) / ((pontosX[index] - pontosX[index - 1]) ** 2)

def derivadaRetardada(pontosX, pontosY, index):
    return (pontosY[index + 2] - 2 * pontosY[index + 1] + pontosY[index]) / ((pontosX[index + 1] - pontosX[index]) ** 2)

def interpolador(pontosX, pontosY):
    n = len(pontosX)
    
    # Matriz que faz o armazenamento das diferenças divididas
    dif = [pontosY.copy()]

    # Calcula as diferenças divididas
    for i in range(1, n):
        dif.append([])
        for j in range(n - i):
            dif[i].append((dif[i - 1][j] - dif[i - 1][j + 1]) / (pontosX[j] - pontosX[i + j]))

    return dif

# Calculo da interpolacao de newton, retornando a derivada segunda real da funcao para testes
def newton(pontosX, pontosY, index):
    # Define o símbolo da variável X para montar a fórmula de f(x)
    x = Symbol("x")

    n = len(pontosX)
    
    fx = 0
    dif = interpolador(pontosX, pontosY)

    for i in range(n):
        termo = dif[i][0]
        for j in range(i):
            termo *= (x - pontosX[j])

        fx += termo

    # Função que faz a expansão que realiza as multiplicações
    fx = expand(fx)

    fx = fx.diff(x)
    fx = fx.diff(x)
    fx = fx.subs(x, index)

    return fx

def main():
    # Obtém o diretório atual do arquivo e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    pontosX = []
    pontosY = []
    index = []

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Lê os pontos X e Y da entrada
            x_aux = list(map(float, lines[i].strip().split()))
            y_aux = list(map(float, lines[i + 1].strip().split()))
            index_aux = int(lines[i + 2].strip())

            pontosX.append(x_aux)
            pontosY.append(y_aux)
            index.append(index_aux)
            i += 3

    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            centrada = derivadaCentrada(pontosX[i], pontosY[i], index[i])
            progressiva = derivadaProgressiva(pontosX[i], pontosY[i], index[i])
            retardada = derivadaRetardada(pontosX[i], pontosY[i], index[i])
            
            arq.write(f'Derivada centrada: {centrada}\n')
            arq.write(f'Derivada progressiva: {progressiva}\n')
            arq.write(f'Derivada retardada: {retardada}\n')

            resultado = newton(pontosX[i], pontosY[i], index[i])
            arq.write(f'Derivada real: {resultado}\n')

            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()