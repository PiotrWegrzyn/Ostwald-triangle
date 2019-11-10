from kivy.uix.floatlayout import FloatLayout

from models.table import Table


class PhiTableVisualization(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        phi_data = [["Phi", "Lambda"]]+[[i*0.1, 1/(i*0.1)] for i in range(1, 16)]

        self.table = Table(75, 95, phi_data)
        self.table.draw(self.canvas)
