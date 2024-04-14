import os
import numpy as np

def numero_condicao_matriz(A):
    # Calcular o número de condição da matriz A
    condicao = np.linalg.cond(A)
    return condicao

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(dir_path, 'in.txt')
    outputs = os.path.join(dir_path, 'out.txt')

    with open(inputs, 'r') as file:
        lines = file.readlines()
        data = [list(map(float, line.strip().split())) for line in lines]

    with open(outputs, 'w') as file:
        for i in range(0, len(data), 3):  # Removido o loop do vetor B
            A = np.array([data[i], data[i + 1], data[i + 2]])

            # Aqui você pode calcular o número de condição da matriz A
            condicao = numero_condicao_matriz(A)
            file.write(f"{condicao}")
            file.write("\n")

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()