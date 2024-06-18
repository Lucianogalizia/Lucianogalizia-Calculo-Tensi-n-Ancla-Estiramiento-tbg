from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    tension_fijacion = ""
    longitud_estiramiento = ""

    if request.method == 'POST':
        try:
            profundidad_ancla = float(request.form['profundidad_ancla'])
            nivel_dinamico = float(request.form['nivel_dinamico'])
            nivel_fijacion = float(request.form['nivel_fijacion'])
            temp_fluido = float(request.form['temp_fluido'])
            gradiente_fluido = float(request.form['gradiente_fluido'])

            tension_fijacion, longitud_estiramiento = calcular_tension_y_estiramiento(
                profundidad_ancla, nivel_dinamico, nivel_fijacion, temp_fluido, gradiente_fluido)

        except ValueError as e:
            error = str(e)

    return render_template('index.html', tension_fijacion=tension_fijacion, longitud_estiramiento=longitud_estiramiento, error=error)

def calcular_tension_y_estiramiento(profundidad_ancla, nivel_dinamico, nivel_fijacion, temp_fluido, gradiente_fluido):
    # Constantes
    diametro_tubing = 2.875  # pulgadas
    area_tubing = 6.49  # pulgadas cuadradas
    coef_poisson = 0.29
    modulo_young = 3.00E+07  # psi
    modulo_expansion_termica = 6.90E-06  # pulg/pulg*°F
    temperatura_media_anual = 134  # °F
    seccion_paredes_tubing = 1.812  # pulgadas cuadradas
    diametro_exterior_tubing = 2.875  # pulgadas
    diametro_interior_tubing = 2.441  # pulgadas

    # Conversiones
    profundidad_ancla_pies = profundidad_ancla / 0.3048  # metros a pies
    nivel_dinamico_pies = nivel_dinamico / 0.3048  # metros a pies
    nivel_fijacion_pies = nivel_fijacion / 0.3048  # metros a pies
    temperatura_fluido_F = temp_fluido * 9/5 + 32  # °C a °F
    delta_temperatura = temperatura_media_anual - temperatura_fluido_F

    # Cálculos
    F1 = area_tubing * gradiente_fluido * nivel_dinamico_pies * (coef_poisson * nivel_dinamico_pies / profundidad_ancla_pies + (1 - 2 * coef_poisson))
    F2 = modulo_young * modulo_expansion_termica * delta_temperatura * profundidad_ancla_pies / 2 * seccion_paredes_tubing
    F3 = area_tubing * gradiente_fluido * (diametro_exterior_tubing**2 - diametro_interior_tubing**2) / diametro_exterior_tubing**2 * nivel_fijacion_pies * (coef_poisson * nivel_fijacion_pies / profundidad_ancla_pies + (1 - 2 * coef_poisson))

    tension_fijacion = F1 + F2 - F3
    longitud_estiramiento = (tension_fijacion * profundidad_ancla_pies) / (modulo_young * area_tubing)

    return tension_fijacion, longitud_estiramiento

if __name__ == '__main__':
    app.run(debug=True)