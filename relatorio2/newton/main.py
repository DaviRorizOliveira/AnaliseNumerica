import os
from sympy import *

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

def newton(pontosX, pontosY):
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

    return f"f(x) = {fx}"

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
            resultado = newton(pontosX[i], pontosY[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()