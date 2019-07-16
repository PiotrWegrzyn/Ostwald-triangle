from math import cos, radians, atan, degrees

from kivy.core.window import Window

from drawers.ostwald_triangle_graph_drawer import OstwaldTriangleGraphDrawer
from geometry.point import Point
from geometry.series import Series
from geometry.vector import Vector
from models.line_info import LineInfo


class OstwaldTriangle:

    def __init__(self, maxco2, maxo2, maxco):
        self.top = Window.size[1] * 95/100
        self.bot = Window.size[1] * 48/100
        self.height = self.top - self.bot
        self.left = Window.size[0] * 5/100
        self.right = Window.size[0] * 85/100
        self.width = self.right - self.left

        self.co2_diagonal_angle = degrees(atan(self.width/self.height))
        self.co_line_angle = self.co2_diagonal_angle
        self.coefficient_line_angle = 20
        coefficient_line_len = self.width * cos(radians(self.coefficient_line_angle))

        self.lines = {
            "o2": LineInfo(
                Vector(self.left, self.top, self.right, self.top),
                points=maxo2 + 1,
                labels={"name": "Tlen %"},
                series=Series(0, maxo2, 2),
            ),
            "co2": LineInfo(
                Vector(self.left, self.bot, self.left, self.top),
                series=Series(0, maxco2, 2),
                labels={"name": "Dwutlenek węgla %"}
            ),
            "co": LineInfo(
                Vector(Point(self.right, self.bot), 180 + self.co_line_angle, self.height),
                series=Series(0, maxco, 3),
                labels={"name": "Tlenek węgla %"}
            ), #todo
            "coefficient": LineInfo(
                Vector(Point(self.right, self.bot), 180+self.coefficient_line_angle, coefficient_line_len),
                series=Series(0, 1.6, 0.1),
                labels={"name": "Współczynnik Phi"} #todo coeff latin smbol
            ),
            "bot": LineInfo(Vector(self.left, self.bot, self.right, self.bot)),
            "diagonal": LineInfo(Vector(self.left, self.top, self.right, self.bot))
        }

    def draw(self, canvas):
        OstwaldTriangleGraphDrawer(canvas, self).draw()
