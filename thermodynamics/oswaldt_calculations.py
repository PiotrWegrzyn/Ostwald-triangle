class Element:
    masses = {
        "H": 1,
        "O": 16,
        "S": 32.06,
        "N": 14,
        "C": 12.011,
    }

    def __init__(self, atomic_number, mass, name=None):
        self.name = name
        self.atomic_number = atomic_number
        self.mass = mass


class Molecule:
    def __init__(self, element, quantity):
        self.element = element
        self.quantity = quantity


class Fuel:
    molecules = {}

    def __init__(self, modecules):
        self.molecules = modecules
        self.total_atoms = sum([value for key, value in self.molecules.items()])
        self.total_mass = sum([value*Element.masses[key] for key, value in self.molecules.items()])

    def atoms_percentage(self, molecule):
        return self.molecules.get(molecule, 0)/self.total_atoms

    def mass_percentage(self, molecule):
        return self.molecules.get(molecule, 0)*Element.masses[molecule]/self.total_mass


class OslwaldtCalculations:
    max_o2 = 21
    max_co2 = None
    max_co = None

    def __init__(self, fuel):
        self.alpha = self.calcualte_alpha(fuel)

        self.max_co2 = 20.9/(1+(2.355*self.alpha))
        self.max_co = 20.9/(0.605+(2.355*self.alpha))

    def calcualte_alpha(self, fuel):
        h = fuel.mass_percentage("H")
        o = fuel.mass_percentage("O")
        s = fuel.mass_percentage("S")
        c = fuel.mass_percentage("C")
        return 2.37 * (h - (0.125*(o-s)))/c

    def calculate_lambda(self, air_actual, air_expected):
        return air_actual/air_expected