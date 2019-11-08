from thermodynamics.Mollier.mollier_calculator_interface import MoillerCalculatorInterface


class MollierSolidStateCalculator(MoillerCalculatorInterface):

    def calculate_ot(self):
        return 22.42 * ((self.fuel["C"] / 12) + (self.fuel["H"] / 4) + (self.fuel["S"] / 32) - (self.fuel["O"] / 32))

    def calculate_oco2ho(self):
        return 22.42 * ((self.fuel["C"] / 24) + (self.fuel["H"] / 4) - (self.fuel["O"] / 32))

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
        return self.vn2 + self.vo2 + self.vco + self.fuel.proportion_of_formula("CO2")