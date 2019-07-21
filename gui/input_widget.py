from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from gui.colors import COLORS
from gui.input_scroll_layout import InputScrollGrid


class InputWidget(BoxLayout):
    def __init__(self, **kwargs):
        self.initial = kwargs.pop("initial", 5)
        self.cols = kwargs.pop("cols", 2)
        self.cols_proportions = kwargs.pop("cols_proportions", None)

        super().__init__(orientation="vertical", **kwargs)
        self.input_scroll = InputScrollGrid(initial=self.initial, cols=self.cols, cols_proportions=self.cols_proportions)

        self.more_button = Button(
            text="More",
            size_hint=(1, 0.1),
            background_normal='',
            background_color=COLORS["green"],
        )
        self.more_button.bind(on_press=self.add_more_rows)

        self.add_widget(self.input_scroll)
        self.add_widget(self.more_button)

    def add_more_rows(self, btn):
        self.input_scroll.add_row()

    def get_inputs(self):
        return self.input_scroll.get_inputs()
