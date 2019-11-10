from kivy.uix.floatlayout import FloatLayout

from models.table import Table


class ResultTableVisualization(FloatLayout):
    def __init__(self, oswald_calculations, phi_result, **kwargs):
        super().__init__(**kwargs)

        phi_data = [["Variable", "Value"]]
        phi_data.append(["Phi:", phi_result])
        phi_data.append(["Lambda:", round(1/phi_result,2)])
        phi_data.append(["Max CO:", oswald_calculations.max_co])
        phi_data.append(["Max CO2:", oswald_calculations.max_co2])
        phi_data.append(["Fuel:", ""])
        for fuel_comp_node in oswald_calculations.fuel.composition_nodes:
            phi_data.append([fuel_comp_node.formula, fuel_comp_node.proportion])

        self.table = Table(75, 45, phi_data)
        self.table.draw(self.canvas)
