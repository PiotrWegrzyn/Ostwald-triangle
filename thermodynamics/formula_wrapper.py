from molmass import Formula


class FormulaWrapper(Formula):
    def __getitem__(self, item):
        return self._elements[item][0]

    def percentage_mass(self, element):
        return self[element]*Formula(element).mass / self.mass
