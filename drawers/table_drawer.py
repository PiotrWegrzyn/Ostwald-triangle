from drawers.drawer import Drawer


class TableDrawer(Drawer):
    def __init__(self, canvas, table):
        self.table = table
        super().__init__(canvas)

    def draw(self, table=None):
        if table:
            self.table = table
        self.draw_line(self.table.lines["top"].line, 2)
        self.draw_line(self.table.lines["bot"].line, 2)
        self.draw_line(self.table.lines["left"].line, 2)
        self.draw_line(self.table.lines["right"].line, 2)
        self.lines_between_2_lines(self.table.lines["right"].line, self.table.lines["left"].line, 16, 1)
        self.lines_between_2_lines(self.table.lines["top"].line, self.table.lines["bot"].line, 3, 1)
