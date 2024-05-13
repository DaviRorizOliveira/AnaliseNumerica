import os
from sympy import *

# Função que calcula os valores da função nos pontos 'a' e 'b'
def fx(func, valorX):
    aux = func.split('x')
    valorY = ('(' + str(valorX) + ')').join(aux)
    return eval(str(valorY))

# Função com a fórmula do trapézio
def trapezio(func, intervalo):
    h = intervalo[1] - intervalo[0]
    return (h / 2) * (func.subs(x, intervalo[0]) + func.subs(x, intervalo[1]))

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
            resultado = trapezio(func, intervalo)
            erro = round(((integral - resultado) / integral) * 100, 2)
            
            arq.write(f'Integral correta: {integral}\n')
            arq.write(f'Estimativa do trapezio simples: {resultado}\n')
            arq.write(f'Erro: {erro}%\n')

if __name__ == "__main__":
    x = symbols('x')
    main()