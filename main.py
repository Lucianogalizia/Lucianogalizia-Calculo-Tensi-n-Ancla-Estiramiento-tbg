from mimetypes import init
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

def calcular(profundidad_ancla, nivel_dinamico, nivel_fijacion, temp_fluido, gradiente_fluido):
    # Constantes
    diametro_tubing = 2.875 # pulgadas
    area_tubing = 6.49 # pulgadas cuadradas
    coef_poisson = 0.29
    modulo_young = 3.00E+07 # psi
    modulo_expansion_termica = 6.90E-06 # pulg/pulg*°F
    temperatura_media_anual = 134 # °F
    seccion_paredes_tubing = 1.812 # pulgadas cuadradas
    diametro_exterior_tubing = 2.875 # pulgadas
    diametro_interior_tubing = 2.441 # pulgadas

    # Conversiones
    profundidad_ancla_pies = profundidad_ancla / 0.3048 # metros a pies
    nivel_dinamico_pies = nivel_dinamico / 0.3048 # metros a pies
    nivel_fijacion_pies = nivel_fijacion / 0.3048 # metros a pies
    temperatura_fluido_F = temp_fluido * 9/5 + 32 # °C a °F
    delta_temperatura = temperatura_media_anual - temperatura_fluido_F

    # Cálculos
    F1 = area_tubing * gradiente_fluido * nivel_dinamico_pies * (coef_poisson * nivel_dinamico_pies / profundidad_ancla_pies + (1 - 2 * coef_poisson))
    F2 = modulo_young * modulo_expansion_termica * delta_temperatura * profundidad_ancla_pies / 2 * seccion_paredes_tubing
    F3 = area_tubing * gradiente_fluido * (diametro_exterior_tubing**2 - diametro_interior_tubing**2) / diametro_exterior_tubing**2 * nivel_fijacion_pies * (coef_poisson * nivel_fijacion_pies / profundidad_ancla_pies + (1 - 2 * coef_poisson))

    tension_fijacion = F1 + F2 - F3
    longitud_estiramiento = (tension_fijacion * profundidad_ancla_pies) / (modulo_young * area_tubing)

    return F2, tension_fijacion, longitud_estiramiento

class AnchorApp(App):
    def build(self):
        self.title = "Cálculo Tensión de Ancla / Estiramiento tbg"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.inputs = {}
        labels = [
            "Profundidad de Ancla (mts):",
            "Nivel Dinámico (mts):",
            "Nivel del Pozo al momento fijar ancla (mts):",
            "T° Fluido en BDP (°C):",
            "Gradiente Fluido (psi/pie):"
        ]

        for label in labels:
            h_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            h_layout.add_widget(Label(text=label, size_hint_x=None, width=200))
            input_field = TextInput(multiline=False)
            h_layout.add_widget(input_field)
            layout.add_widget(h_layout)
            self.inputs[label] = input_field

        self.result_tension = Label(text="TENSIÓN FIJACIÓN (LIBRAS):")
        self.result_length = Label(text="LONGITUD ESTIRAMIENTO (PLG):")

        layout.add_widget(Button(text="Calcular", on_press=self.on_calculate))
        layout.add_widget(self.result_tension)
        layout.add_widget(self.result_length)
        layout.add_widget(Button(text="Back to menu"))

        return layout

    def on_calculate(self, instance):
        try:
            profundidad_ancla = float(self.inputs["Profundidad de Ancla (mts):"].text)
            nivel_dinamico = float(self.inputs["Nivel Dinámico (mts):"].text)
            nivel_fijacion = float(self.inputs["Nivel del Pozo al momento fijar ancla (mts):"].text)
            temp_fluido = float(self.inputs["T° Fluido en BDP (°C):"].text)
            gradiente_fluido = float(self.inputs["Gradiente Fluido (psi/pie):"].text)

            _, tension_fijacion, longitud_estiramiento = calcular(
                profundidad_ancla, nivel_dinamico, nivel_fijacion, temp_fluido, gradiente_fluido)

            self.result_tension.text = f"TENSIÓN FIJACIÓN (LIBRAS): {tension_fijacion:.2f}"
            self.result_length.text = f"LONGITUD ESTIRAMIENTO (PLG): {longitud_estiramiento:.2f}"
        except ValueError:
            pass

if __name__ == "__main__":
    AnchorApp().run()
