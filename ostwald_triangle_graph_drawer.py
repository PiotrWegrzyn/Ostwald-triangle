from drawer import Drawer
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
            self.triangle.lines['co2'].number_of_lines,
            vector_width=1.5
        )
        self.lines_between_2_lines(
            self.triangle.lines['diagonal'].line,
            self.triangle.lines["bot"].line,
            self.triangle.lines['o2'].number_of_lines,
            vector_width=1.5
        )
        self.lines_between_2_lines(
            self.triangle.lines['o2'].line,
            self.triangle.lines["diagonal"].line,
            self.triangle.lines['o2'].number_of_lines,
            vector_width=1
        )
        self.lines_between_2_lines(
            self.triangle.lines["co2"].line,
            self.triangle.lines["co"].line.reversed(),
            self.triangle.lines['co'].number_of_lines,
            vector_width=1
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
        coeff_center = self.calculate_coefficient_center()
        scale = self.triangle.lines['coefficient'].scale
        amount_of_points = int(scale ** -1) + 1
        coeff_line_split = self.triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[
                coeff_center,
                1 - coeff_center
            ]
        )
        self.lines_between_2_lines(
            coeff_line_split[0].reversed(),
            self.triangle.lines['diagonal'].line,
            amount_of_vectors=amount_of_points,
            vector_width=1,
        )
        wages = self.split_remaining_coeff_line(coeff_line_split[1])
        self.lines_between_2_lines(
            coeff_line_split[1],
            self.triangle.lines['co2'].line.reversed(),
            amount_of_vectors=len(wages),
            vector_width=1,
            w1=wages,
            w2=wages
        )

    def split_remaining_coeff_line(self, remaining_part):
        coef_len = int(self.triangle.lines['coefficient'].line.length)
        remaining_coef_len = int(remaining_part.length)
        step = int(self.triangle.lines['coefficient'].scale * coef_len * self.calculate_coefficient_center())
        return [distance / remaining_coef_len for distance in range(0, remaining_coef_len, step)]

    def calculate_coefficient_center(self):
        cos_alpha = self.triangle.lines['co2'].line.length / self.triangle.lines['diagonal'].line.length
        alpha = degrees(acos(cos_alpha))
        distance_from_start = sin(radians(alpha - self.triangle.coefficient_line_angle)) * self.triangle.lines[
            'diagonal'].line.length
        return distance_from_start / self.triangle.lines['coefficient'].line.length
