from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from gui.colors import COLORS
from gui.components.transition_button import TransitionButton


class MainMenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_layout = GridLayout(cols=2)
        self.add_widget(self.menu_layout)
        self.about_button = TransitionButton(
            text="About",
            background_normal='',
            background_color=COLORS["blue"],
            transition_method="up",
            font_size='40sp'
        )
        self.draw_button = TransitionButton(
            text="Draw",
            background_normal='',
            background_color=COLORS["green"],
            transition_method="up",
            font_size='40sp'
        )

        self.set_fuel_button = TransitionButton(
            text="Set fuel composition",
            background_normal='',
            background_color=COLORS["red"],
            transition_method="right",
            font_size='30sp'
        )
        self.set_measured_button = TransitionButton(
            text="Set measured\n composition",
            background_normal='',
            background_color=COLORS["yellow"],
            transition_method="left",
            font_size='30sp'
        )
        self.menu_layout.add_widget(self.about_button)
        self.menu_layout.add_widget(self.draw_button)
        self.menu_layout.add_widget(self.set_fuel_button)
        self.menu_layout.add_widget(self.set_measured_button)

