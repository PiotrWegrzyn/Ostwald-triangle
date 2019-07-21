import os
from datetime import datetime

import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from gui.drawing_screen import DrawingScreen
from gui.menu_screen import MenuScreen
from gui.ostwald_triangle_visualization import OstwaldTriangleVisualization

kivy.require('1.9.0')


class OstwaldTriangleApp(App):
    def build(self):
        self.menu = MenuScreen(name='menu')
        self.menu.draw_button.bind(on_press=self.draw_triangle)

        self.drawing = DrawingScreen(name='drawing')
        self.drawing.export_button.bind(on_press=self.callback_export)
        self.drawing.back_button.bind(on_press=self.show_menu)

        self.sm = ScreenManager()
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.drawing)
        return self.sm

    def draw_triangle(self, button_instance):
        self.triangle = OstwaldTriangleVisualization(fuel="C 70 H 10 O 10 N 10")
        self.drawing.scatter_triangle.clear_widgets()
        self.drawing.scatter_triangle.add_widget(self.triangle)
        self.sm.switch_to(self.drawing, direction="up")

    def callback_export(self, btn):
        self.export_photo(self.drawing.drawing_layout)

    def show_menu(self, b):
        self.sm.switch_to(self.menu, direction='down')

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
