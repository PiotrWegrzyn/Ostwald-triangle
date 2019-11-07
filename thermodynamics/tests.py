import unittest

from molmass import Formula, FormulaError, ELEMENTS

from thermodynamics.carbohydrate import Carbohydrate
from thermodynamics.composition import CompositionNode, Composition
from thermodynamics.formula_wrapper import FormulaWrapper
from thermodynamics.mollier import Mollier
from thermodynamics.ostwald_calculations import OstwaldCalculations


class TestCompositionNode(unittest.TestCase):
    def test_init_raises_value_error_when_wrong_formula_type(self):
        with self.assertRaises(ValueError):
            CompositionNode(1, 1)

    def test_init_raises_value_error_when_proportion_is_negative(self):
        with self.assertRaises(ValueError):
            CompositionNode(FormulaWrapper("H2O"), -1)

    def test_init_raises_value_error_when_proportion_is_more_than_1(self):
        with self.assertRaises(ValueError):
            CompositionNode(FormulaWrapper("H2O"), 1.1)

    def test_amount_of_h_mass_in_watter_with05_proportion(self):
        proportion = 0.5
        cn = CompositionNode(FormulaWrapper("H2O"), proportion)
        self.assertEqual(proportion * (ELEMENTS["H"].mass * 2)/(ELEMENTS["H"].mass *2 + ELEMENTS["O"].mass), cn["H"])

    def test_amount_of_not_existing_element_returns0(self):
        proportion = 0.5
        cn = CompositionNode(FormulaWrapper("H2O"), proportion)
        self.assertEqual(0, cn["C"])

    def test_init_with_str(self):
        cn = CompositionNode("O", 1)
        self.assertTrue(cn)


class TestMolmass(unittest.TestCase):
    def test_amount_of_H_atoms(self):
        f = Formula('(H)20 O10 H20')
        self.assertEqual(40, f._elements.get("H")[0])

    def test_from_string(self):
        string = "H2O"
        f = Formula(string)
        self.assertEqual("H2O", f.formula)

    def test_not_chemically_correct_formula_mass(self):
        f = Formula("HHHH")
        self.assertEqual(4.03176, f.mass)

    def test_float_numbers(self):
        f = Formula("H0.5")
        with self.assertRaises(FormulaError):
            m = f.mass

    def test_composition_mass(self):
        f = Formula("H2O")
        comp = f.composition()
        self.assertEqual(0.11189834407236524, comp[0][3])

    def test_composition_mass_not_chemically_correct(self):
        f = Formula("H2OHHO")
        comp = f.composition()
        self.assertEqual(0.11189834407236524, comp[0][3])


class TestFormulaWrapper(unittest.TestCase):

    def test_get_item(self):
        f = FormulaWrapper("HHHH")
        self.assertEqual(4, f["H"])

    def test_get_mass_percentage(self):
        f = FormulaWrapper("H2O")
        self.assertEqual(0.11189834407236524, f.percentage_mass("H"))


class TestCompositionClass(unittest.TestCase):
    def test_init_args(self):
        fuel = Composition(
            CompositionNode(FormulaWrapper("C"), 0.7),
            CompositionNode(FormulaWrapper("H"), 0.043)
        )
        self.assertEqual(0.7, fuel["C"])

    def test_init_args_as_list(self):
        args = [
            CompositionNode(FormulaWrapper("C"), 0.7),
            CompositionNode(FormulaWrapper("H"), 0.043)
        ]
        fuel = Composition(*args)
        self.assertEqual(0.7, fuel["C"])

    def test_complex_formula_in_init(self):
        args = [
            CompositionNode(FormulaWrapper("C2H4"), 0.7),
            CompositionNode(FormulaWrapper("H"), 0.043)
        ]
        fuel = Composition(*args)
        with self.assertRaises(KeyError):
            c = fuel["C2H4"]


    def test_non_existing_element_returns0(self):
        args = [
            CompositionNode(FormulaWrapper("C"), 0.7),
            CompositionNode(FormulaWrapper("H"), 0.043)
        ]
        fuel = Composition(*args)
        self.assertEqual(0, fuel["O"])

    def test_init_throws_value_error_when_arg_not_composition_node(self):
        with self.assertRaises(ValueError):
            Composition("")

    def test_init_with_empty_list_returns0(self):
        fuel = Composition()
        self.assertEqual(0, fuel["O"])

    def test_creates_composition_nodes_from_tuples_on_init(self):
        fuel = Composition(
            ("H", 1)
        )
        self.assertEqual(1, fuel["H"])

    def test_is_gas_true_when_ch4_present(self):
        fuel = Composition(
            ("S", 0.11),
            ("CH4", 0.11)
        )
        self.assertEqual(True, fuel.is_gas)

    def test_is_gas_true_when_c2h6_present(self):
        fuel = Composition(
            ("S", 0.11),
            ("C2H6", 0.11)
        )
        self.assertEqual(True, fuel.is_gas)

    def test_is_gas_true_when_c3h8_present(self):
        fuel = Composition(
            ("S", 0.11),
            ("C3H8", 0.11)
        )
        self.assertEqual(True, fuel.is_gas)

    def test_is_gas_false_when_not_gas(self):
        fuel = Composition(
            ("S", 0.11),
            ("C", 0.11)
        )
        self.assertEqual(False, fuel.is_gas)

    def test_is_gas_false_when_CH_prop_is_0(self):
        fuel = Composition(
            ("S", 0.11),
            ("CH4", 0)
        )
        self.assertEqual(False, fuel.is_gas)

    def test_proportion_of_formula(self):
        fuel = Composition(
            ("S", 0.11),
            ("CH4", 0.10)
        )
        self.assertEqual(0.10, fuel.proportion_of_formula("CH4"))

    def test_proportion_of_formula_not_matching_capitalization(self):
        fuel = Composition(
            ("S", 0.11),
            ("CH4", 0.10)
        )
        self.assertEqual(0.10, fuel.proportion_of_formula("Ch4"))

    def test_proportion_of_formula_returns_0_when_nothing_found(self):
        fuel = Composition(
            ("S", 0.11),
            ("CH4", 0.10)
        )
        self.assertEqual(0, fuel.proportion_of_formula("not_existing_formula"))


class TestMollierClass(unittest.TestCase):
    # data from page 75
    def test_ot(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(1.496, round(m.Ot, 3))

    def test_vc(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        m = Mollier(f)
        self.assertEqual(1.308, round(m.vc, 3))

    def test_vn(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(0.01, round(m.vn, 2))

    def test_vocoh2o(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(0.842, round(m.Ocoh2o, 3))  # the book says 8.843 but it should be 0.842

    def test_v0(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(7.122, round(m.vo, 3))

    def test_vco(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(1.308, round(m.vco, 3))

    def test_n2(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(5.637, round(m.vn2, 3))

    def test_vo0s(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(7.6, round(m.v0s, 1))

    def test_vo2(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        m = Mollier(f)
        self.assertEqual(0.654, round(m.vo2, 3))

    # data from page 84
    # #wrong
    # def test_ot_formula(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(1.94, round(m.Ot, 2))
    #
    # #wrong
    # def test_vc_formula(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(0.984, round(m.vc, 3))
    #
    # # wrong
    # def test_vn_formula(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(0.022, round(m.vn, 3))
    #
    # def test_vocoh2o(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(1.451, round(m.Ocoh2o, 3))  # the book says 8.843 but it should be 0.842
    #
    # #wrong
    # def test_v0(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(round(m.Ot*4.76, 3), round(m.vo, 3))
    #
    # #wrong
    # def test_vco(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(0.978, round(m.vco, 3))
    #
    # #wrong
    # def test_n2(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(7.317, round(m.vn2, 3))
    #
    # # worng
    # def test_vo0s(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(8.8, round(m.v0s, 1))
    #
    # #worng
    # def test_vo2(self):
    #     f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
    #     m = Mollier(f)
    #     self.assertEqual(0.489, round(m.vo2, 3))

    def test_ot_79(self):
        f = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        m = Mollier(f)
        self.assertAlmostEqual(1.253, m.Ot, delta=0.01)

    def test_vc_s79(self):
        f = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        m = Mollier(f)
        self.assertEqual(1.121, round(m.vc, 3))
        self.assertAlmostEqual(4.772, m.vn2, delta=0.01)

    def test_vn2_s79(self):
        f = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        m = Mollier(f)
        self.assertAlmostEqual(4.772, m.vn2, delta=0.01)

    def test_v0_s79(self):
        f = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        m = Mollier(f)
        self.assertAlmostEqual(5.964, m.vo, delta=0.01)

    # def test_ot_s82(self):
    #     f = Composition(("C", 0.874), ("H", 0.112), ("S", 0.005), ("O", 0.009))
    #     m = Mollier(f)
    #     self.assertEqual(2.261, round(m.ot, 3))
    #
    # def test_vc_s82(self):
    #     f = Composition(("C", 0.874), ("H", 0.112), ("S", 0.005), ("O", 0.009))
    #     m = Mollier(f)
    #     self.assertEqual(1.638, round(m.vc, 3))
    #
    # def test_vn_s82(self):
    #     f = Composition(("C", 0.874), ("H", 0.112), ("S", 0.005), ("O", 0.009))
    #     m = Mollier(f)
    #     self.assertEqual(0, round(m.vn, 3))
    #
    # def test_vs_s82(self):
    #     f = Composition(("C", 0.874), ("H", 0.112), ("S", 0.005), ("O", 0.009))
    #     m = Mollier(f)
    #     self.assertEqual(0, round(m.vn, 3))


class TestOslwaldtCalculationsClass(unittest.TestCase):
    def test_kmax_s84(self):
        f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(11.85, round(ocal.kmax, 2))

    def test_maxco_s84(self):
        f = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(15.25, round(ocal.max_co, 2))

    def test_kmax_s75(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(18.83, round(ocal.kmax, 2))

    def test_maxco_s75(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(29.16, round(ocal.max_co, 2))

    def test_maxco_pointc_co(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(17.2, round(ocal.C.co, 1))

    def test_maxco_pointc_o2(self):
        f = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(8.6, round(ocal.C.o2, 1))

    def test_kmax_s79(self):
        f = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        ocal = OstwaldCalculations(f, 6, 2)
        self.assertEqual(19.17, round(ocal.kmax, 2))


class TestCarbohydrates(unittest.TestCase):
    def test_get_name(self):
        name = Carbohydrate.get_name(2, 4)
        self.assertEqual("C2H4", name)

    def test_get_name_omits_ones_in_name(self):
        name = Carbohydrate.get_name(1, 1)
        self.assertEqual("CH", name)

    def test_get_all_lenght(self):
        all_carbs= Carbohydrate.get_all()
        self.assertEqual(28, len(all_carbs))

    def test_get_all_first_element(self):
        all_carbs= Carbohydrate.get_all()
        self.assertEqual(Carbohydrate(1, 4).name, all_carbs[0].name)

