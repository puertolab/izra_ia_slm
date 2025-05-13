from flask import Flask, request, jsonify, render_template
import csv
import os
import random
import fitz  # PyMuPDF

app = Flask(__name__)

# Ruta del archivo CSV de empleados
CSV_PATH = os.path.join(os.getcwd(), "empleados.csv")
# Ruta del archivo CSV de preguntas frecuentes
FAQ_CSV_PATH = os.path.join(os.getcwd(), "faq.csv")

# Frases motivadoras
PHRASES = [
    "¡Nunca dejes de soñar!",
    "Cada día es una nueva oportunidad para ser mejor.",
    "El esfuerzo de hoy será la recompensa de mañana.",
    "¡El éxito está más cerca de lo que crees!",
    "Tu determinación define tus logros.",
    "La actitud positiva abre puertas inesperadas.",
    "Con paciencia y persistencia, todo es posible.",
    "¡Cree en ti mismo y en tus sueños!",
    "El progreso, no la perfección, es la clave.",
    "¡Hoy es el día perfecto para comenzar!"
]

# Función para extraer texto de un PDF
def extraer_texto_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto.lower()

# Página principal
@app.route('/')
def index():
    phrase = random.choice(PHRASES)
    return render_template('index.html', motivational_phrase=phrase)

# API para buscar extensiones
@app.route('/search', methods=['POST'])
def search():
    search_term = request.json.get('query', '').strip()

    if not search_term:
        return jsonify({"error": "Por favor, ingresa un nombre o departamento para buscar."}), 400

    if not os.path.exists(CSV_PATH):
        return jsonify({"error": "El archivo 'empleados.csv' no existe. Verifica la ruta."}), 500

    try:
        results = []
        with open(CSV_PATH, mode='r', newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if (
                    search_term.lower() in row["Nombre"].lower() or
                    search_term.lower() in row["Departamento"].lower() or
                    search_term in row["Extension"]
                ):
                    results.append({
                        "Nombre": row["Nombre"],
                        "Departamento": row["Departamento"],
                        "Extension": row["Extension"]
                    })

        if results:
            return jsonify(results)
        else:
            return jsonify({"message": "No se encontraron resultados. Intenta de nuevo."}), 404
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error al leer el archivo: {e}"}), 500

# API para buscar manuales PDF
@app.route('/buscar_manual', methods=['POST'])
def buscar_manual():
    query = request.json.get('query', '').strip().lower()
    if not query:
        return jsonify({"error": "Por favor, ingresa una palabra clave para buscar en los manuales."}), 400

    manual_dir = os.path.join(app.root_path, 'static', 'manuales')
    if not os.path.exists(manual_dir):
        return jsonify({"error": "La carpeta de manuales no existe."}), 500

    resultados = []
    for archivo in os.listdir(manual_dir):
        if archivo.endswith('.pdf'):
            ruta_absoluta = os.path.join(manual_dir, archivo)
            texto = extraer_texto_pdf(ruta_absoluta)
            if query in texto:
                resultados.append({
                    "archivo": archivo,
                    "ruta": f"/static/manuales/{archivo}"
                })

    if resultados:
        return jsonify(resultados)
    else:
        return jsonify({"message": "No se encontraron coincidencias en los manuales."}), 404

# API para las preguntas frecuentes
@app.route('/buscar_faq', methods=['POST'])
def buscar_faq():
    query = request.json.get('query', '').strip()

    if not query:
        return jsonify({"error": "Por favor, ingresa una palabra clave para buscar en las preguntas frecuentes."}), 400

    if not os.path.exists(FAQ_CSV_PATH):
        return jsonify({"error": f"El archivo de preguntas frecuentes no existe en la ruta: {FAQ_CSV_PATH}."}), 500

    try:
        resultados = []
        with open(FAQ_CSV_PATH, mode='r', newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                if query.lower() in row['Pregunta'].lower() or query.lower() in row['Respuesta'].lower():
                    resultados.append({
                        "pregunta": row['Pregunta'],
                        "respuesta": row['Respuesta']
                    })

        if resultados:
            return jsonify(resultados)
        else:
            return jsonify({"message": "No se encontraron resultados."}), 404
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error al leer el archivo de FAQ: {str(e)}"}), 500






# Iniciar servidor
if __name__ == "__main__":
    app.run(debug=True)
