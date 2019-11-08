from thermodynamics.mollier_gas_state_calculator import MollierGasStateCalculator
from thermodynamics.mollier_solid_state_calculator import MollierSolidStateCalculator


class Mollier:
    def __init__(self, fuel):
        self.fuel = fuel
        if self.fuel.is_gas:
            self.calculator = MollierGasStateCalculator(fuel)
        else:
            self.calculator = MollierSolidStateCalculator(fuel)

    def __getattr__(self, attr):
        return getattr(self.calculator, attr)
