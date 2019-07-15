from math import sin, radians

from drawers.drawer import Drawer
from geometry.series import Series
from models.line_info import LineInfo


class OstwaldTriangleGraphDrawer(Drawer):
    def __init__(self, canvas, triangle):
        super().__init__(canvas)
        self.triangle = triangle

    def draw(self, triangle=None):
        if triangle:
            self.triangle = triangle
        self.draw_graph_base()
        self.draw_lines_and_annotations()

        self.annotate_line_names()

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
            offset_y=22,
            scale=1.5
        )
        self.annotate_line(
            self.triangle.lines["co2"].labels["name"],
            self.triangle.lines["co2"].line,
            offset_y=48,
            scale=1.5,
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

    def draw_lines_and_annotations(self):
        self.draw_lines_and_annotate(
            self.triangle.lines['co2'],
            self.triangle.lines["diagonal"].line.reversed(),
            offset_x=-20,
            line_width=1.5
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
            angle=self.triangle.lines["co"].line.reversed().angle
        )

        self.coefficient_lines_and_annotations()

    def coefficient_lines_and_annotations(self):
        altitude_drop_ratio = self.coeff_line_altitude_drop_ratio()
        line1_series, line2_series = self.split_coeff_line_series(
            self.triangle.lines['coefficient'].series,
            altitude_drop_ratio
        )
        coeff_line_split = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[altitude_drop_ratio, 1 - altitude_drop_ratio]
        )

        self.draw_lines_and_annotate(
            LineInfo(coeff_line_split[0], series=line1_series),
            self.triangle.lines['diagonal'].line.reversed(),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            scale=0.8
        )

        self.draw_lines_and_annotate(
            LineInfo(coeff_line_split[1], series=line2_series),
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