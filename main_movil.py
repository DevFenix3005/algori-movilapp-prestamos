from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class HomeScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        contenedor = BoxLayout(orientation="vertical")
                                                    # X, Y
        monto_prestamo_input = TextInput(size_hint=(1, 0.25))
        tasa_interes_input = TextInput(size_hint=(1, 0.25))
        plazo_input = TextInput(size_hint=(1, 0.25))
        calculo_button = Button(text="Calcular")
        
        contenedor.add_widget(monto_prestamo_input)
        contenedor.add_widget(tasa_interes_input)
        contenedor.add_widget(plazo_input)
        contenedor.add_widget(calculo_button)
        self.add_widget(contenedor)


class MyPrestamoApp(App):
    
    def build(self):
        contenedor = BoxLayout(orientation="vertical")
        contenedor_botones = BoxLayout(size_hint=(1, 0.20))
        contenedor_botones.add_widget(Button(text="Home"))
        contenedor_botones.add_widget(Button(text="Graph1"))
        contenedor_botones.add_widget(Button(text="Graph2"))
        
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        
        contenedor.add_widget(manager)
        contenedor.add_widget(contenedor_botones)
        
        return contenedor
    
    
if __name__ == "__main__":
    my_prestamo_app = MyPrestamoApp()
    my_prestamo_app.run()