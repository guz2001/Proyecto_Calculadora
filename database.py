import sqlite3

def crear_tabla():
    conexion = sqlite3.connect("calculadora.db")
    cursor = conexion.cursor()
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            genero TEXT NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            edad INTEGER NOT NULL,
            actividad TEXT NOT NULL,
            calorias REAL NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conexion.commit()
    conexion.close()

# Ejecutar la función para crear la tabla
if __name__ == "__main__":
    crear_tabla()
