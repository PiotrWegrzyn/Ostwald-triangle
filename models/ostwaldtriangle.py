from math import cos, radians
from geometry.vector import Vector
from geometry.point import Point

from drawers.ostwald_triangle_graph_drawer import OstwaldTriangleGraphDrawer
from models.line_info import LineInfo


class OstwaldTriangle:

    def __init__(self, maxco2, maxo2, maxco):
        self.top = 670
        self.bot = 300
        self.height = self.top - self.bot
        self.left = 100
        self.right = 800
        self.width = self.right - self.left

        self.co_line_angle = 45
        self.coefficient_line_angle = 20
        coefficient_line_len = self.width * cos(radians(self.coefficient_line_angle))

        self.lines = {
            "co2": LineInfo(
                Vector(self.left, self.bot, self.left, self.top),
                points=int(maxco2)+2,
                scale=1,
                labels={"name": "Dwutlenek węgla %"}
            ),
            "co": LineInfo(
                Vector(Point(self.right, self.bot), 180 + self.co_line_angle, self.height),
                points=int(maxco/2),
                scale=2,
                labels={"name": "Tlenek węgla %"}
            ), #todo
            "o2": LineInfo(
                Vector(self.left, self.top, self.right, self.top),
                points=int(maxo2/2)+1,
                scale=2,
                labels={"name": "Tlen %"}
            ),
            "coefficient": LineInfo(
                Vector(Point(self.right, self.bot), 180+self.coefficient_line_angle, coefficient_line_len),
                scale=0.2,
                labels={"name": "Współczynnik alfa?"} #todo coeff latin smbol
            ),
            "bot": LineInfo(Vector(self.left, self.bot, self.right, self.bot)),
            "diagonal": LineInfo(Vector(self.left, self.top, self.right, self.bot))
        }

    def draw(self, canvas):
        OstwaldTriangleGraphDrawer(canvas, self).draw()
