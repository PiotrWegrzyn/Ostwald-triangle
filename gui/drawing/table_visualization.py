from kivy.uix.floatlayout import FloatLayout

from models.table import Table


class TableVisuallization(FloatLayout):
    def __init__(self, x, y, data, **kwargs):
        super().__init__(**kwargs)

        self.table = Table(x, y, data)
        self.table.draw(self.canvas)
