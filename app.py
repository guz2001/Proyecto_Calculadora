from flask import Flask, render_template, request, jsonify
import sqlite3
from flasgger import Swagger




app = Flask(__name__)
Swagger(app)

#Nombre de la persona 
def actualizar_tabla():
    conexion = sqlite3.connect("calculadora.db")
    cursor = conexion.cursor()
    
    # Añadir la columna 'nombre' si no existe
    try:
        cursor.execute("ALTER TABLE calculos ADD COLUMN nombre TEXT")
        conexion.commit()
    except sqlite3.OperationalError:
        print("La columna 'nombre' ya existe.")

    conexion.close()

# Ejecutar la función
if __name__ == "__main__":
    actualizar_tabla()


# Fórmula para calcular los requerimientos energéticos
def calcular_requerimientos(genero, peso, altura, edad, actividad):
    if genero == "masculino":
        tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

    factores_actividad = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "activo": 1.725,
        "muy_activo": 1.9
    }
    tmb *= factores_actividad.get(actividad, 1.2)
    return round(tmb, 2)

# Ruta principal (frontend)
@app.route('/')
def home():
    return render_template('index.html')

# API para realizar cálculos
@app.route('/calcular', methods=['POST'])
@app.route('/calcular', methods=['POST'])
@app.route('/calcular', methods=['POST'])

@app.route('/calcular', methods=['POST'])
def calcular():
    datos = request.json
    nombre = datos.get('nombre')  # Nuevo campo para el nombre
    genero = datos.get('genero')

    try:
        peso = float(datos.get('peso'))
        altura = float(datos.get('altura'))
        edad = int(datos.get('edad'))
        actividad = datos.get('actividad')
    except (ValueError, TypeError):
        return jsonify({"error": "Los datos ingresados deben ser numéricos"}), 400

    if not all([nombre, genero, peso, altura, edad, actividad]):
        return jsonify({"error": "Faltan datos o son inválidos"}), 400

    calorias = calcular_requerimientos(genero, peso, altura, edad, actividad)

    # Guardar en la base de datos
    conexion = sqlite3.connect("calculadora.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO calculos (nombre, genero, peso, altura, edad, actividad, calorias)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, genero, peso, altura, edad, actividad, calorias))
    conexion.commit()
    conexion.close()

    return jsonify({"calorias_diarias": calorias})

@app.route('/borrar_historial', methods=['DELETE'])
def borrar_historial():
    """
    Borra todos los registros del historial en la base de datos.
    """
    conexion = sqlite3.connect("calculadora.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM calculos")
    conexion.commit()
    conexion.close()
    return jsonify({"mensaje": "Historial borrado correctamente"})



# API para obtener el historial
@app.route('/historial', methods=['GET'])
def historial():
    conexion = sqlite3.connect("calculadora.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM calculos ORDER BY fecha DESC")
    resultados = cursor.fetchall()
    conexion.close()

    historial = [
        {
            "id": fila[0],
            "genero": fila[1],
            "peso": fila[2],
            "altura": fila[3],
            "edad": fila[4],
            "actividad": fila[5],
            "calorias": fila[6],
            "fecha": fila[7]
        }
        for fila in resultados
    ]
    return jsonify(historial)

if __name__ == '__main__':
    app.run(debug=True)
