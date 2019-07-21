from kivy.uix.label import Label
from kivy.uix.popup import Popup


def show_popup(title, text):
    popup = Popup(
        title=title,
        content=Label(
            text=text
        ),
        size_hint=(0.6, 0.3))
    popup.open()
