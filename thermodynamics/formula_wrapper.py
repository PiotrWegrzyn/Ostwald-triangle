from molmass import Formula
from molmass.elements import ELEMENTS


class FormulaWrapper(Formula):
    def __getitem__(self, item):
        return self._elements[item][0]

    def percentage_mass(self, element):
        return self[element]*ELEMENTS[element].mass / self.mass
