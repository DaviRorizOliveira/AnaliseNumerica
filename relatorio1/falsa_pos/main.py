import os
import math

def falsa_pos(f, a, b, tol):
    # Verifica quantas iteracoes vai ter e aproxima para o proximo inteiro
    iteracoes = math.log((b - a) / tol)
    iteracoes = round(iteracoes) + 1
    
    # Condicao de Bolzano
    if f(a) * f(b) > 0:
        raise ValueError("A funcao deve ter sinais opostos em f(a) e f(b).")
    
    contador = 0

    while contador < iteracoes:
        fa = f(a)
        fb = f(b)
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        if fa * fc < 0:
            b = c
        else:
            a = c
        contador += 1

    return (a + b) / 2

def main():
    # Obtém o diretório atual do arquivo, e cria os caminhos para os arquivos de entrada e saída
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input_file_path = os.path.join(dir_path, 'in.txt')
    output_file_path = os.path.join(dir_path, 'out.txt')

    # Lê as entradas do arquivo de entrada
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Calcula e escreve os resultados para cada grupo de função e intervalo
    with open(output_file_path, 'w') as file:
        for i in range(0, len(lines), 4):
            a, b, tolerancia = map(float, lines[i+1:i+4])
            func_str = lines[i].strip()
            func = eval("lambda x: " + func_str)
            raiz = falsa_pos(func, a, b, tolerancia)
            file.write("{}\n".format(raiz))

    print("Resultados gravados no arquivo out.txt")

if __name__ == "__main__":
    main()