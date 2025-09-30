from bottle import Bottle, run, template, static_file, request, redirect, response, TEMPLATE_PATH
from db.conexion import conectar
from dat_tecnomax import (
    login_usuario, registrar_usuario, traer_nombres_prod, traer_prod_por_id, 
    traer_productos, get_stats, get_actividades, get_usuarios, calcular_total_carrito, 
    obtener_carrito, actualizar_cantidad_carrito, agregar_al_carrito, eliminar_del_carrito, 
    contar_items_carrito, finalizar_compra, traer_persona_por_id, registrar_bitacora, 
    actualizar_stock, agregar_producto, get_proveedores, get_categorias, get_productos
)
import os

app = Bottle()

RUTA_VIEWS = os.path.join(os.path.dirname(__file__), 'views')
TEMPLATE_PATH.insert(0, RUTA_VIEWS)

@app.route('/static/<filepath:path>')
def server_static(filepath):
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    return static_file(filepath, root=static_dir)

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

@app.route('/tienda/categoria/<categoria_id:int>')
def do_tienda_categoria(categoria_id):
    productos = traer_productos(categoria_id)
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    usuario = None
    if persona_id:
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM persona WHERE id_persona = %s", (persona_id,))
            resultado = cursor.fetchone()
            if resultado:
                usuario = resultado[0]
            conexion.close()
    if not productos:
        return "Error, no se encontraron productos en esta categoría"
    return template("tienda", todo=productos, usuario=usuario, rol=rol)

@app.route('/tienda')
def do_tienda():
    productos = traer_productos()
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    usuario = None
    if persona_id:
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM persona WHERE id_persona = %s", (persona_id,))
            resultado = cursor.fetchone()
            if resultado:
                usuario = resultado[0]
            conexion.close()
    if not productos:
        return "Error, no se encontro el producto su descripcion "
    return template("tienda", todo=productos, usuario=usuario, rol=rol)

@app.route('/busqueda', method='POST')
def do_busprod():
    filtro = request.forms.get('filtro')
    if not filtro:
        return "Debe escribir algo en el filtro"
    lista = traer_nombres_prod(filtro)
    if not lista:
        return "No se encontro ningún producto"
    return template("busqueda_result", productos=lista)

@app.route('/producto/<id>')
def do_producto(id):
    info = traer_prod_por_id(id)
    if not info:
        return "Error, no se encontro el producto su descripcion "
    return template("producto_detalle", producto=info)

# ✅ RUTA ÚNICA PARA DASHBOARD ADMIN (elimina las duplicadas)
@app.route('/dashboardAdmin')
@app.route('/dashboardAdmin/<seccion>')
def vista_admin(seccion='inicio'):
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    
    # Verificar que está logueado y es admin o trabajador
    if not persona_id or rol not in ['admin', 'trabajador']:
        return redirect('/login')

    stats = get_stats()
    actividades = get_actividades()
    contenido = {}
    
    if seccion == 'usuarios':
        contenido['usuarios'] = get_usuarios()
    elif seccion == 'productos':
        contenido['productos'] = get_productos()
        contenido['categorias'] = get_categorias()
        contenido['proveedores'] = get_proveedores()

    return template('dashboardAdmin',
                    titulo='Panel de Administración',
                    stats=stats,
                    actividades=actividades,
                    seccion=seccion,
                    contenido=contenido)

@app.route('/carrito')
def ver_carrito():
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    carrito = obtener_carrito(int(persona_id))
    subtotal = calcular_total_carrito(int(persona_id))
    return template('carrito', carrito=carrito, subtotal=subtotal, total=subtotal)

@app.route('/agregar-carrito', method='POST')
def do_agregar_carrito():
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    producto_id = request.forms.get('producto_id')
    cantidad = request.forms.get('cantidad', 1)
    
    if not producto_id:
        return "Producto no válido"
    
    resultado, mensaje = agregar_al_carrito(int(persona_id), int(producto_id), int(cantidad))
    if resultado:
        return redirect('/carrito')  # ✅ FALTABA 'return'
    else:
        return template('error', mensaje=mensaje)

@app.route('/actualizar-carrito', method='POST')
def do_actualizar_carrito():
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
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    
    eliminar_del_carrito(int(id_carrito))
    return redirect('/carrito')  # ✅ FALTABA 'return'

@app.route('/checkout')
def ver_checkout():
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    
    carrito = obtener_carrito(int(persona_id))
    if not carrito:
        return redirect('/carrito')  # ✅ FALTABA 'return'
    
    subtotal = calcular_total_carrito(int(persona_id))
    usuario = traer_persona_por_id(int(persona_id))
    return template('checkout', carrito=carrito, subtotal=subtotal, usuario=usuario)

@app.route('/procesar-compra', method='POST')
def do_procesar_compra():
    persona_id = request.get_cookie('persona_id')
    if not persona_id:
        return redirect('/login')
    
    direccion = request.forms.get('direccion_entrega')
    metodo_pago = request.forms.get('metodo_pago', 'efectivo')
    
    if not direccion:
        return "Debe ingresar una dirección de entrega"
    
    resultado, dato = finalizar_compra(int(persona_id), metodo_pago, direccion)
    
    if resultado:
        return template('compra_exitosa', pedido_id=dato)
    else:
        return template('error', mensaje=dato)

@app.route('/api/cantidad-carrito')
def api_cantidad_carrito():
    persona_id = request.get_cookie('persona_id') 
    if not persona_id:
        response.content_type = 'application/json'
        return '{"cantidad": 0}'   
    cantidad = contar_items_carrito(int(persona_id))
    response.content_type = 'application/json'
    return f'{{"cantidad": {cantidad}}}'


@app.route('/admin/producto', method='POST')
def guardar_producto():
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    
    if not persona_id or rol not in ['admin', 'trabajador']:
        return redirect('/login')
    
    # Obtener datos del formulario
    nombre = request.forms.get('nombre')
    descripcion = request.forms.get('descripcion')
    precio = request.forms.get('precio')
    categoria_id = request.forms.get('categoria_id')
    proveedor_id = request.forms.get('proveedor_id')
    cantidad = request.forms.get('cantidad', 0)
    
    print(f"🔧 DEBUG: Datos del formulario - nombre: {nombre}, categoria: {categoria_id}, proveedor: {proveedor_id}")
    
    if not all([nombre, descripcion, precio, categoria_id, proveedor_id]):
        return "❌ Faltan datos obligatorios"
    
    try:
        resultado, mensaje = agregar_producto(
            nombre, descripcion, float(precio), 
            int(categoria_id), int(proveedor_id), int(cantidad), int(persona_id)
        )
    except Exception as e:
        print(f"Error en guardar_producto: {e}")
        return template('error', mensaje=f"Error al procesar: {e}")
    
    if resultado:
        print(f" Producto guardado exitosamente: {mensaje}")
        return redirect('/dashboardAdmin/productos')
    else:
        print(f" Error al guardar producto: {mensaje}")
        return template('error', mensaje=mensaje)


@app.route('/admin/stock', method='POST')
def actualizar_stock_route():
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    
    if not persona_id or rol not in ['admin', 'trabajador']:
        return redirect('/login')
    
    producto_id = request.forms.get('producto_id')
    cantidad = request.forms.get('cantidad')
    
    if not producto_id or not cantidad:
        return "❌ Faltan datos"
    
    if actualizar_stock(int(producto_id), int(cantidad), int(persona_id)):
        registrar_bitacora(f"Actualizó el stock del producto ID:{producto_id} a {cantidad}", persona_id)
        return redirect('/dashboardAdmin/productos') 
        return template('error', mensaje="Error al actualizar stock")

@app.route('/dashboardAdmin/productos/stock/<id:int>')
def form_stock_producto(id):
    persona_id = request.get_cookie("persona_id")
    rol = request.get_cookie("rol")
    
    if not persona_id or rol not in ['admin', 'trabajador']:
        return redirect('/login')
    
    producto = traer_prod_por_id(id)
    if not producto:
        return "Producto no encontrado"
    return template('form_stock', producto=producto)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)