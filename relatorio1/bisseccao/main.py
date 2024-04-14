import os
import math

def bissect(f, a, b, tol):
    # Verifica quantas iteracoes vai ter e aproxima para o proximo inteiro
    iteracoes = math.log((b - a) / tol)
    iteracoes = round(iteracoes) + 1
    
    # Condicao de Bolzano
    if f(a) * f(b) > 0:
        raise ValueError("A funcao deve ter sinais opostos em f(a) e f(b).")
    
    contador = 0

    while contador < iteracoes:
        medio = (a + b) / 2
        if f(a) * f(medio) < 0:
            b = medio
        else:
            a = medio
        contador += 1

    return (a + b) / 2

def main():
    # Obtem o diretorio atual do arquivo, e cria os caminhos para os arquivos de entrada e saida
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, 'in.txt')
    outputs = os.path.join(diretorio, 'out.txt')

    # Le as entradas do arquivo de entrada
    with open(inputs, 'r') as file:
        lines = file.readlines()

    # Calcula e escreve os resultados para cada grupo de funcao e intervalo
    with open(outputs, 'w') as file:
        for i in range(0, len(lines), 4):
            a, b, tolerancia = map(float, lines[i+1:i+4])
            func_str = lines[i].strip()
            func = eval("lambda x: " + func_str)
            raiz = bissect(func, a, b, tolerancia)
            file.write("{}\n".format(raiz))

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()