from drawers.drawer import Drawer
from math import sin, radians, degrees, acos


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
            self.triangle.lines['co'].points,
            line_width=1
        )
        self.draw_coefficient_lines()

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
        wages = self.split_remaining_coeff_line(coeff_line_split[1])
        self.lines_between_2_lines(
            coeff_line_split[1],
            self.triangle.lines['co2'].line.reversed(),
            amount_of_lines=len(wages),
            line_width=1,
            w1=wages,
            w2=wages
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
