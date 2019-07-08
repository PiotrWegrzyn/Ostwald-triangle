from math import sin, radians, degrees, acos

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line
from kivy.uix.floatlayout import FloatLayout

import geometry
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
        self.draw_coefficient_lines()

    def calculate_coefficient_center(self):
        cosalfa = self.graph.lines['co2'].line.length / self.graph.lines['diagonal'].line.length
        alfa = degrees(acos(cosalfa))
        distance_from_start = sin(radians(alfa-self.graph.coefficient_line_angle)) * self.graph.lines['diagonal'].line.length
        return distance_from_start / self.graph.lines['coefficient'].line.length

    def draw_coefficient_lines(self):
        scale = 0.1
        amount_of_points = int(scale**-1)+1
        coeff_line_split = self.graph.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[
                self.calculate_coefficient_center(),
                1 - self.calculate_coefficient_center()
            ]
        )
        self.drawer.lines_between_2_lines(
            coeff_line_split[0].reversed(),
            self.graph.lines['diagonal'].line,
            amount_of_vectors=amount_of_points,
            vector_width=1,
        )
        coef_len = int(self.graph.lines['coefficient'].line.length)
        remaining_coef_len = int(coeff_line_split[1].length)
        step = int(scale * coef_len * self.calculate_coefficient_center())
        wages = [distance / remaining_coef_len for distance in range(0,remaining_coef_len, step)]
        self.drawer.lines_between_2_lines(
            coeff_line_split[1],
            self.graph.lines['co2'].line.reversed(),
            amount_of_vectors=len(wages),
            vector_width=1,
            w1=wages,
            w2=wages
        )


class OstwaldTriangle(App):
    def build(self):
        return OstwaldTriangleVisualization()


if __name__ == '__main__':
    OstwaldTriangle().run()