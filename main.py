
import kivy
from kivy.app import App
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout

from ostwaldtriangle import OstwaldTriangle

kivy.require('1.9.0')


class OstwaldTriangleVisualization(FloatLayout):
    ostwald_triangle_graph = OstwaldTriangle(18.9, 21, 28)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1150, 700)
        Window.top = 75
        Window.left = 200

        self.ostwald_triangle_graph.draw(self.canvas)


class OstwaldTriangleAppn(App):
    def build(self):
        return OstwaldTriangleVisualization()


if __name__ == '__main__':
    OstwaldTriangleAppn().run()