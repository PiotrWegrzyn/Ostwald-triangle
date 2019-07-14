from drawers.drawer import Drawer
from geometry import Vector


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
        self.lines_between_2_lines(self.table.lines["right"].line, self.table.lines["left"].line, self.table.rows+1, 1)
        self.lines_between_2_lines(self.table.lines["top"].line, self.table.lines["bot"].line, self.table.columns+1, 1)

        self.fill_table()

    def fill_table(self):
        line1_points = self.table.lines["left"].line.get_split_points(len(self.table.data)+1)
        line2_points = self.table.lines["right"].line.get_split_points(len(self.table.data)+1)
        for start, end, data_row in zip(line1_points[1:], line2_points[1:], self.table.data):
            self.annotate_line_manually(
                line=Vector(start, end),
                values=data_row,
                placements=[0.25, 0.75]
            )
