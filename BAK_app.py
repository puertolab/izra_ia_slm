from flask import Flask, request, jsonify, render_template
import csv
import os
import random

app = Flask(__name__)

# Ruta del archivo CSV
CSV_PATH = os.path.join(os.getcwd(), "empleados.csv")

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

# Página principal
@app.route('/')
def index():
    phrase = random.choice(PHRASES)  # Selecciona una frase motivadora aleatoria
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
                if search_term.lower() in row["Nombre"].lower() or search_term.lower() in row["Departamento"].lower():
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

if __name__ == "__main__":
    app.run(debug=True)
