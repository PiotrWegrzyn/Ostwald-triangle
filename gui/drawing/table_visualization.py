from kivy.uix.floatlayout import FloatLayout

from models.table import Table


class TableVisuallization(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.table = Table(75, 95)
        self.table.draw(self.canvas)
