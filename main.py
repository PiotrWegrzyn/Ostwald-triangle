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
from geometry import PolygonalChain
from graph import Graph

kivy.require('1.9.0')


class Drawer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas

    def lines_between_2_lines(self, line1, line2, amount_of_vectors, vector_width, color=(0, 0, 0), w1=None, w2=None):
        line1_points = line1.get_split_points(amount_of_vectors, w1)
        line2_points = line2.get_split_points(amount_of_vectors, w2)
        for start, end in zip(line1_points, line2_points):
            self.draw_line(geometry.Vector(start, end), vector_width, color)

    def draw_line(self, vector, vector_width=1, color=(0, 0, 0)):
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

    graph = Graph(18.9,21,28)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1150, 700)
        Window.top = 75
        Window.left = 200

        self.drawer = Drawer(self.graph, self.canvas)
        self.drawer.draw_line(self.graph.lines["co2"].line, 2)
        self.drawer.draw_line(self.graph.lines["co"].line, 1.5)
        self.drawer.draw_line(self.graph.lines["o2"].line, 1.5)
        self.drawer.draw_line(self.graph.lines["coefficient"].line, 1.5)
        self.drawer.draw_line(self.graph.lines["bot"].line, 2)
        self.drawer.draw_line(self.graph.lines["diagonal"].line, 2)

        self.drawer.lines_between_2_lines(
            self.graph.lines['co2'].line,
            self.graph.lines["diagonal"].line.reversed(),
            self.graph.lines['co2'].number_of_lines,
            vector_width=1.5
        )
        self.drawer.lines_between_2_lines(
            self.graph.lines['diagonal'].line,
            self.graph.lines["bot"].line,
            self.graph.lines['o2'].number_of_lines,
            vector_width=1.5
        )
        self.drawer.lines_between_2_lines(
            self.graph.lines['o2'].line,
            self.graph.lines["diagonal"].line,
            self.graph.lines['o2'].number_of_lines,
            vector_width=1
        )
        self.drawer.lines_between_2_lines(
            self.graph.lines["co2"].line,
            self.graph.lines["co"].line.reversed(),
            self.graph.lines['co'].number_of_lines,
            vector_width=1
        )

        pc = PolygonalChain([self.graph.lines['co2'].line, self.graph.lines['diagonal'].line])
        wages = self.wages_for_coefficient_lines()
        self.drawer.lines_between_2_lines(self.graph.lines['coefficient'].line.reversed(), pc, len(wages), 1, w2=wages)

    def wages_for_coefficient_lines(self):
        center = self.graph.lines['co2'].line.length / (self.graph.lines['co2'].line.length + self.graph.lines['diagonal'].line.length)
        scaled_center = int(center * 1000)
        step = int(scaled_center /self.graph.lines['co2'].number_of_lines)
        wages = [0] \
                + [s / 1000 for s in range(step, scaled_center, step)] \
                + [center] \
                + [s / 1000 for s in range(scaled_center + step, 1000, step)] \
                + [1]

        return wages


class TestvectorApp(App):
    def build(self):
        return OstwaldTriangleVisualization()


if __name__ == '__main__':
    TestvectorApp().run()