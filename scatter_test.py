from kivy import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter

from main import OstwaldTriangleVisualization

KV = """

#:import win kivy.core.window

<Picture@Scatter>:
    source: None
    on_size: self.center = win.Window.center
    size: image.size
    size_hint: None, None

    Image:
        id: image
        source: root.source
    Rectangle:
        size: self.size
     
FloatLayout:
    Picture:
        source: "test.jpg"
    Picture:
        source: "test.jpg"

"""


class MyApp(App):

    def build(self):
        Config.set('graphics', 'fullscreen', 'auto')
        Config.set('graphics', 'window_state', 'maximized')
        Config.write()
        Window.clearcolor = (1, 1, 1, 1)
        root = FloatLayout()
        scatter = Scatter()
        scatter.add_widget(OstwaldTriangleVisualization())
        # root.add_widget(scatter)
        return scatter
        return Builder.load_string(KV)

MyApp().run()
