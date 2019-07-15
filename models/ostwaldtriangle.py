from math import cos, radians, atan, degrees

from drawers.ostwald_triangle_graph_drawer import OstwaldTriangleGraphDrawer
from geometry.point import Point
from geometry.series import Series
from geometry.vector import Vector
from models.line_info import LineInfo


class OstwaldTriangle:

    def __init__(self, maxco2, maxo2, maxco):
        self.top = 720
        self.bot = 350
        self.height = self.top - self.bot
        self.left = 100
        self.right = 800
        self.width = self.right - self.left

        self.co_line_angle = 90 - degrees(atan(self.height/self.width))
        self.coefficient_line_angle = 15
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
                series=Series(0, maxco, 2),
                labels={"name": "Tlenek węgla %"}
            ), #todo
            "coefficient": LineInfo(
                Vector(Point(self.right, self.bot), 180+self.coefficient_line_angle, coefficient_line_len),
                series=Series(0, 1.6, 0.1),
                labels={"name": "Współczynnik alfa?"} #todo coeff latin smbol
            ),
            "bot": LineInfo(Vector(self.left, self.bot, self.right, self.bot)),
            "diagonal": LineInfo(Vector(self.left, self.top, self.right, self.bot))
        }

    def draw(self, canvas):
        OstwaldTriangleGraphDrawer(canvas, self).draw()
