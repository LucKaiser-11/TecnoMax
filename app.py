from bottle import Bottle, run, template, static_file, request, redirect , response ,TEMPLATE_PATH, get
from db.conexion import conectar
from dat_tecnomax import login_usuario, registrar_usuario, traer_nombres_prod, traer_prod_por_id, traer_productos, get_stats, get_actividades, get_usuarios , calcular_total_carrito, obtener_carrito, actualizar_cantidad_carrito,  agregar_al_carrito,eliminar_del_carrito, contar_items_carrito, finalizar_compra, traer_persona_por_id
import os# importe pq no me daba la pgn
import os# importe pq no me daba la pgn

app = Bottle()

RUTA_VIEWS = os.path.join(os.path.dirname(__file__), 'views')# importe pq no me daba la pgn
TEMPLATE_PATH.insert(0, RUTA_VIEWS)# importe pq no me daba la pgn

@app.route('/static/<filepath:path>')
def server_static(filepath):
    #return static_file(filepath, root='./static') ESTABA ANTES
    print(f"Solicitando archivo estático: {filepath}")
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    print(f"Directorio estático: {static_dir}")
    full_path = os.path.join(static_dir, filepath)
    print(f"Ruta completa: {full_path}")
    if os.path.exists(full_path):
        print(f"El archivo existe: {full_path}")
        return static_file(filepath, root=static_dir)
    else:
        print(f"Archivo no encontrado: {full_path}")
        return 'Archivo no encontrado', 404

@app.route('/')
def home():
    persona_id = request.get_cookie("persona_id")#usuario_id = request.get_cookie("usuario_id")
    rol = request.get_cookie("rol")# no estaba
    conexion = conectar()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM productos LIMIT 5")
        productos = cursor.fetchall()

        usuario = None
        if persona_id:#if usuario_id:
            cursor.execute("SELECT nombre FROM persona WHERE id_persona = %s", (persona_id,))
            resultado = cursor.fetchone()
            if resultado:
                usuario = resultado[0]

        conexion.close()
        return template('index', productos=productos, usuario=usuario, rol=rol)# return template('index', productos=productos, usuario=usuario)
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
    response.delete_cookie("persona_id", path='/')# response.delete_cookie("usuario_id", path='/')
    response.delete_cookie("rol", path='/')#print("🔒 Sesión cerrada")
    return redirect('/')
#tienda ver todos los productos
@app.route('/tienda')
def do_tienda():
    productos= traer_productos()
    if not productos:
        return "Error, no se encontro el producto su descripcion "
    return template("tienda", todo=productos)
#buscar
@app.route('/busqueda', method='POST')
def do_busprod():
    filtro = request.forms.get('filtro')
    if not filtro:#ya no len
        return "Debe escribir algo en el filtro"
    lista = traer_nombres_prod(filtro)
    if not lista:#if len(lista)==0:
        return "No se encontro ningún producto"

    return template("busqueda_result", productos=lista)
@app.route('/producto/<id>')
def do_producto(id):#ruta, endpoint, controladores producto inf
    info= traer_prod_por_id(id)
    
    if not info:
        return "Error, no se encontro el producto su descripcion "
    return template("producto_detalle", producto=info)

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
@app.route('/dashboardAdmin')
@app.route('/dashboardAdmin/<seccion>')
def vista_admin(seccion='inicio'):
    rol = request.get_cookie("rol")
    if rol not in ['admin', 'trabajador']:
        return redirect('/login')

    stats = get_stats()
    actividades = get_actividades()

    contenido = {}
    if seccion == 'usuarios':
        contenido['usuarios'] = get_usuarios()

    return template('dashboardAdmin',
                    titulo='Panel de Administración',
                    stats=stats,
                    actividades=actividades,
                    seccion=seccion,
                    contenido=contenido)
@app.route('/carrito')
def ver_carrito():
    """Muestra la página del carrito"""
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    carrito = obtener_carrito(int(persona_id))
    subtotal = calcular_total_carrito(int(persona_id))
    
    return template('carrito',   carrito=carrito, subtotal=subtotal,   total=subtotal)

@app.route('/agregar-carrito', method='POST')
def do_agregar_carrito():
    """Agregar producto al carrito"""
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    producto_id = request.forms.get('producto_id')
    cantidad = request.forms.get('cantidad', 1)
    
    if not producto_id:
        return "Producto no válido"
    
    resultado, mensaje = agregar_al_carrito(  int(persona_id), int(producto_id),  int(cantidad) )
    if resultado:
        redirect('/carrito')
    else:
        return template('error', mensaje=mensaje)


@app.route('/actualizar-carrito', method='POST')
def do_actualizar_carrito():
    """Actualizar cantidades del carrito"""
    persona_id = request.get_cookie('persona_id')
    
    if not persona_id:
        return redirect('/login')
    
    carrito = obtener_carrito(int(persona_id))
    
    for item in carrito:
        nueva_cantidad = request.forms.get(f"cantidad_{item['id_carrito']}")
        if nueva_cantidad and nueva_cantidad.isdigit():
            actualizar_cantidad_carrito(item['id_carrito'], int(nueva_cantidad))
    
    return redirect('/carrito')


@app.route('/eliminar-carrito/<id_carrito>', method='POST')
def do_eliminar_carrito(id_carrito):
    """Eliminar producto del carrito"""
    persona_id = request.get_cookie('persona_id')
    
    if not persona_id:
        return redirect('/login')
    
    eliminar_del_carrito(int(id_carrito))
    redirect('/carrito')


@app.route('/checkout')
def ver_checkout():
    """Página de checkout (formulario de compra)"""
    persona_id = request.get_cookie('persona_id')
    
    if not persona_id:
        return redirect('/login')
    
    carrito = obtener_carrito(int(persona_id))
    
    if not carrito:
        redirect('/carrito')
    
    subtotal = calcular_total_carrito(int(persona_id))
    
    # Obtener datos del usuario para prellenar el formulario
    usuario = traer_persona_por_id(int(persona_id))
    
    return template('checkout',    carrito=carrito, subtotal=subtotal,    usuario=usuario)

@app.route('/procesar-compra', method='POST')
def do_procesar_compra():
    """Finalizar la compra (procesa el pedido)"""
    persona_id = request.get_cookie('persona_id')
    
    if not persona_id:
        return redirect('/login')
    
    direccion = request.forms.get('direccion_entrega')
    metodo_pago = request.forms.get('metodo_pago', 'efectivo')  # valor por defecto: efectivo
    
    if not direccion:
        return "Debe ingresar una dirección de entrega"
    
    resultado, dato = finalizar_compra(int(persona_id), metodo_pago, direccion)
    
    if resultado:
        # dato contiene el pedido_id
        return template('compra_exitosa', pedido_id=dato)
    else:
        # dato contiene el mensaje de error
        return template('error', mensaje=dato)


@app.route('/api/cantidad-carrito')
def api_cantidad_carrito():
    """API para obtener cantidad de items (para mostrar en el header)"""
    persona_id = request.get_cookie('usuario_id')
    
    if not persona_id:
        response.content_type = 'application/json'
        return '{"cantidad": 0}'   
    cantidad = contar_items_carrito(int(persona_id))
    response.content_type = 'application/json'
    return f'{{"cantidad": {cantidad}}}'

run(app, host='localhost', port=8080, debug=True)