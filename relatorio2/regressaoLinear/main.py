import os

def regressaoLinear(pontosX, pontosY):
    n = len(pontosX)

    # Faz o somatório dos valores de X e Y, respectivamente
    x = sum(pontosX)
    y = sum(pontosY)

    # Inicializa as variáveis e faz o somatório dos valores de X*Y e X^2, respectivamente
    xy = 0
    x2 = 0
    for i in range (n):
        xy += pontosX[i] * pontosY[i]
        x2 += pontosX[i] * pontosX[i]

    # Faz o calculo dos valores que serão utilizados na fórmula: f(x) = b * x + a
    a = (n * xy - x*y) / (n * x2 - x ** 2)
    b = (y - a * x) / n
    
    # Aproxima para 4 casas decimais
    a = round(a, 4)
    b = round(b, 4)

    if b > 0:
        return f"f(x) = {a} * x + {b}"
    else:
        b *= -1
        return f"f(x) = {a} * x - {b}"

def main():
    # Obtém o diretório atual do arquivo, e cria os caminhos para os arquivos de entrada e saída
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    pontosX = []
    pontosY = []

    # Lê os valores do arquivo de entrada
    with open(inputs, "r") as arq:
        for linha in arq:
            aux = linha.strip().split(";")
            x_aux = aux[0].split(",")
            y_aux = aux[1].split(",")

            pontosX.append(list(map(float, x_aux)))
            pontosY.append(list(map(float, y_aux)))
    
    # Realiza o cálculo da função e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            resultado = regressaoLinear(pontosX[i], pontosY[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()