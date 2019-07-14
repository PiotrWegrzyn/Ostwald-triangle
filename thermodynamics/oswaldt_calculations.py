class OslwaldtCalculations:
    max_o2 = 21
    max_co2 = None
    max_co = None

    def __init__(self):
        h2h202ch4 = 1
        co2coch = 1
        H = 2.015 * h2h202ch4
        C = 12 * co2coch
        self.alpha = H/C

        self.max_co2 = 20.9/(1+(2.355*self.alpha))
        self.max_co = 20.9/(0.605+(2.355*self.alpha))
