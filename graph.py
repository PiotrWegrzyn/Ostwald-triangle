from geometry.line import Line
from geometry.point import Point


class Graph:

    def __init__(self):
        self.top = 650
        self.bot = 350
        self.height = self.top - self.bot
        self.left = 100
        self.right = 500
        self.width = self.right - self.left
        self.line_co2 = Line(self.left, self.top, self.left, self.bot)
        self.line_co = Line(Point(self.right, self.bot), 360-(90+45), self.height)
        self.line_o2 = Line(self.left, self.bot, self.right, self.bot)
