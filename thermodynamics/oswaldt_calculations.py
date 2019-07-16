class Fuel:

    def __init__(self, ch4=0, ch2h4=0, co2=0, co=0, o2=0, n2=0):
        self.ch4 = ch4
        self.ch2h4 = ch2h4
        self.co2 = co2
        self.co = co
        self.o2 = o2
        self.n2 = n2


class Mollier:
    def __init__(self, fuel):
        self.fuel = fuel
        self.ot = self.calculate_ot()
        self.vc = self.calculate_vc()
        self.vn = self.calculate_vn()
        self.sigma = self.calculate_sigma()
        self.nu = self.calculate_nu()

    def calculate_ot(self):
        return self.fuel.ch4 / 100 * 2 + self.fuel.ch2h4 / 100 * 3 + self.fuel.co / 100 * 0.5 + self.fuel.o2/100

    def calculate_vc(self):
        return (self.fuel.ch4 / 100) + ((self.fuel.ch2h4 / 100) * 2) + (self.fuel.co2 / 100) + (self.fuel.co / 100)

    def calculate_vn(self):
        return self.fuel.n2 / 100

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
