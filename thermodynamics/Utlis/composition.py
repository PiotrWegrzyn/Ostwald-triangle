from thermodynamics.Utlis.formula_wrapper import FormulaWrapper
from thermodynamics.carbohydrate import Carbohydrate


class CompositionNode:
    def __init__(self, *args):
        self.formula = FormulaWrapper("")
        self.proportion = 0.0

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
            if isinstance(cn, (tuple, list)):
                self.composition_nodes[i] = CompositionNode(cn)
            elif not isinstance(cn, CompositionNode):
                raise ValueError("arguments should only contain CompositionNodes")
        self.validate_proportion_range()

    def mass_percentage(self, element):
        return round(sum(node[element] for node in self.composition_nodes), 4)

    def __getitem__(self, item):
        return self.mass_percentage(item)

    def __contains__(self, item):
        return self[item] > 0

    def validate_proportion_range(self):
        sum_proportions = sum(node.proportion for node in self.composition_nodes)
        if sum_proportions > 1:
            raise ValueError("Sum of proportions is more than 1.")
        if sum_proportions < 0:
            raise ValueError("Sum of proportions is less than 0.")

    @property
    def is_gas(self):
        for carbohydrate in Carbohydrate.get_all():
            if self.contains_formula(carbohydrate.name):
                return True
        return False

    def contains_formula(self, formula):
        return self.proportion_of_formula(formula) > 0

    def proportion_of_formula(self, formula):
        return sum([node.proportion for node in self.composition_nodes if str(node.formula.formula).upper() == formula.upper()])