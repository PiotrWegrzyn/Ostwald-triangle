from thermodynamics.formula_wrapper import FormulaWrapper


class CompositionNode:
    def __init__(self, *args):
        if len(args) is 1:
            if not isinstance(args[0], (tuple, list)):
                raise ValueError("Can create only from list or tuple.")
            self.formula = args[0][0]
            self.proportion = args[0][1]
        else:
            self.formula = args[0]
            self.proportion = args[1]
        if isinstance(self.formula, str):
            self.formula = FormulaWrapper(self.formula)
        elif not isinstance(self.formula, FormulaWrapper):
            raise ValueError("Formula is not an instance of " + FormulaWrapper.__name__ + "nor a string.")
        if 0 > self.proportion or self.proportion > 1:
            raise ValueError("Proportion should be a number in range <0,1>")

    def mass_percentage(self, iso_element_name):
        return self.formula.percentage_mass(iso_element_name) * self.proportion

    def __getitem__(self, iso_element_name):
        return self.mass_percentage(iso_element_name)


class Composition:
    composition_nodes = []

    def __init__(self, *args):
        self.composition_nodes = list(args)
        for i, cn in enumerate(self.composition_nodes):
            if isinstance(cn, tuple):
                self.composition_nodes[i] = CompositionNode(cn)
            elif not isinstance(cn, CompositionNode):
                raise ValueError("arguments should only contain CompositionNodes")
        self.validate_proportion_range()

    def mass_percentage(self, element):
        return round(sum(node[element] for node in self.composition_nodes), 4)

    def __getitem__(self, item):
        return self.mass_percentage(item)

    def validate_proportion_range(self):
        sum_proportions = sum(node.proportion for node in self.composition_nodes)
        if sum_proportions > 1:
            raise ValueError("Sum of proportions is more than 1.")
        if sum_proportions < 0:
            raise ValueError("Sum of proportions is less than 0.")


class Mollier:
    def __init__(self, fuel):
        self.fuel = fuel
        self.ot = self.calculate_ot()
        self.vc = self.calculate_vc()
        self.vn = self.calculate_vn()
        self.vs = self.calculate_vs()
        self.sigma = self.calculate_sigma()
        self.nu = self.calculate_nu()

    def calculate_ot(self):
        return 22.42 * ((self.fuel["C"]/12) + (self.fuel["H"]/4) + (self.fuel["S"]/32) - (self.fuel["O"]/32))

    def calculate_vc(self):
        return 22.42 * ((self.fuel["C"]/12) + (self.fuel["S"] /32))

    def calculate_vs(self):
        return 22.42 * (self.fuel["S"]/28) + 0.79

    def calculate_vn(self):
        return 22.42 * (self.fuel["N"]/28)

    def calculate_sigma(self):
        return self.ot / self.vc

    def calculate_nu(self):
        return self.vn / self.vc


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

    def set_mollier(self):
        self.mollier = Mollier(self.fuel)

    def calculate_kmax(self):
        return round(100/(((79/21) * self.mollier.sigma) + self.mollier.nu + 1), 2)# percent

    def calculate_max_co(self):
        return round(100/(100 / self.kmax - 79 / 42), 2) # percent
