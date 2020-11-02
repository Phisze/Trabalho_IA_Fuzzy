import numpy
from matplotlib import pyplot
import skfuzzy
from skfuzzy import control


def sistema(input_altitude_real: int, input_altitude_relativa: int, metodo_defuzz: str, graficos: bool) -> float:
    """
    O sistema inteiro foi contido em uma função para facilitar sua reutilização,
    necessitando apenas dos dados de entrada essenciais
    """

    # Variáveis de entrada abstraídas a partir das caracterísitcas e necessidades
    # da aeronave
    altitude_real = control.Antecedent(numpy.arange(0, 1000, 1), "altitude_real")
    altitude_relativa = control.Antecedent(numpy.arange(0, 1000, 1), "altitude_relativa")
    
    # Variável de saída para controle dos equipamentos da aeronave
    velocidade = control.Consequent(numpy.arange(0, 100, 1), "velocidade", defuzzify_method=metodo_defuzz)
    
    # Não utilizada devido à ausência de asa em quadrimotores
    # angulo_asa = control.Antecedent(numpy.arange(0, 90, 0.1), "angulo_asa")

    # Interpretação da variável de altitude real da aeronave
    # Essa variavel representa a altitude do veículo em relação ao nível do mar
    altitude_real["baixa"] = skfuzzy.trimf(altitude_real.universe, [0, 0, 250])
    altitude_real["media"] = skfuzzy.trapmf(altitude_real.universe, [200, 250, 500, 550])
    altitude_real["alta"] = skfuzzy.trimf(altitude_real.universe, [500, 600, 700])
    altitude_real["muito_alta"] = skfuzzy.trimf(altitude_real.universe, [650, 1000, 1000])

    # Interpretação da variável de altitude relativa da aeronave
    # Essa variavel representa a altitude do veículo em relção ao solo diretamente abaixo
    altitude_relativa["baixa"] = skfuzzy.trimf(altitude_real.universe, [0, 0, 200])
    altitude_relativa["media"] = skfuzzy.trapmf(altitude_real.universe, [150, 300, 500, 550])
    altitude_relativa["alta"] = skfuzzy.trimf(altitude_real.universe, [500, 1000, 1000])

    # Interpretação da variável de velocidade dos motores da aeronave
    velocidade["baixa"] = skfuzzy.trimf(velocidade.universe, [0, 0, 50])
    velocidade["media"] = skfuzzy.trimf(velocidade.universe, [25, 50, 75])
    velocidade["alta"] = skfuzzy.trimf(velocidade.universe, [75, 100, 100])

    # Regras para o controle de velocidade a partir das medições de altitude
    # Conjunto 1 - Tratando das condições de baixa e média altitudes reais 
    regra_1 = control.Rule(altitude_relativa["baixa"] & (altitude_real["baixa"] | altitude_real["media"]), velocidade["alta"])
    regra_2 = control.Rule(altitude_relativa["media"] & (altitude_real["baixa"] | altitude_real["media"]), velocidade["media"])
    regra_3 = control.Rule(altitude_relativa["alta"] & (altitude_real["baixa"] | altitude_real["media"] | altitude_real["alta"]), velocidade["baixa"])
    # Conjunto 2 - Tratando das condições de alta altitude real
    regra_4 = control.Rule(altitude_relativa["baixa"] & altitude_real["alta"], velocidade["media"])
    regra_5 = control.Rule(altitude_relativa["media"] & altitude_real["alta"], velocidade["media"])
    # Conjunto 3 - Tratando das condições de altitude real muito alta
    regra_6 = control.Rule(altitude_relativa["baixa"] & altitude_real["muito_alta"], velocidade["baixa"])
    regra_7 = control.Rule(altitude_relativa["media"] & altitude_real["muito_alta"], velocidade["baixa"])

    # Construindo o sistema de regras
    controle_velocidade = control.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5, regra_6, regra_7])
    simulacao_velocidade = control.ControlSystemSimulation(controle_velocidade)

    # Inserção dos valores de entrada a serem processados
    simulacao_velocidade.input["altitude_real"] = input_altitude_real
    simulacao_velocidade.input["altitude_relativa"] = input_altitude_relativa

    # Realizando computação do modelo construído
    simulacao_velocidade.compute()

    # Exibição dos gráficos de entrada e saída do modelo Fuzzy
    if graficos:
        altitude_real.view()
        altitude_relativa.view()
        velocidade.view()
        velocidade.view(sim=simulacao_velocidade)

    return simulacao_velocidade.output["velocidade"]


# Valores para teste e demonstração do funcionamento do algoritmo
altitude_real = 400
altitude_relativa = 200

velocidade = sistema(altitude_real, altitude_relativa, "centroid", True)
print("Velocidade: %d" % velocidade)
pyplot.show() # Mantendo os gráficos abertos após a execução do algoritmo
