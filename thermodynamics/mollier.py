class Mollier:
    def __init__(self, fuel):
        self.fuel = fuel
        self.Ot = self.calculate_ot()
        self.vc = self.calculate_vc()
        self.vn = self.calculate_vn()
        self.vs = self.calculate_vs()
        self.sigma = self.calculate_sigma()
        self.nu = self.calculate_nu()
        self.Ocoh2o = self.calculate_vocov2ho()
        self.vo = self.calculate_vo() # 7.121
        self.vco = self.calculate_vco()
        self.vn2 = self.calculate_vn2()
        self.vo2 = self.calculate_vo2()
        self.v0s = self.calculate_v0s()

    # tlen teoretyczny
    def calculate_ot(self):
        if self.fuel.is_gas:
            return self.fuel.proportion_of_formula("CO")*0.5 + self.fuel.proportion_of_formula("H2")*0.5 + self.fuel.proportion_of_formula("H2S")*1.5 + self.fuel.proportion_of_formula("CH4")*2 + self.fuel.proportion_of_formula("C2H6")*3 + self.fuel.proportion_of_formula("C3H6")*4
        else:
            return 22.42 * ((self.fuel["C"]/12) + (self.fuel["H"]/4) + (self.fuel["S"]/32) - (self.fuel["O"]/32))

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

    def calculate_vocov2ho(self):
        return 22.42 * ((self.fuel["C"]/24) + (self.fuel["H"]/4) - (self.fuel["O"]/32))

    def calculate_v0s(self):
        return self.vco + self.vn2 + self.vo2

    def calculate_vco(self):
        return 22.42 * (self.fuel["C"] / 12)

    def calculate_vn2(self):
        return 22.42 * (self.fuel["N"] / 28) + (0.79 * self.vo)

    # ilość tlenu potrzebna do spalenia zupełnego
    def calculate_vo(self):
        return 4.76 * self.Ot

    def calculate_vo2(self):
        return self.Ot - self.Ocoh2o
