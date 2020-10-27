import sys
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl


#função para plotagem de gráfico
def imprime_grafico(xvals, ymax, labels, colors):
    plt.figure(figsize=(8, 5))

    # Plota a gráfico e adiciona os valores
    plt.plot(x, mfx, 'k')
    for xv, y, label, color in zip(xvals, ymax, labels, colors):
        plt.vlines(xv, 0, y, label=label, color=color)
    plt.ylabel('Funcao de pertinencia Fuzzy')
    plt.xlabel('Universo das variaveis')
    plt.ylim(-0.1, 1.1)
    plt.legend(loc=2)

    # Exibe o gráfico
    plt.show()


# Gera função de pertinência trapezoidal, no intervalo [0, 1]
x = np.arange(0, 5.05, 0.1) #gera valores de 0 até 5.05, com intervalo de 0.
mfx = fuzz.trapmf(x, [2, 2.5, 3, 4.5])

# Defuzzificação das funções de pertinência
defuzz_centroid = fuzz.defuzz(x, mfx, 'centroid')
defuzz_mom = fuzz.defuzz(x, mfx, 'mom')

# Coleção de valores para as linhas verticais do gráfico
labels = ['centroide', 'media dos maximos'] #métodos de defuzificação
xvals = [defuzz_centroid, defuzz_mom] #valores do eixo x
colors = ['r', 'g'] #cores das linhas 
ymax = [fuzz.interp_membership(x, mfx, i) for i in xvals]

# Exibe a gráfico, com as funções de defuzificação
imprime_grafico(xvals, ymax, labels, colors)
