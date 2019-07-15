import unittest

from thermodynamics.oswaldt_calculations import Fuel, OslwaldtCalculations


class TestFuelClass(unittest.TestCase):
    def test_init_total_atoms(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = Fuel(molecules)
        self.assertEqual(3, f.total_atoms)

    def test_init_total_mass(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = Fuel(molecules)
        self.assertEqual(18, f.total_mass)

    def test_percentage_atoms(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = Fuel(molecules)
        self.assertEqual(1 / 3, f.atoms_percentage("O"))

    def test_mass_percentage(self):
        molecules = {
            "H": 2,
            "O": 1
        }
        f = Fuel(molecules)
        self.assertEqual(16 / 18, f.mass_percentage("O"))


class TestOslwaldtCalculationsClass(unittest.TestCase):
    def test_calculate_alpha(self):
        molecules = {
            "H": 2,
            "O": 1,
            "C": 1
        }
        f = Fuel(molecules)
        ocal = OslwaldtCalculations(f)
        self.assertEqual(4.4437500000000005, ocal.alpha)

    def test_maxco2(self):
        molecules = {
            "H": 4,
            "C": 1
        }
        f = Fuel(molecules)
        ocal = OslwaldtCalculations(f)
        self.assertEqual(11.7, ocal.max_co2)

    # def test_maxco(self):
    #     molecules = {
    #         "H": 4,
    #         "C": 1
    #     }
    #     f = Fuel(molecules)
    #     ocal = OslwaldtCalculations(f)
    #     self.assertEqual(4.4437500000000005, ocal.alpha)
