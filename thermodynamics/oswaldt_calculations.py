class Fuel:

    def __init__(self, formula=None, c=None,o=None,n=None,h = None):
        if formula:
            self.formula = formula
            self.c = formula.percentage_mass("C")
            self.o = formula.percentage_mass("O")
            self.h = formula.percentage_mass("H")
            self.n = formula.percentage_mass("N")
        else:
            self.c = c
            self.o = o
            self.n = n
            self.h = h


class Mollier:
    def __init__(self, fuel):
        self.fuel = fuel
        self.ot = self.calculate_ot()
        self.vc = self.calculate_vc()
        self.vn = self.calculate_vn()
        self.sigma = self.calculate_sigma()
        self.nu = self.calculate_nu()

    def calculate_ot(self):
        return 22.42 * ((self.fuel.c/12) + (self.fuel.o/32) + (self.fuel.h/4))

    def calculate_vc(self):
        return 22.42 * (self.fuel.c/12)

    def calculate_vn(self):
        return 22.42 * (self.fuel.n/28)

    def calculate_sigma(self):
        return self.ot / self.vc

    def calculate_nu(self):
        return self.vn / self.vc


class OslwaldtCalculations:
    max_o2 = 21
    max_co2 = None
    max_co = None

    def __init__(self, fuel, co2, o2):
        self.co2 = co2
        self.o2 = o2
        self.fuel = fuel
        self.mollier = None
        self.set_moiller()
        self.kmax = self.calculate_kmax()

    def set_moiller(self):
        self.mollier = Mollier(self.fuel)

    def calculate_kmax(self):
        return 100/(((79/21) * self.mollier.sigma) + self.mollier.nu + 1) #percent
