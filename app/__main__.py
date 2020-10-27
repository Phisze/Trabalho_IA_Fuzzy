import numpy
from matplotlib import pyplot
import skfuzzy
from skfuzzy import control


def sistema(input_altitude_real: int, input_altitude_relativa: int, metodo_defuzz: str) -> None:

    altitude_real = control.Antecedent(numpy.arange(0, 1000, 1), "altitude_real")
    altitude_relativa = control.Antecedent(numpy.arange(0, 1000, 1), "altitude_relativa")
    velocidade = control.Consequent(numpy.arange(0, 100, 1), "velocidade", defuzzify_method=metodo_defuzz)
    # angulo_asa = control.Antecedent(numpy.arange(0, 90, 0.1), "angulo_asa")

    altitude_real["baixa"] = skfuzzy.trimf(altitude_real.universe, [0, 0, 250])
    altitude_real["media"] = skfuzzy.trapmf(altitude_real.universe, [200, 250, 500, 550])
    altitude_real["alta"] = skfuzzy.trimf(altitude_real.universe, [500, 600, 700])
    altitude_real["muito_alta"] = skfuzzy.trimf(altitude_real.universe, [650, 1000, 1000])

    altitude_relativa["baixa"] = skfuzzy.trimf(altitude_real.universe, [0, 0, 200])
    altitude_relativa["media"] = skfuzzy.trapmf(altitude_real.universe, [150, 300, 500, 550])
    altitude_relativa["alta"] = skfuzzy.trimf(altitude_real.universe, [500, 1000, 1000])

    velocidade["baixa"] = skfuzzy.trimf(velocidade.universe, [0, 0, 50])
    velocidade["media"] = skfuzzy.trimf(velocidade.universe, [25, 50, 75])
    velocidade["alta"] = skfuzzy.trimf(velocidade.universe, [75, 100, 100])


    regra_1 = control.Rule(altitude_relativa["baixa"] & (altitude_real["baixa"] | altitude_real["media"]), velocidade["alta"])
    regra_2 = control.Rule(altitude_relativa["media"] & (altitude_real["baixa"] | altitude_real["media"]), velocidade["media"])
    regra_3 = control.Rule(altitude_relativa["alta"] & (altitude_real["baixa"] | altitude_real["media"] | altitude_real["alta"]), velocidade["baixa"])

    regra_4 = control.Rule(altitude_relativa["baixa"] & altitude_real["alta"], velocidade["media"])
    regra_5 = control.Rule(altitude_relativa["media"] & altitude_real["alta"], velocidade["media"])

    regra_6 = control.Rule(altitude_relativa["baixa"] & altitude_real["muito_alta"], velocidade["baixa"])
    regra_7 = control.Rule(altitude_relativa["media"] & altitude_real["muito_alta"], velocidade["baixa"])


    controle_velocidade = control.ControlSystem([regra_1, regra_2, regra_3, regra_4, regra_5, regra_6, regra_7])
    simulacao_velocidade = control.ControlSystemSimulation(controle_velocidade)

    simulacao_velocidade.input["altitude_real"] = input_altitude_real
    simulacao_velocidade.input["altitude_relativa"] = input_altitude_relativa

    simulacao_velocidade.compute()

    print("Velocidade: %d" % simulacao_velocidade.output["velocidade"])

    altitude_real.view()
    altitude_relativa.view()
    velocidade.view()
    velocidade.view(sim=simulacao_velocidade)


sistema(400, 200, "centroid")
pyplot.show()
