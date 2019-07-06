from geometry.line import Line


class Graph:

    def __init__(self):
        self.top = 600
        self.bot = 200
        self.height = self.top - self.bot
        self.left = 100
        self.right = 500
        self.width = self.right - self.left
        self.line_co2 = Line(self.left, self.bot, self.left, self.top)
