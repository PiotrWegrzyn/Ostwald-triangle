from math import sin, radians, degrees, acos

from drawers.drawer import Drawer
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
            line_width=1.5
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
        self.annotate_line_range(self.triangle.lines["o2"], 0, self.triangle.lines["o2"].points-1, offset_y=8)
        self.annotate_line_range(self.triangle.lines["co2"], 0, self.triangle.lines["co2"].points-1, offset_x=-16)
        self.annotate_line_range(
            self.triangle.lines["co"],
            0,
            self.triangle.lines["co"].points,
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

    def draw_coefficient_lines(self):
        altitude_drop_ratio = self.coeff_line_altitude_drop_ratio()
        scale = self.triangle.lines['coefficient'].scale
        amount_of_points = int(scale ** -1) + 1
        coeff_line_split = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[
                altitude_drop_ratio,
                1 - altitude_drop_ratio
            ]
        )
        self.lines_between_2_lines(
            coeff_line_split[0].reversed(),
            self.triangle.lines['diagonal'].line,
            amount_of_lines=amount_of_points,
            line_width=1,
        )
        self.annotate_line_range(
            LineInfo(coeff_line_split[0], scale=scale),
            0,
            scale*(amount_of_points-1),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle
        )

        wages = self.split_remaining_coeff_line(coeff_line_split[1])
        self.lines_between_2_lines(
            coeff_line_split[1],
            self.triangle.lines['co2'].line.reversed(),
            amount_of_lines=len(wages),
            line_width=1,
            w1=wages,
            w2=wages
        )
        remaining_part_split = coeff_line_split[1].split(
            number_of_lines=2,
            proportions=[
                wages[-1],
                1 - wages[-1]
            ]
        )
        self.annotate_line_range(
            LineInfo(remaining_part_split[0], scale=scale),
            scale*(amount_of_points-1),
            scale*(amount_of_points-1+len(wages)-1),
            offset_y=-8,
            angle=self.triangle.lines["coefficient"].line.reversed().angle
        )

    def split_remaining_coeff_line(self, remaining_part):
        coef_len = self.triangle.lines['coefficient'].line.length
        step = int(self.triangle.lines['coefficient'].scale * coef_len * self.coeff_line_altitude_drop_ratio())
        return [distance / remaining_part.length for distance in range(0, int(remaining_part.length), step)]

    def coeff_line_altitude_drop_ratio(self):
        cos_alpha = self.triangle.lines['co2'].line.length / self.triangle.lines['diagonal'].line.length
        alpha = degrees(acos(cos_alpha))
        distance_from_start = sin(radians(alpha - self.triangle.coefficient_line_angle)) * self.triangle.lines[
            'diagonal'].line.length
        return distance_from_start / self.triangle.lines['coefficient'].line.length

