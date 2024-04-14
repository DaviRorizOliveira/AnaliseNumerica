import os
import numpy as np

# Funcao para resolver um sistema linear triangular inferior por substituicao progressiva
def substituicao_progressiva(L, B):
    n = len(L)
    y = n * [0]
    for i in range(n):
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (B[i] - soma) / L[i][i]
    return y

# Funcao para resolver um sistema linear triangular superior por substituicao regressiva
def substituicao_regressiva(U, y):
    n = len(U)
    x = n * [0]
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - soma) / U[i][i]
    return x

def fatoracao_LU(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        L[i][i] = 1
        for j in range(i, n):
            soma1 = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - soma1
        for j in range(i + 1, n):
            soma2 = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - soma2) / U[i][i]
    
    return L, U

def resolve_sistema(A, B):
    L, U = fatoracao_LU(A)
    y = substituicao_progressiva(L, B)
    x = substituicao_regressiva(U, y)
    return x

def main():
    # Obtem o diretorio atual do arquivo e cria os caminhos para os arquivos de entrada e saida
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(dir_path, 'in.txt')
    outputs = os.path.join(dir_path, 'out.txt')

    # Le as entradas do arquivo de entrada
    with open(inputs, 'r') as file:
        lines = file.readlines()
        data = [list(map(float, line.strip().split())) for line in lines]

    # Calcula e escreve os resultados no arquivo de saida
    with open(outputs, 'w') as file:
        for i in range(0, len(data), 4):
            A = np.array([data[i], data[i + 1], data[i + 2]])
            B = np.array(data[i + 3])

            result = resolve_sistema(A, B)

            for j in range(len(result)):
                file.write(f"x[{j}] = {result[j]}\n")
            file.write("\n")

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()