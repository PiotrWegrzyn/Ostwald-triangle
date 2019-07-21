from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from gui.colors import COLORS
from gui.components.colored_label import ColoredLabel
from gui.components.transition_button import TransitionButton


class AboutScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation="horizontal")
        self.text_container = BoxLayout(orientation="vertical")

        self.app_title = ColoredLabel(
            text="The Ostwald Triangle Generator", bg_color=COLORS["red"], size_hint=(1, 0.3), font_size='40sp')
        self.description = ColoredLabel(
            text="The app's task is to generate an Ostwald Triangle graph.\n"
                 "The graph is generated based on:\n"
                 "- fuel composition\n"
                 "- measured exhaust composition\n"
                 ""
                 "The app also has an export feature which generates\n"
                 "a .png file with the graphics that the app generated.\n"
                 "The file can be found in 'Exports' folder.",
            bg_color=COLORS["green"],
            size_hint=(1, 0.6),
            font_size='25sp'

        )
        self.author = ColoredLabel(
            text="Author: Piotr Węgrzyn", bg_color=COLORS["yellow"], size_hint=(1, 0.1), font_size='20sp')

        self.text_container.add_widget(self.app_title)
        self.text_container.add_widget(self.description)
        self.text_container.add_widget(self.author)

        self.back_button = TransitionButton(
            text="Back",
            size_hint=(0.1, 1),
            transition_method="down",
            background_normal='',
            background_color=COLORS["blue"],
            font_size='20sp'
        )
        self.layout.add_widget(self.text_container)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)


