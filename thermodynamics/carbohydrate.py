from thermodynamics.Utlis.formula_wrapper import FormulaWrapper


class Carbohydrate:
    ALKAN = "Alkan"
    ALKEN = "Alken"
    ALKIN = "Alkin"

    def __init__(self, c, h):
        if c < 1 or h < 1:
            raise ValueError("C and H need to be positive numbers")
        self.carbon = c
        self.hydrogen = h
        self.type = self.get_type(c, h)
        self.name = self.get_name(c, h)
        self.formula = FormulaWrapper(self.name)

    @staticmethod
    def get_name(carbon, hydrogen):
        if carbon is 1:
            carbon = ""
        if hydrogen is 1:
            hydrogen = ""
        return 'C' + carbon.__str__() + 'H' + hydrogen.__str__()

    @classmethod
    def get_all(cls):
        carbs = []
        carbs.append(cls(1, 4))
        for c in range(2, 11):
            carbs.append(cls(c, 2*c + 2))
            carbs.append(cls(c, 2*c))
            carbs.append(cls(c, 2*c - 2))
        return carbs

    @staticmethod
    def get_type(c, h):
        if c * 2 == h:
            return Carbohydrate.ALKEN
        elif c * 2 + 2 == h:
            return Carbohydrate.ALKAN
        elif c * 2 - 2 == h:
            return Carbohydrate.ALKIN

