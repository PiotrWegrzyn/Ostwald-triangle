from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from gui.colors import COLORS
from gui.components.input_scroll_layout import InputScrollGrid


class InputWidget(BoxLayout):
    def __init__(self, **kwargs):
        self.initial_rows = kwargs.pop("initial_rows", 1)
        self.initial_data = kwargs.pop("initial_data", None)
        self.cols = kwargs.pop("cols", 2)
        self.cols_proportions = kwargs.pop("cols_proportions", None)
        self.labels = kwargs.pop("labels", None)

        super().__init__(orientation="vertical", **kwargs)

        self.input_layout = InputScrollGrid(
            initial_rows=self.initial_rows,
            cols=self.cols,
            cols_proportions=self.cols_proportions,
            labels=self.labels,
            initial_data=self.initial_data
        )
        self.more_button = Button(
            text="More",
            size_hint=(1, 0.1),
            background_normal='',
            background_color=COLORS["green"],
            font_size='20sp'
        )
        self.more_button.bind(on_press=self.add_more_rows)

        self.add_widget(self.input_layout)
        self.add_widget(self.more_button)

    def add_more_rows(self, btn):
        self.input_layout.add_row()

    def get_inputs(self):
        return self.input_layout.get_inputs()
