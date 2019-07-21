from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from gui.colors import COLORS
from gui.components.colored_label import ColoredLabel
from gui.components.transition_button import TransitionButton


class SetMeasuredScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_layout = BoxLayout(orientation="horizontal")

        self.back_button = TransitionButton(
            text="Back",
            transition_method="right",
            size_hint=(0.1, 1),
            background_normal='',
            background_color=COLORS["blue"],
            font_size='20sp'
        )

        self.input_grid = GridLayout(
            cols=2,
            padding=[20, 20, 20, 20],
            spacing=(30, 30),
            row_force_default=True,
            row_default_height=40,
        )
        self.co2_input = TextInput(text="6",  size_hint_x=0.5)
        self.input_grid.add_widget(ColoredLabel(text="CO2", bg_color=COLORS["red"], size_hint_x=0.5))
        self.input_grid.add_widget(self.co2_input)

        self.o2_input = TextInput(text="2", size_hint_x=0.5)
        self.input_grid.add_widget(ColoredLabel(text="O2", bg_color=COLORS["red"], size_hint_x=0.5))
        self.input_grid.add_widget(self.o2_input)

        self.menu_layout.add_widget(self.input_grid)
        self.menu_layout.add_widget(self.back_button)
        self.add_widget(self.menu_layout)



