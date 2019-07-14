from kivy.graphics.context_instructions import Color, Rotate
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line

from geometry import Point, Vector
from models.annotation import Annotation


class Drawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def lines_between_2_lines(self, line1, line2, amount_of_lines, line_width, color=(0, 0, 0), w1=None, w2=None):
        line1_points = line1.get_split_points(amount_of_lines, w1)
        line2_points = line2.get_split_points(amount_of_lines, w2)
        for start, end in zip(line1_points, line2_points):
            self.draw_line(Vector(start, end), line_width, color)

    def draw_line(self, line, line_width=1, color=(0, 0, 0)):
        instructions = InstructionGroup()
        self.set_color(instructions, color)
        instructions.add(
            Line(points=[(line.start.x, line.start.y), (line.end.x, line.end.y)], width=line_width)
        )
        self.canvas.add(instructions)

    def annotate_line(self, text, line, **kwargs):
        placement = kwargs.get("placement", 0.5)
        offset_x = kwargs.get("offset_x", 0)
        offset_y = kwargs.get("offset_y", 0)
        self.add_annotation(text, (line.start.x + line.dx*placement + offset_x, line.start.y + line.dy*placement + offset_y), **kwargs)

    def annotate_line_range(self, line_info, start, stop, **kwargs):
        scale = line_info.scale
        amount = int((stop-start)/scale)+1
        values = [start + scale * i for i in range(amount)]
        placements = [x/(amount-1) for x in range(amount)]
        self.annotate_line_manually(line_info.line, values, placements, format="float", **kwargs)

    def annotate_line_manually(self, line, values, placements, **kwargs):
        if len(values) is not len(placements):
            raise ValueError("Values and placements need to have the same amount of items")
        for placement in placements:
            if placement > 1:
                raise ValueError("Placement value cannot be bigger than 1.")
        for value, placement in zip(values, placements):
            kwargs['placement'] = placement
            self.annotate_line(value, line, **kwargs)

    def add_annotation(self, text, position, **kwargs):
        angle = kwargs.get("angle", 0)
        self.canvas.add(Rotate(angle=angle))
        position = self.rotate_position(position, angle)
        self.canvas.add(Annotation(text, position, **kwargs))
        self.canvas.add(Rotate(angle=-angle))

    def rotate_position(self, position, angle):
        rotated_point = Point.rotate(position, -angle)
        return tuple(rotated_point)

    @staticmethod
    def create_color(rgb):
        return Color(rgb[0], rgb[1], rgb[2])

    def set_color(self, instructions, color):
        color = self.create_color(color)
        instructions.add(color)



