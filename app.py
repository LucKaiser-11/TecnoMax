from bottle import Bottle, run, template, static_file, request, redirect , response
from db.conexion import conectar
from dat_tecnomax import login_usuario, registrar_usuario

app = Bottle()

# Ruta para servir archivos estáticos (CSS, imágenes, JS)
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Ruta principal (landing page)
@app.route('/')
def home():
    usuario_id = request.get_cookie("usuario_id")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos LIMIT 5")
        productos = cursor.fetchall()

        usuario = None
        if usuario_id:
            cursor.execute("SELECT nombre FROM persona WHERE id_persona = %s", (usuario_id,))
            resultado = cursor.fetchone()
            if resultado:
                usuario = resultado[0]

        conexion.close()
        return template('index', productos=productos, usuario=usuario)
    else:
        return "Error al conectar con la base de datos"


# Mostrar formulario de login/registro
@app.route('/login')
def mostrar_login():
    return template('login')

# Procesar login o registro desde el mismo formulario
@app.post('/login')
def procesar_login():
    accion = request.forms.get('accion')
    if accion == 'login':
        return login_usuario(request)
    elif accion == 'registro':
        return registrar_usuario(request)
    else:
        return "Acción no reconocida"

@app.route('/logout')
def cerrar_sesion():
    response.delete_cookie("usuario_id", path='/')
    print("🔒 Sesión cerrada")
    return redirect('/')

run(app, host='localhost', port=8080, debug=True)