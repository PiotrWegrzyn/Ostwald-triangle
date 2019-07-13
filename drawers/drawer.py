from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Rectangle
import geometry
from models.annotation import Annotation


class Drawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def lines_between_2_lines(self, line1, line2, amount_of_lines, line_width, color=(0, 0, 0), w1=None, w2=None):
        line1_points = line1.get_split_points(amount_of_lines, w1)
        line2_points = line2.get_split_points(amount_of_lines, w2)
        for start, end in zip(line1_points, line2_points):
            self.draw_line(geometry.Vector(start, end), line_width, color)

    def draw_line(self, line, line_width=1, color=(0, 0, 0)):
        instructions = InstructionGroup()
        self.set_color(instructions, color)
        instructions.add(
            Line(points=[(line.start.x, line.start.y), (line.end.x, line.end.y)], width=line_width)
        )
        self.canvas.add(instructions)

    def annotate_line(self, text, line):
        self.add_annotation(text, (line.get_center().x, line.get_center().y))

    def annotate_line_range(self, line_info, start, stop):
        line = line_info.line
        scale = line_info.scale
        amount = int((stop-start)/scale)
        dx = line.dx/amount
        dy = line.dy/amount
        for i in range(amount+1):
            self.add_annotation(self.annotation_format(start + scale * i), (line.start.x + dx * i, line.start.y + dy * i))

    def add_annotation(self, text, position):
        self.canvas.add(Annotation(text, position))

    def annotation_format(self, annotation):
        if isinstance(annotation, float):
            if annotation % 1 == 0:
                return int(annotation)
        return annotation

    @staticmethod
    def create_color(rgb):
        return Color(rgb[0], rgb[1], rgb[2])

    def set_color(self, instructions, color):
        color = self.create_color(color)
        instructions.add(color)

