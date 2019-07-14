
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.modules import keybinding
from kivy.uix.floatlayout import FloatLayout

from models.ostwaldtriangle import OstwaldTriangle
from models.table import Table

kivy.require('1.9.0')


class OstwaldTriangleVisualization(FloatLayout):
    ostwald_triangle_graph = OstwaldTriangle(18.9, 21, 28)
    table = Table()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1150, 750)
        Window.top = 75
        Window.left = 200
        self.ostwald_triangle_graph.draw(self.canvas)
        self.table.draw(self.canvas)
        self.export_to_png("triangle.png")


class OstwaldTriangleApp(App):
    def build(self):
        main_widget = OstwaldTriangleVisualization(size=(Window.size[0]+200, Window.size[1]))
        keybinding.start(Window, main_widget)

        return main_widget


if __name__ == '__main__':
    OstwaldTriangleApp().run()
