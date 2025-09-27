from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from calculos import calcular_cuota

class HomeScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        contenedor = BoxLayout(orientation="vertical")
                                                    # X, Y
        self.monto_prestamo_input = TextInput(size_hint=(1, 0.25))
        self.tasa_interes_input = TextInput(size_hint=(1, 0.25))
        self.plazo_input = TextInput(size_hint=(1, 0.25))
        calculo_button = Button(text="Calcular")
        calculo_button.on_press = self.calculo_prestamo_handler
        
        contenedor.add_widget(self.monto_prestamo_input)
        contenedor.add_widget(self.tasa_interes_input)
        contenedor.add_widget(self.plazo_input)
        contenedor.add_widget(calculo_button)
        self.add_widget(contenedor)

    def calculo_prestamo_handler(self):
        print("Se preciono el boton")
        monto_prestamo = float(self.monto_prestamo_input.text)
        tasa_interes = float(self.tasa_interes_input.text)
        plazo = int(self.plazo_input.text)
        print(f"Monto prestamo: {monto_prestamo}")
        print(f"Tasa interes: {tasa_interes}")
        print(f"Plazo: {plazo}")
        
        cuota, total = calcular_cuota(monto_prestamo, tasa_interes, plazo)
        texto_calculo = f"Pago mensual: ${cuota:,.2f}\nTotal a pagar: ${total:,.2f}"
        popup = Popup(title='Calculo del prestamo',
            content=Label(text=texto_calculo),
            size_hint=(None, None), size=(400, 400))
        popup.open()
        
class Graph1Screen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        label = Label(text="Esta es mi vista de las graficas 1")
        self.add_widget(label)

class Graph2Screen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        label = Label(text="Esta es mi vista de las graficas 2")
        self.add_widget(label)

        

class MyPrestamoApp(App):
    
    def build(self):
        button_home = Button(text="Home")
        button_home.on_press = self.go_to_home_screen

        button_graph1 = Button(text="Graph1")
        button_graph1.on_press = self.go_to_graph1_screen

        button_graph2 = Button(text="Graph2")
        button_graph2.on_press = self.go_to_graph2_screen
        
        contenedor = BoxLayout(orientation="vertical")
        contenedor_botones = BoxLayout(size_hint=(1, 0.20))
        contenedor_botones.add_widget(button_home)
        contenedor_botones.add_widget(button_graph1)
        contenedor_botones.add_widget(button_graph2)
        
        self.manager = ScreenManager()
        self.manager.add_widget(HomeScreen(name="home"))
        self.manager.add_widget(Graph1Screen(name="graph1"))
        self.manager.add_widget(Graph2Screen(name="graph2"))
        
        contenedor.add_widget(self.manager)
        contenedor.add_widget(contenedor_botones)
        
        return contenedor
    
    def go_to_home_screen(self):
        self.manager.current = "home"
    
    def go_to_graph1_screen(self):
        self.manager.current = "graph1"

    def go_to_graph2_screen(self):
        self.manager.current = "graph2"

    
if __name__ == "__main__":
    my_prestamo_app = MyPrestamoApp()
    my_prestamo_app.run()