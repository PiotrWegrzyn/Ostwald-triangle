from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line
import geometry


class Drawer:
    def __init__(self, canvas):
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