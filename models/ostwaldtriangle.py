from math import cos, radians, atan, degrees

from kivy.core.window import Window

from drawers.ostwald_triangle_graph_drawer import OstwaldTriangleGraphDrawer
from geometry.point import Point
from geometry.series import Series
from geometry.vector import Vector
from models.line_info import LineInfo


class OstwaldTriangle:
    top = bot = left = right = height = width = 0

    def __init__(self, maxco2, maxo2, maxco, pointC):
        self.maxco2 = maxco2
        self.maxco = maxco
        self.maxo2 = maxo2

        self.set_width(margin_left=17, triangle_width=50)
        self.set_height(margin_top=5, triangle_width=50)

        self.co2_diagonal_angle = degrees(atan(self.width/self.height))
        self.co_line_angle = self.co2_diagonal_angle
        self.bot_diagonal_angle = 90 - self.co2_diagonal_angle

        self.coefficient_line_angle = self.calculate_coeff_line_angle(pointC, maxo2)
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
                Vector(Point(self.right, self.bot), 180 + self.co_line_angle, self.width*cos(radians(self.co2_diagonal_angle))),
                series=Series(0, maxco, 3),
                labels={"name": "Tlenek węgla %"}
            ),
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

    def calculate_coeff_line_angle(self, pointC, maxo2):
        pointCscale = pointC / maxo2
        A = Point(self.left,self.top)
        B = Point(self.right,self.bot)
        C = Point(self.left+(pointCscale*(self.right-self.left)),self.bot)
        AC = Vector(A,C)
        AB = Vector(A,B)
        alpha = Vector.angle_between(AB, AC)
        return 90 - alpha - self.bot_diagonal_angle

    def set_height(self, margin_top, triangle_width):
        self.top = Window.size[1] * (100-margin_top)/100
        self.bot = Window.size[1] * (100-margin_top)/100 - Window.size[0]*((self.maxco2*triangle_width/self.maxo2)/100)
        self.height = self.top - self.bot

    def set_width(self, margin_left, triangle_width):
        self.left = Window.size[0] * margin_left/100
        self.right = Window.size[0] * (margin_left + triangle_width)/100
        self.width = self.right - self.left



