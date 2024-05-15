import os
import math

def secante(f, x0, x1, tol):

    iteracoes = 0

    while True:
        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))
        if abs(x2 - x1) < tol:
            return x2
        x0, x1 = x1, x2
        iteracoes += 1
        if iteracoes > 1000:
            raise ValueError("O metodo da secante nao convergiu apos 1000 iteracoes.")

def main():
    # Obtém o diretório atual do arquivo, e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, 'in.txt')
    outputs = os.path.join(diretorio, 'out.txt')

    # Lê as entradas do arquivo de entrada
    with open(inputs, 'r') as file:
        lines = file.readlines()

    # Calcula e escreve os resultados para cada grupo de funcao e intervalo
    with open(outputs, 'w') as file:
        for i in range(0, len(lines), 4):
            x0, x1, tolerancia = map(float, lines[i+1:i+4])
            func_str = lines[i].strip()
            func = eval("lambda x: " + func_str)
            raiz = secante(func, x0, x1, tolerancia)
            file.write("{}\n".format(raiz))

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()