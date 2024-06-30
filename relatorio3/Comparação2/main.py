import os
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Function, Eq, dsolve, lambdify, sympify

# Função que plota o gráfico da função exata e das estimativas pelos métodos
def grafico_comparativo(func, x0, y0, h, n, yb, diff_finite_result, shooting_result):
    f = lambdify((symbols('x'), symbols('y')), func, 'numpy')
    
    solucao_exata = solucao(func, x0, y0, symbols('x'))
    
    x_vals_diff = [x for x, y in diff_finite_result]
    y_aprox_diff = [y for x, y in diff_finite_result]
    
    x_vals_shooting = [x for x, y in shooting_result]
    y_aprox_shooting = [y for x, y in shooting_result]
    
    y_exato = [solucao_exata.subs(symbols('x'), x) for x in x_vals_diff]
    
    plt.figure(figsize=(12, 7))
    
    # Plotando solução exata
    plt.plot(x_vals_diff, y_exato, 'k--', label='Solução Exata')
    
    # Plotando estimativa pelo método das diferenças finitas
    plt.plot(x_vals_diff, y_aprox_diff, marker='o', linestyle='-', color='b', label='Diferenças Finitas')
    
    # Plotando estimativa pelo método de shooting
    plt.plot(x_vals_shooting, y_aprox_shooting, marker='s', linestyle='-', color='g', label='Shooting')

    plt.title('Comparação entre Métodos: Diferenças Finitas vs Shooting vs Solução Exata')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Função para calcular o método das diferenças finitas
def diferencasFinitas(f, x0, y0, h, n, yb):
    def boundary_condition(z):
        y = [0] * (n + 1)
        y[0] = y0
        for i in range(1, n + 1):
            y[i] = y[i - 1] + h * f(x0 + (i - 1) * h, y[i - 1])
        return y[-1] - yb
    
    z0 = fsolve(boundary_condition, [y0])
    y = [0] * (n + 1)
    y[0] = y0
    for i in range(1, n + 1):
        y[i] = y[i - 1] + h * f(x0 + (i - 1) * h, y[i - 1])
    
    results = [(x0 + i * h, y[i]) for i in range(n + 1)]
    return results

# Função do método de Shooting
def shooting(f, x0, y0, h, n, yb):
    def residual(z):
        results = hungeKutta(f, x0, y0, h, n)
        xb, yb_approx = results[-1]
        return yb_approx - yb
    
    z0 = fsolve(residual, [y0])
    return hungeKutta(f, x0, z0[0], h, n)

# Função para calcular o método de Runge-Kutta de 4ª ordem
def hungeKutta(f, x0, y0, h, n):
    x = x0
    y = y0
    results = [(x, y)]

    for i in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h / 2, y + k1 / 2)
        k3 = h * f(x + h / 2, y + k2 / 2)
        k4 = h * f(x + h, y + k3)
        y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x += h
        results.append((x, y))
    
    return results

# Função para calcular a solução exata da EDO utilizando funções do sympy
def solucao(func, x0, y0, x):
    y = Function('y')
    edo = Eq(y(x).diff(x), func.subs(symbols('y'), y(x)))
    sol = dsolve(edo, y(x), ics={y(x0): y0})
    return sol.rhs

def main():
    diretorio = os.path.dirname(os.path.realpath(__file__))
    inputs = os.path.join(diretorio, "in.txt")
    outputs = os.path.join(diretorio, "out.txt")

    entradas = []

    with open(inputs, "r") as arq:
        lines = arq.readlines()
        i = 0
        while i < len(lines):
            func = sympify(lines[i].strip())
            x0 = float(lines[i + 1].strip())
            y0 = float(lines[i + 2].strip())
            h = float(lines[i + 3].strip())
            n = int(lines[i + 4].strip())
            yb = float(lines[i + 5].strip())

            entradas.append((func, x0, y0, h, n, yb))
            i += 6

    with open(outputs, "w") as arq:
        for func, x0, y0, h, n, yb in entradas:
            f = lambdify((symbols('x'), symbols('y')), func, 'numpy')
            
            # Calculando resultados
            resultado_diff = diferencasFinitas(f, x0, y0, h, n, yb)
            resultado_shooting = shooting(f, x0, y0, h, n, yb)
            solucao_exata = solucao(func, x0, y0, symbols('x'))
            
            # Escrevendo resultados no arquivo
            arq.write(f'Comparação entre Diferenças Finitas e Shooting:\n')
            for (x_diff, y_diff), (x_shooting, y_shooting) in zip(resultado_diff, resultado_shooting):
                y_exato = solucao_exata.subs(symbols('x'), x_diff)
                erro_diff = round(float(((y_diff - y_exato) / y_exato) * 100), 2) if y_exato != 0 else 0
                erro_shooting = round(float(((y_shooting - y_exato) / y_exato) * 100), 2) if y_exato != 0 else 0
                
                arq.write(f'x_diff: {x_diff}, y_diff: {y_diff}, Erro Diff: {erro_diff}%\n')
                arq.write(f'x_shooting: {x_shooting}, y_shooting: {y_shooting}, Erro Shooting: {erro_shooting}%\n')
            arq.write('\n')

            # Plotando gráfico comparativo
            grafico_comparativo(func, x0, y0, h, n, yb, resultado_diff, resultado_shooting)

if __name__ == "__main__":
    main()