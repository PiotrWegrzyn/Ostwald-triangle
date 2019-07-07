from math import sin, radians

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line
from kivy.properties import NumericProperty, ListProperty, \
    BooleanProperty
from kivy.uix.floatlayout import FloatLayout

import geometry
from graph import Graph

kivy.require('1.9.0')


class Drawer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas

    def sketch_vectors_from_top(self, instructions, angle, width, distance, offset_x=0, offset_y=0):
        for i in range(1, int(self.graph.width/distance)):
            instructions.add(
                vector(
                    points=[
                        (self.graph.left + distance * i + offset_x, self.graph.top),
                        (self.graph.left + distance * i + sin(radians(angle))*self.graph.width+offset_x, self.graph.bot+offset_y)
                    ],
                    width=width)
            )

    def sketch_vectors_from_left(self, instructions, angle, width, distance, offset_x=0, offset_y=0):
        for i in range(1, int(self.graph.height/distance)):
            instructions.add(
                vector(
                    points=[
                        (self.graph.left + offset_x, self.graph.bot + distance * i),
                        (self.graph.left + distance * i + sin(radians(angle))*self.graph.width+offset_x, self.graph.bot+offset_y)
                    ],
                    width=width)
            )

    def vectors_between_2_vectors(self, vector1, vector2, amount_of_vectors, vector_width, color=(0, 0, 0)):
        vector1_points = vector1.get_split_points(amount_of_vectors)
        vector2_points = vector2.get_split_points(amount_of_vectors)
        for start, end in zip(vector1_points, vector2_points):
                self.draw_vector(geometry.Vector(start, end), vector_width, color)

    def draw_vector(self, vector, vector_width=1, color=(0, 0, 0)):
        instructions = InstructionGroup()
        self.set_color(instructions, color)
        instructions.add(
            Line(points=[(vector.start.x, vector.start.y), (vector.end.x, vector.end.y)], width=vector_width)
        )
        self.canvas.add(instructions)

    @staticmethod
    def create_color(rgb):
        return Color(rgb[0], rgb[1], rgb[2])

    def set_color(self, instructions, color):
        color = self.create_color(color)
        instructions.add(color)


class OstwaldTriangleVisualization(FloatLayout):

    close = BooleanProperty(False)
    points = ListProperty([])
    points2 = ListProperty([])
    axis_points = ListProperty([])
    sktech_points = ListProperty([])

    vectorwidth = NumericProperty(1.0)
    dt = NumericProperty(0)
    dash_length = NumericProperty(1)
    dash_offset = NumericProperty(0)
    dashes = ListProperty([])

    _update_points_animation_ev = None

    graph = Graph()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1150, 700)
        Window.top = 75
        Window.left = 200

        self.drawer = Drawer(self.graph, self.canvas)
        self.drawer.draw_vector(self.graph.lines["co2"], 2)
        self.drawer.draw_vector(self.graph.lines["co"], 1.5)
        self.drawer.draw_vector(self.graph.lines["o2"], 1.5)
        self.drawer.draw_vector(self.graph.lines["coefficient"], 1.5)
        self.drawer.draw_vector(self.graph.lines["bot"], 2)
        self.drawer.draw_vector(self.graph.lines["diagonal"], 2)

        # self.drawer.vectors_between_2_vectors(self.graph.vectors['diagonal'], self.graph.vectors["bot"], 15, 1.5)
        # self.drawer.vectors_between_2_vectors(self.graph.vectors['co2'], self.graph.vectors["diagonal"].reversed(), 15, 1.5)
        # self.drawer.vectors_between_2_vectors(self.graph.vectors["co2"], self.graph.vectors["co"].reversed(), 15, 1)
        # self.drawer.vectors_between_2_vectors(self.graph.vectors['o2'], self.graph.vectors["diagonal"], 15, 1)

        split_coefficient = self.graph.lines["coefficient"].reversed().split(2, [self.graph.lines['co2'].length,
                                                                                 self.graph.lines['diagonal'].length])
        self.drawer.vectors_between_2_vectors(split_coefficient[0], self.graph.lines['co2'], 6, 1)
        self.drawer.vectors_between_2_vectors(split_coefficient[1], self.graph.lines['diagonal'], 9,1)


class TestvectorApp(App):
    def build(self):
        return OstwaldTriangleVisualization()


if __name__ == '__main__':
    TestvectorApp().run()