from thermodynamics.formula_wrapper import FormulaWrapper


class Carbohydrate:

    def __init__(self, c, h):
        if c < 1 or h < 1:
            raise ValueError("C and H need to be positive numbers")
        self.c = c
        self.h = h
        self.name = self.get_name(c, h)
        self.formula = FormulaWrapper(self.name)

    @staticmethod
    def get_name(c, h):
        if c is 1:
            c = ""
        if h is 1:
            h = ""
        return 'C' + c.__str__() + 'H' + h.__str__()

    @classmethod
    def get_all(cls):
        carbs = []
        carbs.append(cls(1, 4))
        for c in range(2, 11):
            carbs.append(cls(c, 2*c + 2))
            carbs.append(cls(c, 2*c))
            carbs.append(cls(c, 2*c - 2))
        return carbs

