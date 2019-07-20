import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput

from models.ostwaldtriangle import OstwaldTriangle
from models.table import Table
from thermodynamics.ostwald_calculations import OstwaldCalculations, Composition

kivy.require('1.9.0')


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


class TableVisuallization(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.table = Table(3, 95)
        self.table.draw(self.canvas)


class MenuScreen(Screen):
    pass


class DrawingScreen(Screen):
    pass


class OstwaldTriangleApp(App):
    def build(self):
        self.menu = MenuScreen(name='menu')
        self.menu_layout = BoxLayout(orientation="vertical")
        self.menu.add_widget(self.menu_layout)

        self.draw_button = Button(text="Draw", size=(1, 0.3))
        self.draw_button.bind(on_press=self.draw_triangle)
        self.input = TextInput(
            text="CH4 95.8 C2H4 0.8 CO 0.4 O2 0.2 CO2 0.6 N2 2.2",
            size=(1, 0.3)
        )
        self.menu_layout.add_widget(self.draw_button)
        self.menu_layout.add_widget(self.input)


        self.drawing = DrawingScreen(name='drawing')
        self.drawing_layout = BoxLayout(orientation="horizontal", size=(Window.size[0], Window.size[1]))
        self.drawing.add_widget(self.drawing_layout)

        self.scatter_triangle = Scatter(do_rotation=False)
        self.triangle = OstwaldTriangleVisualization()
        self.scatter_triangle.add_widget(self.triangle)

        self.drawing_layout_menu = BoxLayout(orientation="vertical", size_hint=(0.1,1))

        self.back_button = Button(text="Back", size_hint=(1, 0.7))
        self.back_button.bind(on_press=self.show_menu)

        self.drawing_layout.add_widget(TableVisuallization(size_hint=(0.001, 1)))
        self.drawing_layout.add_widget(self.scatter_triangle)
        self.drawing_layout.add_widget(self.drawing_layout_menu)

        self.export_button = Button(text="Export", size_hint=(1, 0.7))
        self.export_button.bind(on_press=self.callback_export)

        self.drawing_layout_menu.add_widget(self.back_button)
        self.drawing_layout_menu.add_widget(self.export_button)


        self.sm = ScreenManager()
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.drawing)
        return self.sm

    def draw_triangle(self, button_instance):
        self.triangle = OstwaldTriangleVisualization(fuel=self.input.text)
        self.scatter_triangle.clear_widgets()
        self.scatter_triangle.add_widget(self.triangle)
        self.sm.switch_to(self.drawing, direction="left")

    def callback_export(self, btn):
        self.export_photo(self.drawing_layout)

    def show_menu(self, b):
        self.sm.switch_to(self.menu, direction='right')

    @staticmethod
    def export_photo(widget):
        photo_name = "Ostwald-"+datetime.now().strftime("%y-%m-%d %H-%M-%S-%f")+".png"
        p = os.path.join("Exports", photo_name)
        widget.export_to_png(p)


if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    # Config.set('graphics', 'fullscreen', 'False')
    Config.set('graphics', 'window_state', 'maximize')
    # Config.set('graphics', 'window_state', 'visible')
    Config.write()
    Window.clearcolor = (1, 1, 1, 1)
    OstwaldTriangleApp().run()
