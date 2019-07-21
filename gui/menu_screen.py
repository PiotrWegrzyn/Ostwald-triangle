from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen

from gui.colored_label import ColoredLabel


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu_layout = GridLayout(cols=2)
        self.add_widget(self.menu_layout)

        self.draw_button = Button(
            text="Draw",
            background_normal='',
            background_color=(15/255, 157/255, 88/255, 1)
        )

        self.set_fuel_button = Button(
            text="Set fuel composition",
            background_normal='',
            background_color=(219/255, 68/255, 55/255, 1)
        )
        self.set_read_button = Button(
            text="Set read chemicals",
            background_normal='',
            background_color=(244 / 255, 180 / 255, 0, 1)
        )
        self.title_label = ColoredLabel((66 / 255, 133 / 255, 244 / 255, 1), text="Main Menu", font_size='40sp')
        self.menu_layout.add_widget(self.title_label)
        self.menu_layout.add_widget(self.draw_button)
        self.menu_layout.add_widget(self.set_fuel_button)
        self.menu_layout.add_widget(self.set_read_button)

