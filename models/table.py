from kivy.core.window import Window

from drawers.table_drawer import TableDrawer
from geometry import Vector
from models.line_info import LineInfo


class Table:
    def __init__(self, x, y, data):
        self.top = 650
        self.bot = 300
        self.left = 850
        self.right = 950

        self.data = data

        height_p = 45
        self.top = Window.size[1] * y/100
        self.bot = Window.size[1] * (y-height_p)/100
        self.height = self.top - self.bot
        width_p = 10
        self.left = Window.size[0] * x/100
        self.right = Window.size[0] * (x + width_p)/100
        self.width = self.right - self.left

        self.columns = 2
        self.rows = 16

        self.lines = {
            "top": LineInfo(Vector(self.left, self.top, self.right, self.top)),
            "bot": LineInfo(Vector(self.left, self.bot, self.right, self.bot)),
            "right": LineInfo(Vector(self.right, self.top, self.right, self.bot)),
            "left": LineInfo(Vector(self.left, self.top, self.left, self.bot))
        }

    def draw(self, canvas):
        TableDrawer(canvas, self).draw()
