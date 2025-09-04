import sqlite3
from flask import Flask, g, jsonify, request

def dict_factory(cursor, row):
    """Convierte cada fila de la DB en un diccionario"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def abrirConexion():
    if 'db' not in g:
        g.db = sqlite3.connect("sensores.sqlite")
        g.db.row_factory = dict_factory
    return g.db

def cerrarConexion(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app = Flask(__name__)
app.teardown_appcontext(cerrarConexion)

@app.route("/api/test")
def test():
    return "funcionando!"

@app.route("/api/sensor", methods=['POST'])
def sensor():
    datos = request.json
    nombre = datos["nombre"]
    valor = datos["valor"]
    fecha_hora = datos["fecha_hora"]

    db = abrirConexion()
    db.execute(
        "INSERT INTO datos (nombre, valor, fecha_hora) VALUES (?, ?, ?)",
        (nombre, valor, fecha_hora)
    )
    db.commit()
    cerrarConexion()

    print(f"nombre del sensor: {nombre}, valor: {valor}, Fecha_hora: {fecha_hora}")  
    return "OK"

@app.route('/api/register', methods=['POST'])
def login():
    nombre = request.form['nombre']
    fila = abrirConexion().execute(
        'SELECT * FROM datos WHERE nombre = ?', (nombre,)
    ).fetchone()

    if fila:
        return jsonify(fila)
    else:
        return jsonify({"error": "No encontrado"}), 404

def crear_tabla():
    db = sqlite3.connect("sensores.sqlite")
    db.execute("""
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            valor REAL NOT NULL,
            fecha_hora TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

# Crear tabla antes de iniciar el servidor
crear_tabla()
