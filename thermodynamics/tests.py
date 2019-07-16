import unittest

from thermodynamics.oswaldt_calculations import MoleculeMix, Formula, Element, FormulaNode


class TestFormulaClass(unittest.TestCase):
    def test_nodes(self):
        h2o=Formula(elements=[Element(1,name="H"),Element(8,name="O")],quantities=[2,1])
        self.assertEqual(FormulaNode(Element(1,name="H"),2),h2o.formula()[0] )


class TestMoleculeMixClass(unittest.TestCase):
    def test_init_total_atoms(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = MoleculeMix(molecules)
        self.assertEqual(3, f.total_atoms)

    def test_init_total_mass(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = MoleculeMix(molecules)
        self.assertEqual(18, f.total_mass)

    def test_percentage_atoms(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = MoleculeMix(molecules)
        self.assertEqual(1 / 3, f.atoms_percentage("O"))

    def test_percentage_atoms2(self):
        molecules = {
            "H": 0.3,
            "O": 0.7
        }
        f = MoleculeMix(molecules)
        self.assertEqual(0.7, f.atoms_percentage("O"))

    def test_mass_percentage(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = MoleculeMix(molecules)
        self.assertEqual(16 / 18, f.mass_percentage("O"))


class TestOslwaldtCalculationsClass(unittest.TestCase):
    pass
    # def test_calculate_alpha(self):
    #     molecules = {
    #         "H": 2,
    #         "O": 1,
    #         "C": 1
    #     }
    #     f = MoleculeMix(molecules)
    #     ocal = OslwaldtCalculations(f)
    #     self.assertEqual(4.4437500000000005, ocal.alpha)
    #
    # def test_maxco2(self):
    #     molecules = {
    #         "H": 4,
    #         "C": 1
    #     }
    #     f = MoleculeMix(molecules)
    #     ocal = OslwaldtCalculations(f)
    #     self.assertEqual(11.7, ocal.max_co2)

    # def test_maxco(self):
    #     molecules = {
    #         "H": 4,
    #         "C": 1
    #     }
    #     f = Fuel(molecules)
    #     ocal = OslwaldtCalculations(f)
    #     self.assertEqual(4.4437500000000005, ocal.alpha)
