# INCOMPLETO !!!!!!!!!!!!!

import os
from sympy import *
import numpy as np

def casoDiscreto(valores_x, f):
    x = Symbol("x")
    funcao = [1, eval("x"), eval("x**2")]
    tamFuncao = len(funcao)
    tam_X = len(valores_x)
    matrizUi = [tam_X*[1]]
    
    listaAux = []
    for i in range(tamFuncao):
        aux = funcao[i]
        if(aux != 1):
            for elem in valores_x:
                listaAux.append(aux.subs(x, elem))
                
            matrizUi.append(listaAux)
            listaAux = []

    vetorF = zeros(tamFuncao, 1)
    matrizRes = zeros(tamFuncao)
    for i in range(tamFuncao):
        for j in range(tamFuncao):
            matrizRes[i,j] = sum(np.multiply(matrizUi[i], matrizUi[j]))
        vetorF[i] = sum(np.multiply(f, matrizUi[i]))
    resultado = matrizRes.LUsolve(vetorF)

    potencializacao = 1
    resultado_final = 0
    for i in range(tamFuncao):
        resultado_final += round(resultado[i,0], 2) * potencializacao
        potencializacao *= x

    return resultado_final

def main():
    # Obtém o diretório atual do arquivo, e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    valor_x = []
    valor_y = []

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        for linha in arq:
            aux = linha.strip().split(";")
            x_aux = aux[0].split(",")
            y_aux = aux[1].split(",")

            valor_x.append(list(map(float, x_aux)))
            valor_y.append(list(map(float, y_aux)))
    
    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(valor_x)):
            resultado = casoDiscreto(valor_x[i], valor_y[i])
            arq.write(str(resultado))
            if i < len(valor_x) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()

def calcular_vetores_potenciais(vetor_y):
    N = len(vetor_y)
    vetores_potenciais = []
    
    for potencia in range(N - 1):
        novo_vetor = [valor ** potencia for valor in vetor_y]
        vetores_potenciais.append(novo_vetor)
    
    return vetores_potenciais

# Exemplo de uso:
vetor_y = [1, 2, 3, 4]
resultado = calcular_vetores_potenciais(vetor_y)
for i, vetor in enumerate(resultado):
    print(f'Vetor {i}: {vetor}')