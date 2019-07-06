from math import cos, sin, radians

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
    BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

from geometry.point import Point
from geometry.line import Line as GeoLine
from graph import Graph

kivy.require('1.9.0')

Builder.load_string('''
<LinePlayground>:

    canvas:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            points: self.axis_points
            width: 2
            
    GridLayout:
        cols: 2
        size_hint: 1, None
        height: 44 * 5
   

''')


class Drawer:
    def __init__(self, graph):
        self.graph = graph

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

    def lines_between_2_lines(self, canvas, line1, line2, amount_of_lines, line_width):
        instructions = InstructionGroup()
        line1_points = line1.get_equally_split_points(amount_of_lines)
        line2_points = line2.get_equally_split_points(amount_of_lines)
        for start, end in zip(line1_points, line2_points):
            instructions.add(
                Line(points=[(start.x, start.y), (end.x, end.y)], width=line_width)
            )
        canvas.add(instructions)


class LinePlayground(FloatLayout):

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
        self.axis_points.append((self.graph.left, self.graph.top))
        self.axis_points.append((self.graph.left, self.graph.bot))
        self.axis_points.append((self.graph.right, self.graph.bot))

        drawer = Drawer(self.graph)

        l2 = GeoLine(self.graph.left+50, self.graph.bot-100, self.graph.right, self.graph.bot)
        drawer.lines_between_2_lines(self.canvas, self.graph.line_co2, l2, 15, 1.5)


class TestLineApp(App):
    def build(self):
        return LinePlayground()


if __name__ == '__main__':
    TestLineApp().run()