from drawer import Drawer
from math import sin, radians, degrees, acos


class OstwaldTriangleGraphDrawer(Drawer):
    def draw(self, triangle):
        self.draw_line(triangle.lines["co2"].line, 2)
        self.draw_line(triangle.lines["co"].line, 1.5)
        self.draw_line(triangle.lines["o2"].line, 1.5)
        self.draw_line(triangle.lines["coefficient"].line, 1.5)
        self.draw_line(triangle.lines["bot"].line, 2)
        self.draw_line(triangle.lines["diagonal"].line, 2)

        self.lines_between_2_lines(
            triangle.lines['co2'].line,
            triangle.lines["diagonal"].line.reversed(),
            triangle.lines['co2'].number_of_lines,
            vector_width=1.5
        )
        self.lines_between_2_lines(
            triangle.lines['diagonal'].line,
            triangle.lines["bot"].line,
            triangle.lines['o2'].number_of_lines,
            vector_width=1.5
        )
        self.lines_between_2_lines(
            triangle.lines['o2'].line,
            triangle.lines["diagonal"].line,
            triangle.lines['o2'].number_of_lines,
            vector_width=1
        )
        self.lines_between_2_lines(
            triangle.lines["co2"].line,
            triangle.lines["co"].line.reversed(),
            triangle.lines['co'].number_of_lines,
            vector_width=1
        )
        self.draw_coefficient_lines(triangle)

    def draw_coefficient_lines(self, triangle):
        coeff_center = self.calculate_coefficient_center(triangle)
        scale = 0.1
        amount_of_points = int(scale ** -1) + 1
        coeff_line_split = triangle.lines['coefficient'].line.split(
            number_of_lines=2,
            proportions=[
                coeff_center,
                1 - coeff_center
            ]
        )
        self.lines_between_2_lines(
            coeff_line_split[0].reversed(),
            triangle.lines['diagonal'].line,
            amount_of_vectors=amount_of_points,
            vector_width=1,
        )
        coef_len = int(triangle.lines['coefficient'].line.length)
        remaining_coef_len = int(coeff_line_split[1].length)
        step = int(scale * coef_len * coeff_center)
        wages = [distance / remaining_coef_len for distance in range(0, remaining_coef_len, step)]
        self.lines_between_2_lines(
            coeff_line_split[1],
            triangle.lines['co2'].line.reversed(),
            amount_of_vectors=len(wages),
            vector_width=1,
            w1=wages,
            w2=wages
        )

    def calculate_coefficient_center(self, triangle):
        cos_alpha = triangle.lines['co2'].line.length / triangle.lines['diagonal'].line.length
        alpha = degrees(acos(cos_alpha))
        distance_from_start = sin(radians(alpha - triangle.coefficient_line_angle)) * triangle.lines[
            'diagonal'].line.length
        return distance_from_start / triangle.lines['coefficient'].line.length
