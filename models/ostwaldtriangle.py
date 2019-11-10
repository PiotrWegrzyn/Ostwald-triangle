from math import cos, radians, atan, degrees

from kivy.core.window import Window

from drawers.ostwald_triangle_graph_drawer import OstwaldTriangleGraphDrawer
from geometry.point import Point
from geometry.series import Series
from geometry.vector import Vector
from models.line_info import LineInfo


class OstwaldTriangle:
    top = bot = left = right = height = width = 0

    def __init__(self, calculations):
        self.title = "The Ostwald Triangle"
        self.maxco2 = calculations.max_co2
        self.maxco = calculations.max_co
        self.maxo2 = calculations.max_o2

        self.set_width(margin_left=10, triangle_width=50)
        self.set_height(margin_top=10, triangle_width=50)
        self.A = Point(self.left, self.top)
        self.B = Point(self.right, self.bot)
        self.C = self.get_position_from_scale(calculations.C.o2, calculations.C.co2)
        self.P = self.get_position_from_scale(calculations.P.o2, calculations.P.co2)
        self.Pco2 = self.get_position_from_scale(0, calculations.P.co2)
        self.Po2 = self.get_position_from_scale(calculations.P.o2, self.maxco2)
        self.co2_diagonal_angle = degrees(atan(self.width/self.height))
        self.co_line_angle = self.co2_diagonal_angle
        self.bot_diagonal_angle = 90 - self.co2_diagonal_angle

        self.coefficient_line_angle = self.calculate_coeff_line_angle()
        self.lines = {"o2": LineInfo(
            Vector(self.left, self.top, self.right, self.top),
            points=self.maxo2 + 1,
            labels={"name": "Oxygen %"},
            series=Series(0, self.maxo2, 2),
        ), "co2": LineInfo(
            Vector(self.left, self.bot, self.left, self.top),
            series=Series(0, self.maxco2, 2),
            labels={"name": "Carbon dioxide %"}
        ), "co": LineInfo(
            Vector(Point(self.right, self.bot), 180 + self.co_line_angle,
                   self.width * cos(radians(self.co2_diagonal_angle))),
            series=Series(0, self.maxco, 5),
            labels={"name": "Carbon monoxide %"}
        ), "coefficient": LineInfo(
            self.create_coefficient_line(),
            series=Series(0, 1.6, 0.2),
            labels={"name": "Phi coefficient"}  # todo coeff latin smbol
        ), "bot": LineInfo(
            Vector(self.left, self.bot, self.right, self.bot)
        ), "diagonal": LineInfo(
            Vector(self.left, self.top, self.right, self.bot)
        ), "P-co": LineInfo(
            self.create_p_co_line()
        ), "P-o2": LineInfo(
            self.create_p_o2_line()
        ), "P-co2": LineInfo(
            self.create_p_co2_line()
        )
        }

    def draw(self, canvas):
        self.drawer = OstwaldTriangleGraphDrawer(canvas, self)
        self.drawer.draw()

    def calculate_coeff_line_angle(self):
        AC = Vector(self.A, self.C)
        AB = Vector(self.A, self.B)
        alpha = Vector.angle_between(AB, AC)
        return 90 - alpha - self.bot_diagonal_angle

    def set_height(self, margin_top, triangle_width):
        self.top = Window.size[1] * (100-margin_top)/100
        self.bot = Window.size[1] * (100-margin_top)/100 - Window.size[0]*((self.maxco2*triangle_width/self.maxo2)/100) + (Window.size[1] * 0.2)
        self.height = self.top - self.bot

    def set_width(self, margin_left, triangle_width):
        self.left = Window.size[0] * margin_left/100
        self.right = Window.size[0] * (margin_left + triangle_width)/100
        self.width = self.right - self.left

    def create_coefficient_line(self):
        coefficient_line_len = self.width * cos(radians(self.coefficient_line_angle))
        return Vector(Point(self.right, self.bot), 180 + self.coefficient_line_angle, coefficient_line_len)

    def create_p_co_line(self):
        line_from_p_with_angle = Vector(self.P, 180 + 90 + self.coefficient_line_angle, self.height*2+self.width)
        coefficient_line = self.create_coefficient_line()
        point_of_intersection = Vector.intersection(line_from_p_with_angle, coefficient_line)
        return Vector(self.P, point_of_intersection)

    def create_p_o2_line(self):
        return Vector(self.Pco2, self.P)

    def create_p_co2_line(self):
        return Vector(self.Po2, self.P)

    def get_position_from_scale(self, o2, co2):
        return Point(
            self.left + ((o2 / self.maxo2) * (self.right - self.left)),
            self.bot + ((co2 / self.maxco2) * (self.top - self.bot))
        )

    def get_result_phi(self):
        return self.drawer.calculate_result_phi()





