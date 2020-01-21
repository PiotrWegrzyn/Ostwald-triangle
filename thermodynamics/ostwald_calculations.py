from thermodynamics.Mollier.mollier import Mollier


class OstwaldCalculations:

    def __init__(self, fuel, read_co2, read_o2):
        self.read_co2 = read_co2
        self.read_o2 = read_o2
        self.fuel = fuel
        self.mollier = None
        self.set_mollier()
        self.kmax = self.calculate_kmax()
        self.max_o2 = 21
        self.max_co = self.calculate_max_co()
        self.max_co2 = self.kmax
        self.C = self.calculate_point_c()  # amount of theoretical dry exhaust
        self.P = OstwaldCalculations.Point(read_co2, read_o2)  # amount of theoretical dry exhaust

    def set_mollier(self):
        self.mollier = Mollier(self.fuel)

    def calculate_kmax(self):
        return round(100/(((79/21) * self.mollier.sigma) + self.mollier.nu + 1), 2)

    def calculate_max_co(self):
        return round(100/(100 / self.kmax - 79 / 42), 2) # percent

    def calculate_point_c(self):
        co2 = 100 * self.mollier.vco2/self.mollier.v0s
        co = 100 * self.mollier.vco/self.mollier.v0s  # 17.2
        o2 = 100 * self.mollier.vo2/self.mollier.v0s   # 8.6
        return OstwaldCalculations.Point(co2, o2, co)

    class Point:
        def __init__(self, co2=None, o2=None, co=None):
            self.co = co
            self.co2 = co2
            self.o2 = o2


