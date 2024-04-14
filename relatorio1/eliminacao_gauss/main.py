import os

def substituicoes_somatoria(A, B):
    n = len(A)
    x = n * [0]
    for i in range(n - 1, -1, -1):
        S = 0
        for j in range(i + 1, n):
            S = S + A[i][j] * x[j]
        x[i] = (B[i] - S) / A[i][i]
    return x

def gauss(A, B):
    n = len(A)
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            F = -A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] = F * A[k][j] + A[i][j]
            B[i] = F * B[k] + B[i]
            A[i][k] = 0
    det = 1
    for i in range(n):
        det = det * A[i][i]
    if det != 0:
        x = substituicoes_somatoria(A, B)
        return (x, det)
    else:
        print('A matriz dos coeficientes eh singular, ou seja, o determinante eh igual a zero!')
        return ([], det)

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
            A = [data[i], data[i + 1], data[i + 2]]
            B = data[i + 3]

            result = gauss(A, B)

            for j in range(len(result[0])):
                file.write(f"x[{j}] = {result[0][j]}\n")
            file.write("\n")

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()