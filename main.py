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

kivy.require('1.9.0')


class OstwaldTriangleVisualization(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ostwald_triangle_graph = OstwaldTriangle(18.9, 21, 29.2)
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
