import os
from sympy import *

# Função para calcular a quadratura gaussiana
def gauss(func, intervalo):
    pontos = [-sqrt(3) / 3, sqrt(3) / 3]
    pesos = [1, 1]

    a, b = intervalo
    a0 = (b - a) / 2
    a1 = (b + a) / 2

    soma = 0
    for i in range(len(pontos)):
        point = pontos[i]
        soma += pesos[i] * func.subs(x, a0 * point + a1)

    return a0 * soma

def main():
    # Obtém o diretório atual do arquivo e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    # Lista para armazenar as funções e intervalos
    entradas = []

    # Lê as entradas do arquivo de entrada
    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            # Lê a função
            func = sympify(lines[i].strip())
            
            # Lê os limites do intervalo
            a = float(lines[i + 1].strip())
            b = float(lines[i + 2].strip())

            entradas.append((func, (a, b)))
            i += 3

    # Calcula a integral para cada entrada e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for func, intervalo in entradas:
            # Função pronta para calcular a integral a fim de mostrar as diferenças
            integral = integrate(func, (x, intervalo[0], intervalo[1]))
            arq.write(f'Integral correta: {integral}\n')

            # Calcula o resultado final
            resultado = gauss(func, intervalo).evalf()
            arq.write(f'Estimativa da quadratura gaussiana: {resultado}\n')
            
            # Porcentagem de erro em relação a integral correta
            erro = round(((integral - resultado) / integral) * 100, 2)
            arq.write(f'Erro: {erro}%\n')

if __name__ == "__main__":
    x = Symbol("x")
    main()