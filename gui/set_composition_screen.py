from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from gui.colors import COLORS
from gui.input_widget import InputWidget
from gui.transition_button import TransitionButton


class SetCompositionScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_layout = BoxLayout(orientation="horizontal")

        self.back_button = TransitionButton(
            text="Back",
            transition_method="left",
            size_hint=(0.1, 1),
            background_normal='',
            background_color=COLORS["blue"],
            font_size='20sp'
        )

        self.input_widget = InputWidget(
            cols=2,
            cols_proportions=[0.8, 0.2],
            labels=["Chemical composition", "Proportion"]
        )

        self.menu_layout.add_widget(self.input_widget)
        self.menu_layout.add_widget(self.back_button)
        self.add_widget(self.menu_layout)



