import os

def mmq(pontosX, pontosY):
    n = len(pontosX)

    # Calcula as somas necessárias para o MMQ
    sum_x = sum(pontosX)
    sum_y = sum(pontosY)
    sum_xy = sum(x * y for x, y in zip(pontosX, pontosY))
    sum_x2 = sum(x ** 2 for x in pontosX)

    # Calcula os coeficientes da reta de regressão
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b = (sum_y - a * sum_x) / n
    
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
    
    # Realiza o cálculo da função utilizando MMQ e escreve os resultados no arquivo de saída
    with open(outputs, "w") as arq:
        for i in range(len(pontosX)):
            resultado = mmq(pontosX[i], pontosY[i])
            arq.write(str(resultado))
            if i < len(pontosX) - 1:
                arq.write("\n")

if __name__ == "__main__":
    main()