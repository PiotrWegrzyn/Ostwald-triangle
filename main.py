from math import cos, sin, radians

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
    BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

import geometry
from graph import Graph

kivy.require('1.9.0')


class Drawer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas

    def sketch_lines_from_top(self, instructions, angle, width, distance, offset_x=0, offset_y=0):
        for i in range(1, int(self.graph.width/distance)):
            instructions.add(
                Line(
                    points=[
                        (self.graph.left + distance * i + offset_x, self.graph.top),
                        (self.graph.left + distance * i + sin(radians(angle))*self.graph.width+offset_x, self.graph.bot+offset_y)
                    ],
                    width=width)
            )

    def sketch_lines_from_left(self, instructions, angle, width, distance, offset_x=0, offset_y=0):
        for i in range(1, int(self.graph.height/distance)):
            instructions.add(
                Line(
                    points=[
                        (self.graph.left + offset_x, self.graph.bot + distance * i),
                        (self.graph.left + distance * i + sin(radians(angle))*self.graph.width+offset_x, self.graph.bot+offset_y)
                    ],
                    width=width)
            )

    def lines_between_2_lines(self, line1, line2, amount_of_lines, line_width, color=(0, 0, 0)):
        line1_points = line1.get_equally_split_points(amount_of_lines)
        line2_points = line2.get_equally_split_points(amount_of_lines)
        for start, end in zip(line1_points, line2_points):
                self.draw_line(geometry.Line(start, end), line_width, color)

    def draw_line(self, line, line_width=1, color=(0, 0, 0)):
        instructions = InstructionGroup()
        self.set_color(instructions, color)
        instructions.add(
            Line(points=[(line.start.x, line.start.y), (line.end.x, line.end.y)], width=line_width)
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

    linewidth = NumericProperty(1.0)
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

        drawer = Drawer(self.graph, self.canvas)
        drawer.draw_line(self.graph.lines["co2"], 2)
        drawer.draw_line(self.graph.lines["co"], 1.5)
        drawer.draw_line(self.graph.lines["o2"], 1.5)
        drawer.draw_line(self.graph.lines["coefficient"], 1.5)
        drawer.draw_line(self.graph.lines["bot"], 2)
        drawer.draw_line(self.graph.lines["diagonal"], 2)

        drawer.lines_between_2_lines(self.graph.lines["co2"], self.graph.lines["co"], 15, 1)
        drawer.lines_between_2_lines(self.graph.lines['o2'], self.graph.lines["diagonal"], 15, 1)
        drawer.lines_between_2_lines(self.graph.lines['diagonal'], self.graph.lines["bot"], 15, 1.5)
        drawer.lines_between_2_lines(self.graph.lines['co2'], self.graph.lines["diagonal"], 15, 1.5)


        drawer.lines_between_2_lines( self.graph.lines["coefficient"], 15, 1)


class TestLineApp(App):
    def build(self):
        return OstwaldTriangleVisualization()


if __name__ == '__main__':
    TestLineApp().run()