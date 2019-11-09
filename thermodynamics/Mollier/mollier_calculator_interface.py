
class MoillerCalculatorInterface:
    def __init__(self, fuel):
        self.fuel = fuel
        self.Ot = self.calculate_ot()
        self.vc = self.calculate_vc()
        self.vn = self.calculate_vn()
        self.vs = self.calculate_vs()
        self.sigma = self.calculate_sigma()
        self.nu = self.calculate_nu()
        self.Ocoh2o = self.calculate_oco2ho()
        self.vo = self.calculate_vo()
        self.vco = self.calculate_vco()
        self.vco2 = self.calculate_vco2()
        self.vso2 = self.calculate_vso2()
        self.vn2 = self.calculate_vn2()
        self.vo2 = self.calculate_vo2()
        self.v0s = self.calculate_v0s()

    def calculate_ot(self):
        raise NotImplementedError()

    def calculate_oco2ho(self):
        raise NotImplementedError()

    def calculate_vo2(self):
        raise NotImplementedError()

    def calculate_vc(self):
        raise NotImplementedError()

    def calculate_vn(self):
        raise NotImplementedError()

    def calculate_vs(self):
        raise NotImplementedError()

    def calculate_sigma(self):
        raise NotImplementedError()

    def calculate_nu(self):
        raise NotImplementedError()

    def calculate_vo(self):
        raise NotImplementedError()

    def calculate_vco(self):
        raise NotImplementedError()

    def calculate_vn2(self):
        raise NotImplementedError()

    def calculate_vso2(self):
        raise NotImplementedError()

    def calculate_vco2(self):
        raise NotImplementedError()

    def calculate_v0s(self):
        raise NotImplementedError()

