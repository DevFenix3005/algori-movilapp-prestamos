from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from calculos import calcular_cuota

class HomeScreen(Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        contenedor = BoxLayout(orientation="vertical", padding=8, spacing=8)
                                                    # X, Y
        self.monto_prestamo_input = TextInput(size_hint=(1, 0.25), multiline=False, hint_text="Monto del prestamo", font_size=20)
        self.tasa_interes_input = TextInput(size_hint=(1, 0.25), multiline=False, hint_text="Interes del prestamo (%)", font_size=20)
        self.plazo_input = TextInput(size_hint=(1, 0.25), multiline=False, hint_text="Plazo en año", font_size=20)

        calculo_button = Button(text="Calcular", size_hint=(1, 0.25))
        calculo_button.on_press = self.calculo_prestamo_handler

        amortizacion_button = Button(text="Tablas Amortizacion", size_hint=(1, 0.25))
        sub_contenedor_botones = BoxLayout(padding=8, spacing=8)
        sub_contenedor_botones.add_widget(calculo_button)
        sub_contenedor_botones.add_widget(amortizacion_button)


        contenedor_botones = AnchorLayout(anchor_y='bottom')
        contenedor_botones.add_widget(sub_contenedor_botones)
        
        contenedor.add_widget(self.monto_prestamo_input)
        contenedor.add_widget(self.tasa_interes_input)
        contenedor.add_widget(self.plazo_input)
        contenedor.add_widget(contenedor_botones)
        self.add_widget(contenedor)

    def obtener_datos(self):
        monto = self.monto_prestamo_input.text
        interes = self.tasa_interes_input.text
        plazo = self.plazo_input.text
        return monto, interes, plazo

    def calculo_prestamo_handler(self):
        m, i, p = self.obtener_datos()
        if m and i and p:
            monto_prestamo = float(m)
            tasa_interes = float(i)
            plazo = int(p)
            print(f"Monto prestamo: {monto_prestamo}")
            print(f"Tasa interes: {tasa_interes}")
            print(f"Plazo: {plazo}")
            
            cuota, total = calcular_cuota(monto_prestamo, tasa_interes, plazo)
            texto_calculo = f"Pago mensual: ${cuota:,.2f}\nTotal a pagar: ${total:,.2f}"
            popup = Popup(title='Calculo del prestamo',
                content=Label(text=texto_calculo),
                size_hint=(None, None), size=(400, 400))
            popup.open()
        else:
            popup = Popup(title='La validacion ha fallado',
                content=Label(text="Ingresa valores en los campos monto, tasa, plazo"),
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