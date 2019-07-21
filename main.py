import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from gui.About.about_screen import AboutScreen
from gui.drawing.drawing_screen import DrawingScreen
from gui.drawing.ostwald_triangle_visualization import OstwaldTriangleVisualization
from gui.fuel_comp.set_composition_screen import SetCompositionScreen
from gui.main_menu.menu_screen import MainMenuScreen
from gui.measured_comp.measured_composition_screen import SetMeasuredScreen
from gui.show_popup import show_popup

kivy.require('1.9.0')


class OstwaldTriangleApp(App):
    def build(self):
        self.menu = MainMenuScreen(name='menu')
        self.menu.about_button.bind(on_press=self.show_about)
        self.menu.draw_button.bind(on_press=self.draw_callback)
        self.menu.set_fuel_button.bind(on_press=self.show_set_fuel_composition_menu)
        self.menu.set_measured_button.bind(on_press=self.show_set_measured_composition_menu)

        self.about = AboutScreen(name='about')
        self.about.back_button.bind(on_press=self.show_menu)

        self.menu_fuel_composition = SetCompositionScreen(name='set_fuel_composition')
        self.menu_fuel_composition.back_button.bind(on_press=self.show_menu)

        self.menu_measured_composition = SetMeasuredScreen(name='set_measured_composition')
        self.menu_measured_composition.back_button.bind(on_press=self.show_menu)

        self.drawing = DrawingScreen(name='drawing')
        self.drawing.export_button.bind(on_press=self.callback_export)
        self.drawing.back_button.bind(on_press=self.show_menu)
        self.draw_triangle()

        self.sm = ScreenManager()
        self.sm.add_widget(self.menu)
        return self.sm

    def show_about(self, btn):
        self.sm.switch_to(self.about, direction=btn.transition_method)

    def draw_callback(self, btn):
        self.draw_triangle()
        self.sm.switch_to(self.drawing, direction="up")

    def draw_triangle(self):
        self.triangle = OstwaldTriangleVisualization(
            fuel=self.parse_input_to_composition(),
            measured_co2=self.get_measured_co2(),
            measured_o2=self.get_measured_o2()
        )
        self.drawing.scatter_triangle.clear_widgets()
        self.drawing.scatter_triangle.add_widget(self.triangle)

    def callback_export(self, btn):
        self.export_photo(self.drawing.drawing_layout)

    def show_menu(self, btn):
        self.sm.switch_to(self.menu, direction=btn.transition_method)

    def show_set_fuel_composition_menu(self, btn):
        self.sm.switch_to(self.menu_fuel_composition, direction=btn.transition_method)

    def show_set_measured_composition_menu(self, btn):
        self.sm.switch_to(self.menu_measured_composition, direction=btn.transition_method)

    @staticmethod
    def export_photo(widget):
        photo_name = "Ostwald-"+datetime.now().strftime("%y-%m-%d %H-%M-%S-%f")+".png"
        p = os.path.join("Exports", photo_name)
        widget.export_to_png(p)

    def parse_input_to_composition(self):
        inputs = self.menu_fuel_composition.input_widget.get_inputs()
        composition = []
        for row in inputs:
            chemical = row[0].text
            try:
                proportion = float(row[1].text) / 100
            except ValueError:
                proportion = 0
            if chemical is not "":
                composition.append((chemical, proportion))
        return composition

    def get_measured_co2(self):
        given_co2 = self.menu_measured_composition.co2_input.text
        try:
            return float(given_co2)
        except:
            show_popup("Error", 'There was a problem reading measured CO2.')
            return 0

    def get_measured_o2(self):
        given_co2 = self.menu_measured_composition.o2_input.text
        try:
            return float(given_co2)
        except:
            show_popup("Error", 'There was a problem reading measured O2.')
            return 0


if __name__ == '__main__':
    # Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'fullscreen', 'False')
    # Config.set('graphics', 'window_state', 'maximize')
    Config.set('graphics', 'window_state', 'visible')
    Config.write()
    Window.clearcolor = (194/255, 194/255, 214/255, .69)
    OstwaldTriangleApp().run()
