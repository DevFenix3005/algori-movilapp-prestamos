from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class Graph2Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw, name="chart-bar")
        label = Label(text="Esta es mi vista de las graficas 2")
        self.add_widget(label)
