from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class InputScrollGrid(ScrollView):
    def __init__(self, **kwargs):
        self.initial = kwargs.pop("initial", 5)
        self.cols = kwargs.pop("cols", 1)
        self.cols_proportions = kwargs.pop("cols_proportions", None)
        if not self.cols_proportions:
            self.cols_proportions = [1/self.cols for _ in range(self.cols)]
        super().__init__(size_hint=(1, 0.9), **kwargs)
        self.rows = []
        self.input_grid = GridLayout(
            cols=self.cols,
            row_force_default=True,
            row_default_height=40,
            spacing=(15, 15),
            padding=[20, 20, 20, 20],
            size_hint_y=None
        )
        self.input_grid.bind(minimum_height=self.input_grid.setter('height'))
        for i in range(self.initial):
            self.add_row()
        self.add_widget(self.input_grid)

    def add_row(self):
        row = []
        for i in range(self.cols):
            row.append(TextInput(size_hint_x=self.cols_proportions[i]))
        for input in row:
            self.input_grid.add_widget(input)
        self.rows.append(row)

    def get_inputs(self):
        return self.rows