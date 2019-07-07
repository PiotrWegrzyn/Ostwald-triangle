from math import sin, cos, radians

from geometry.vector import Vector
from geometry.point import Point


class LineInfo:
    def __init__(self, line, number_of_lines=0, labels=None):
        self.line = line
        self.number_of_lines = number_of_lines
        self.labels = labels


class Graph:

    def __init__(self, maxco2, maxo2, maxco):
        self.top = 650
        self.bot = 350
        self.height = self.top - self.bot
        self.left = 100
        self.right = 800
        self.width = self.right - self.left

        self.co_line_angle = 60
        self.coefficient_line_angle = 20
        coefficient_line_len = self.width * cos(radians(self.coefficient_line_angle))

        self.lines = {
            "co2": LineInfo(Vector(self.left, self.bot, self.left, self.top), int(maxco2)),
            "co": LineInfo(Vector(Point(self.right, self.bot), 180 + self.co_line_angle, self.height), int(maxco)),
            "o2": LineInfo(Vector(self.left, self.top, self.right, self.top), int(maxo2)),
            "coefficient": LineInfo(Vector(Point(self.right, self.bot), 180+self.coefficient_line_angle, coefficient_line_len)),
            "bot": LineInfo(Vector(self.left, self.bot, self.right, self.bot)),
            "diagonal": LineInfo(Vector(self.left, self.top, self.right, self.bot))
        }

