from math import sin, radians, degrees, acos

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
        self.lines_between_2_lines(
            self.triangle.lines['co2'].line,
            self.triangle.lines["diagonal"].line.reversed(),
            self.triangle.lines['co2'].points,
            line_width=1.5,
            w1=self.triangle.lines['co2'].series.get_point_wages(),
            w2=self.triangle.lines['co2'].series.get_point_wages()
        )
        self.lines_between_2_lines(
            self.triangle.lines['diagonal'].line,
            self.triangle.lines["bot"].line,
            self.triangle.lines['o2'].points,
            line_width=1.5
        )
        self.lines_between_2_lines(
            self.triangle.lines['o2'].line,
            self.triangle.lines["diagonal"].line,
            self.triangle.lines['o2'].points,
            line_width=1
        )
        self.lines_between_2_lines(
            self.triangle.lines["co2"].line,
            self.triangle.lines["co"].line.reversed(),
            self.triangle.lines['co'].points+1,
            line_width=1
        )
        self.draw_coefficient_lines()

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
        self.annotate_line_with_series(self.triangle.lines["o2"], offset_y=8)
        self.annotate_line_with_series(self.triangle.lines["co2"], offset_x=-20)
        self.annotate_line_with_series(
            self.triangle.lines["co"],
            offset_y=-8,
            angle=self.triangle.lines["co"].line.reversed().angle
        )

    def draw_graph_base(self):
        self.draw_line(self.triangle.lines["co2"].line, 2)
        self.draw_line(self.triangle.lines["co"].line, 1.5)
        self.draw_line(self.triangle.lines["o2"].line, 1.5)
        self.draw_line(self.triangle.lines["coefficient"].line, 1.5)
        self.draw_line(self.triangle.lines["bot"].line, 2)
        self.draw_line(self.triangle.lines["diagonal"].line, 2)

    def draw_coefficient_lines2(self):
        altitude_drop_ratio = self.coeff_line_altitude_drop_ratio()
        coeff_line_split = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[
                altitude_drop_ratio,
                1 - altitude_drop_ratio
            ]
        )
        line1 = LineInfo(
            coeff_line_split[0].reversed(),

        )

    def draw_coefficient_lines(self):
        altitude_drop_ratio = self.coeff_line_altitude_drop_ratio()
        main_series = self.triangle.lines['coefficient'].series
        line1_series = Series(main_series.start, 1, main_series.scale)
        line2_series = Series(1, 1/altitude_drop_ratio, main_series.scale)
        coeff_line_split = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[altitude_drop_ratio, 1 - altitude_drop_ratio]
        )
        self.lines_between_2_lines(
            coeff_line_split[0].reversed(),
            self.triangle.lines['diagonal'].line,
            amount_of_lines=line1_series.points,
            line_width=1,
        )
        self.annotate_line_with_series(
            LineInfo(coeff_line_split[0], series=line1_series),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            scale=0.7
        )

        remaining_line = LineInfo(coeff_line_split[1], series=line2_series)

        self.lines_between_2_lines(
            remaining_line.line,
            self.triangle.lines['co2'].line.reversed(),
            amount_of_lines=remaining_line.series.points,
            line_width=1,
            w1=remaining_line.series.get_point_wages(),
            w2=remaining_line.series.get_point_wages()
        )
        self.annotate_line_with_series(
            LineInfo(coeff_line_split[1], series=line2_series),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle,
            scale=0.7
        )

    def coeff_line_altitude_drop_ratio(self):
        cos_alpha = self.triangle.lines['co2'].line.length / self.triangle.lines['diagonal'].line.length
        alpha = degrees(acos(cos_alpha))
        distance_from_start = sin(radians(alpha - self.triangle.coefficient_line_angle)) * self.triangle.lines[
            'diagonal'].line.length
        return distance_from_start / self.triangle.lines['coefficient'].line.length

