import os
import numpy as np

def jacobi(A, B):
    iteracoes = 1000
    tol = 1e-6
    n = len(A)
    x = np.zeros(n)
    x_ant = np.zeros(n)
    for _ in range(iteracoes):
        for i in range(n):
            soma = sum(A[i][j] * x_ant[j] for j in range(n) if j != i)
            x[i] = (B[i] - soma) / A[i][i]
        if np.allclose(x, x_ant, atol=tol):
            break
        x_ant = np.copy(x)
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

            result = jacobi(A, B)

            for j in range(len(result)):
                file.write(f"x[{j}] = {result[j]}\n")
            file.write("\n")

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()