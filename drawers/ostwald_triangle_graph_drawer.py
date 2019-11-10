from math import sin, radians

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse

from drawers.drawer import Drawer
from geometry import Vector
from geometry.series import Series
from gui.colors import COLORS
from models.line_info import LineInfo


class OstwaldTriangleGraphDrawer(Drawer):
    def __init__(self, canvas, triangle):
        super().__init__(canvas)
        self.triangle = triangle

    def draw(self, triangle=None):
        if triangle:
            self.triangle = triangle
        self.draw_graph_base()
        self.draw_lines_and_scales()
        self.annotate_line_names()
        self.add_title()
        self.draw_results()

    def draw_graph_base(self):
        self.draw_line(self.triangle.lines["co2"].line, 2)
        self.draw_line(self.triangle.lines["co"].line, 1.5)
        self.draw_line(self.triangle.lines["o2"].line, 1.5)
        self.draw_line(self.triangle.lines["coefficient"].line, 1.5)
        self.draw_line(self.triangle.lines["bot"].line, 2)
        self.draw_line(self.triangle.lines["diagonal"].line, 2)

    def annotate_line_names(self):
        self.annotate_line(
            self.triangle.lines["o2"].labels["name"],
            self.triangle.lines["o2"].line,
            offset_y=24,
            scale=1.3
        )
        self.annotate_line(
            self.triangle.lines["co2"].labels["name"],
            self.triangle.lines["co2"].line,
            offset_y=40,
            scale=1.3,
            angle=self.triangle.lines["co2"].line.angle
        )
        self.annotate_line(
            self.triangle.lines["co"].labels["name"],
            self.triangle.lines["co"].line,
            offset_y=-32,
            scale=1.2,
            angle=self.triangle.lines["co"].line.reversed().angle
        )
        self.annotate_line(
            self.triangle.lines["coefficient"].labels["name"],
            self.triangle.lines["coefficient"].line,
            offset_y=-32,
            scale=1.2,
            angle=self.triangle.lines["coefficient"].line.reversed().angle
        )

    def draw_lines_and_scales(self):
        self.draw_lines_and_annotate(
            self.triangle.lines['co2'],
            self.triangle.lines["diagonal"].line.reversed(),
            offset_x=-24,
            line_width=1.5,
            scale=1
        )

        self.lines_between_2_lines(
            self.triangle.lines['diagonal'].line,
            self.triangle.lines["bot"].line,
            self.triangle.lines['o2'].points,
            line_width=1.5
        )

        self.draw_lines_and_annotate(
            self.triangle.lines['o2'],
            self.triangle.lines["diagonal"].line,
            offset_y=8,
        )

        self.draw_lines_and_annotate(
            self.triangle.lines["co"],
            self.triangle.lines["co2"].line.reversed(),
            offset_y=-8,
            angle=self.triangle.lines["co"].line.reversed().angle,
            scale=0.8
        )

        self.coefficient_lines_and_annotations()

    def coefficient_lines_and_annotations(self):
        altitude_drop_ratio = self.coeff_line_altitude_drop_ratio()
        line1_series, line2_series = self.split_coeff_line_series(
            self.triangle.lines['coefficient'].series,
            altitude_drop_ratio
        )
        self.coefficient_line_split_by_altitude_drop = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[altitude_drop_ratio, 1 - altitude_drop_ratio]
        )

        self.draw_lines_and_annotate(
            LineInfo(self.coefficient_line_split_by_altitude_drop[0], series=line1_series),
            self.triangle.lines['diagonal'].line.reversed(),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            scale=0.8
        )

        self.draw_lines_and_annotate(
            LineInfo(self.coefficient_line_split_by_altitude_drop[1], series=line2_series),
            self.triangle.lines["co2"].line.reversed(),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            scale=0.8
        )

    def coeff_line_altitude_drop_ratio(self):
        angle_between = self.triangle.co2_diagonal_angle - self.triangle.coefficient_line_angle
        distance_from_start = sin(radians(angle_between)) * self.triangle.lines['diagonal'].line.length
        return distance_from_start / self.triangle.lines['coefficient'].line.length

    def split_coeff_line_series(self, main_series, altitude_drop_ratio):
        line1_series = Series(main_series.start, 1, main_series.scale)
        line2_series = Series(1, 1 / altitude_drop_ratio, main_series.scale)
        return line1_series, line2_series

    def draw_point(self, point, color=(0, 0, 0)):
        with self.canvas:
            self.create_color(color)
            Ellipse(pos=(point.x-5, point.y-5), size=(10,10))
            Color(0, 0, 0, 1)

    def draw_results(self):
        self.draw_line(self.triangle.lines["P-co"].line, 2, color=COLORS["red"])
        self.draw_line(self.triangle.lines["P-o2"].line, 1.5, color=COLORS["red"])
        self.draw_line(self.triangle.lines["P-co2"].line, 1.5, color=COLORS["red"])
        self.draw_point(self.triangle.P, color=COLORS["red"])
        self.draw_point(self.triangle.C, color=COLORS["blue"])
        self.add_annotation(
            self.calculate_result_phi(),
            self.triangle.lines["P-co"].line.end,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            offset_y=-8,
            color=COLORS["red"]
        )

    def calculate_result_phi(self):
        line_from_res_to_co_start = Vector(self.triangle.lines["P-co"].line.end, self.triangle.lines["co"].line.start)
        res = line_from_res_to_co_start.length/self.coefficient_line_split_by_altitude_drop[0].length
        return round(res, 2)

    def add_title(self):
        self.annotate_line(
            self.triangle.title,
            self.triangle.lines['o2'].line,
            offset_y=48,
            scale=1.8
        )


