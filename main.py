import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.modules import keybinding
from kivy.uix.floatlayout import FloatLayout

from models.ostwaldtriangle import OstwaldTriangle
from models.table import Table
from thermodynamics.ostwald_calculations import OstwaldCalculations, Composition

kivy.require('1.9.0')


class OstwaldTriangleVisualization(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        fuels84 = Composition(("CH4", 0.958), ("C2H4", 0.008), ("CO", 0.004), ("O2", 0.002), ("CO2", 0.006), ("N2", 0.022))
        fuels79 = Composition(("C", 0.5921), ("H", 0.0377), ("S", 0.0211), ("O", 0.112), ("N", 0.0128))
        fuels75 = Composition(("C", 0.7), ("H", 0.043), ("O", 0.075), ("N", 0.013))

        fuel = fuels79
        osw_calc = OstwaldCalculations(fuel, 6, 2)
        self.ostwald_triangle_graph = OstwaldTriangle(osw_calc.max_co2, osw_calc.max_o2, osw_calc.max_co)
        self.table = Table()
        self.ostwald_triangle_graph.draw(self.canvas)
        self.table.draw(self.canvas)
        self.export_photo()

    def export_photo(self):
        photo_name = "Ostwald-"+datetime.now().strftime("%y-%m-%d %H-%M-%S-%f")+".png"
        p = os.path.join("Exports", photo_name)
        self.export_to_png(p)


class OstwaldTriangleApp(App):
    def build(self):
        main_widget = OstwaldTriangleVisualization(size=(Window.size[0]+200, Window.size[1]))
        keybinding.start(Window, main_widget)

        return main_widget


if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    Window.clearcolor = (1, 1, 1, 1)
    OstwaldTriangleApp().run()
