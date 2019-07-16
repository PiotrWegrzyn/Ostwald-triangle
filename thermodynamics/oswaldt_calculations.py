class Element:
    masses = {
        "H": 1,
        "O": 16,
        "S": 32.06,
        "N": 14,
        "C": 12.011,
    }

    def __init__(self, atomic_number, mass=None, name=None):
        self.name = name
        self.atomic_number = atomic_number
        self.mass = mass

    def __eq__(self, other):
        return other.atomic_number == self.atomic_number


class FormulaNode:
    def __init__(self, element, quantity):
        self.quantity = quantity
        self.element = element

    def __eq__(self, other):
        return other.element == self.element and self.quantity == other.quantity


class Formula:
    def __init__(self, elements=None, quantities=None, nodes=None):
        self.elements = elements
        self.quantities = quantities
        if nodes:
            self.nodes = nodes
        else:
            self.nodes = [FormulaNode(e, q)for e, q in zip(self.elements, self.quantities)]

    def formula(self):
        return self.nodes


class MoleculeMix:
    molecules = {}

    def __init__(self, modecules):
        self.molecules = modecules
        self.total_atoms = sum([value for key, value in self.molecules.items()])
        self.total_mass = sum([value*Element.masses[key] for key, value in self.molecules.items()])

    def atoms_percentage(self, molecule):
        return self.molecules.get(molecule, 0)/self.total_atoms

    def mass_percentage(self, molecule):
        return self.molecules.get(molecule, 0)*Element.masses[molecule]/self.total_mass


class Fuel:

    def __init__(self, ch4=0, ch2h4=0, co2=0, co=0, o2=0, n2=0):
        self.ch4 = ch4
        self.ch2h4 = ch2h4
        self.co2 = co2
        self.co = co
        self.o2 = o2
        self.n2 = n2

        def get_h_percentage():
            return self.ch4 / 100 * 2 + self.ch2h4 / 100 * 3 + self.co / 100 * 0.5

class OslwaldtCalculations:
    max_o2 = 21
    max_co2 = None
    max_co = None

    def __init__(self, fuel, co2, o2):
        self.co2 = co2
        self.o2 = o2
        self.fuel = fuel
        ot = self.fuel.ch4/100 * 2 + self.fuel.ch2h4/100 * 3 + self.fuel.co/100 * 0.5
        vc = self.fuel.ch4/100 + self.fuel.ch2h4/100 * 2 + self.fuel.co2/100 + self.fuel.co/100
        sigma = ot/vc
        nu = ot/ vc
        kmax = 100/((79/21)* sigma* nu +1) #percent

