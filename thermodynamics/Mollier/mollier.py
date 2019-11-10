from thermodynamics.Mollier.mollier_gas_state_calculator import MollierGasStateCalculator
from thermodynamics.Mollier.mollier_solid_state_calculator import MollierSolidStateCalculator
from thermodynamics.Utlis.composition import Composition


class Mollier:
    def __init__(self, fuel):
        if not isinstance(fuel, Composition):
            raise ValueError("fuel needs to by of type Composition")
        self.fuel = fuel
        if self.fuel.is_gas:
            self.calculator = MollierGasStateCalculator(fuel)
        else:
            self.calculator = MollierSolidStateCalculator(fuel)

    def __getattr__(self, attr):
        return getattr(self.calculator, attr)
