from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import Screen

from gui.colors import COLORS
from gui.components.transition_button import TransitionButton
from gui.drawing.phi_table_visualization import PhiTableVisualization


class DrawingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.drawing_layout = FloatLayout(size=(Window.size[0], Window.size[1]))
        self.add_widget(self.drawing_layout)

        self.scatter_triangle = Scatter(do_rotation=False, size_hint=(0.6, 1.1))

        self.drawing_layout_menu = BoxLayout(orientation="vertical", pos_hint={'x': 0.9}, size_hint=(0.1, 1))

        self.back_button = TransitionButton(
            text="Back",
            size_hint=(1, 0.7),
            transition_method="down",
            background_normal='',
            background_color=COLORS["blue"],
            font_size='20sp'
        )

        self.drawing_layout.add_widget(self.drawing_layout_menu)
        self.drawing_layout.add_widget(self.scatter_triangle)
        self.drawing_layout.add_widget(PhiTableVisualization(size_hint=(0.1, 1)))
        self.result_table_placeholder = FloatLayout(size_hint=(0.1, 1))
        self.drawing_layout.add_widget(self.result_table_placeholder)

        self.export_button = Button(
            size_hint=(1, 0.7),
            background_normal='',
            background_color=COLORS["yellow"],
            text="Export",
            font_size='20sp'

        )

        self.drawing_layout_menu.add_widget(self.back_button)
        self.drawing_layout_menu.add_widget(self.export_button)
