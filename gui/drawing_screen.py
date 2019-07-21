from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import Screen

from gui.table_visualization import TableVisuallization
from gui.transition_button import TransitionButton


class DrawingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.drawing_layout = BoxLayout(orientation="horizontal", size=(Window.size[0], Window.size[1]))
        self.add_widget(self.drawing_layout)

        self.scatter_triangle = Scatter(do_rotation=False)

        self.drawing_layout_menu = BoxLayout(orientation="vertical", size_hint=(0.1, 1))

        self.back_button = TransitionButton(text="Back", size_hint=(1, 0.7), transition_method="down")

        self.drawing_layout.add_widget(TableVisuallization(size_hint=(0.001, 1)))
        self.drawing_layout.add_widget(self.scatter_triangle)
        self.drawing_layout.add_widget(self.drawing_layout_menu)

        self.export_button = Button(text="Export", size_hint=(1, 0.7))

        self.drawing_layout_menu.add_widget(self.back_button)
        self.drawing_layout_menu.add_widget(self.export_button)
