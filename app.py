from bottle import Bottle, run, template, static_file, request, redirect, response
from db.conexion import conectar
from dat_tecnomax import login_usuario, registrar_usuario, get_stats, get_actividades


app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@app.route('/')
def home():
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos LIMIT 5")
        productos = cursor.fetchall()

        usuario = None
        if persona_id:
            cursor.execute("SELECT nombre FROM persona WHERE id_persona = %s", (persona_id,))
            resultado = cursor.fetchone()
            if resultado:
                usuario = resultado[0]

        conexion.close()
        return template('index', productos=productos, usuario=usuario, rol=rol)
    else:
        return "Error al conectar con la base de datos"

@app.route('/login')
def mostrar_login():
    return template('login')

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
    response.delete_cookie("persona_id", path='/')
    response.delete_cookie("rol", path='/')
    return redirect('/')

@app.route('/dashboardAdmin')
def vista_admin():
    rol = request.get_cookie("rol")
    if rol not in ['admin', 'trabajador']:
        return redirect('/login')
    stats = get_stats()
    print("DEBUG stats:", stats)  # 👈 esto te muestra en consola lo que se está enviando
    return template('dashboardAdmin',
                    titulo='Panel de Administración',
                    stats=stats,
                    actividades=get_actividades())

run(app, host='localhost', port=8080, debug=True)