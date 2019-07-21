from kivy.uix.floatlayout import FloatLayout

from models.ostwaldtriangle import OstwaldTriangle
from thermodynamics.ostwald_calculations import OstwaldCalculations, Composition


class OstwaldTriangleVisualization(FloatLayout):

    def __init__(self, **kwargs):
        fuel = kwargs.pop("fuel", None)
        super().__init__(**kwargs)
        fuels84 = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
        fuels79 = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        fuels75 = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))
        if fuel:
            try:
                fuel = self.create_composition(fuel)
            except:
                fuel = fuels75

        else:
            fuel = fuels75
        osw_calc = OstwaldCalculations(fuel, 6, 2)
        self.ostwald_triangle_graph = OstwaldTriangle(osw_calc)
        self.ostwald_triangle_graph.draw(self.canvas)

    def create_composition(self, text):
        split_text = text.split(" ")
        res = [(split_text[i], float(split_text[i + 1]) / 100) for i in range(0, len(split_text), 2)]
        return Composition(*res)