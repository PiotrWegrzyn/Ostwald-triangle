from thermodynamics.Mollier.mollier_calculator_interface import MoillerCalculatorInterface
from thermodynamics.carbohydrate import Carbohydrate


class MollierGasStateCalculator(MoillerCalculatorInterface):

    def calculate_ot(self):
        ot = self.fuel.proportion_of_formula("CO") * 0.5 + self.fuel.proportion_of_formula(
            "H2") * 0.5 + self.fuel.proportion_of_formula("H2S") * 1.5
        ot -= self.fuel.proportion_of_formula("02")
        for carbohydrate in Carbohydrate.get_all():
            ot += self.fuel.proportion_of_formula(carbohydrate.name) * (carbohydrate.c + (carbohydrate.h / 4))
        return ot

    def calculate_oco2ho(self):
        oco2ho = 0
        for carbohydrate in Carbohydrate.get_all():
            proportion = self.fuel.proportion_of_formula(carbohydrate.name)
            if proportion > 0:
                if carbohydrate.type == "Alkan":
                    stehio = carbohydrate.c + 0.5
                elif carbohydrate.type == "Alken":
                    stehio = carbohydrate.c
                else:
                    stehio = carbohydrate.c - 0.5
                oco2ho += proportion * stehio
        oco2ho -= self.fuel.proportion_of_formula("02")
        return oco2ho

    def calculate_vo2(self):
        return self.Ot - self.Ocoh2o


    def calculate_vc(self):
        return 22.42 * ((self.fuel["C"]/12) + (self.fuel["S"] /32))

    def calculate_vs(self):
        return 22.42 * (self.fuel["S"]/28) + 0.79

    def calculate_vn(self):
        return 22.42 * (self.fuel["N"]/28)

    def calculate_sigma(self):
        return self.Ot / self.vc

    def calculate_nu(self):
        return self.vn / self.vc

    def calculate_vco(self):
        return 22.42 * (self.fuel["C"] / 12)

    def calculate_vn2(self):
        return 22.42 * (self.fuel["N"] / 28) + (0.79 * self.vo)

    # ilość tlenu potrzebna do spalenia zupełnego
    def calculate_vo(self):
        return 4.76 * self.Ot

    def calculate_v0s(self):
        vco = self.vco / 2
        return self.vn2 + self.vo2 + vco + self.fuel.proportion_of_formula("CO2")
