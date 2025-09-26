from bottle import Bottle, run, template
from db.conexion import conectar

app = Bottle()

@app.route('/')
def home():
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos LIMIT 5")
        productos = cursor.fetchall()
        conexion.close()
        return template('index', productos=productos)
    else:
        return "Error al conectar con la base de datos"

run(app, host='localhost', port=8080, debug=True)