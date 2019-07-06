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
        self.lines = {
            "co2": Line(self.left, self.top, self.left, self.bot),
            "co": Line(Point(self.right, self.bot), 360 - (90 + 45), self.height),
            "o2": Line(self.left, self.top, self.right, self.top),
            "coefficient": Line(Point(self.right, self.bot), 360 - (90 + 60), self.height),
            "bot": Line(self.left, self.bot, self.right, self.bot),
            "diagonal": Line(self.left, self.top, self.right, self.bot)
        }

