from bottle import redirect, response, template, request
import hashlib
import mysql.connector
from db.conexion import conectar

def login_usuario(request):
    correo = request.forms.get('correo')
    contraseña = request.forms.get('password')

    if not correo or not contraseña:
        return template('login', error='⚠️ Faltan datos en el formulario')

    conexion = conectar()
    if not conexion:
        return "❌ Error al conectar con la base de datos"

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.id_persona, r.nombre
        FROM persona p
        JOIN rol r ON p.rol_id = r.id_rol
        WHERE p.correo_ = %s AND p.contrase = %s
    """, (correo, contraseña))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario:
        persona_id, rol = usuario
        response.set_cookie("persona_id", str(persona_id), path='/')
        response.set_cookie("rol", rol, path='/')

        if rol in ['admin', 'trabajador']:
            return redirect('dashboardAdmin')
        elif rol == 'cliente':
            return redirect('/')
        else:
            return "⚠️ Rol no reconocido"
    else:
        return template('login', error='Credenciales incorrectas')

def registrar_usuario(request):
        nombre = request.forms.get('nombre')
        apellidoPat = request.forms.get('apellidoPat')
        apellidoMat = request.forms.get('apellidoMat')
        correo = request.forms.get('correo_reg')
        direccion = request.forms.get('direccion')
        telefono = request.forms.get('telefono')
        contrase = request.forms.get('pass_reg')
        if not (nombre and correo and contrase):
            return "⚠️ Faltan datos obligatorios"
        conexion = conectar()
        if not conexion:
            return "❌ Error al conectar con la base de datos"
        cursor = conexion.cursor()
        cursor.execute("SELECT id_rol FROM rol WHERE nombre = 'cliente'")
        resultado = cursor.fetchone()
        rol_cliente = resultado[0] if resultado else 2
        cursor.execute("SELECT id_persona FROM persona WHERE correo_ = %s", (correo,))
        if cursor.fetchone():
            conexion.close()
            return "⚠️ Ya existe una cuenta con ese correo"
        cursor.execute("""
            INSERT INTO persona (nombre, apellidoPat, apellidoMat, correo_, direccion, telefono, contrase, rol_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellidoPat, apellidoMat, correo, direccion, telefono, contrase, rol_cliente))
        conexion.commit()
        conexion.close()
        print(f"✅ Usuario registrado: {correo}")
        return redirect('/login')
#tienda ver todos los productos
def traer_productos():
    productos=[]
    try: 
        conn= conectar()
        if conn:
            cursor= conn.cursor()
            query = "SELECT id_producto, nombre, precio, categoria_id FROM productos;"
            cursor.execute(query)
            resultados = cursor.fetchall()
            productos = [dict(zip(['id_producto','nombre','precio','categoria_id'], fila)) for fila in resultados]
    except mysql.connector.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return productos
 #busqueda 
def traer_nombres_prod(filtro):
    prod = []
    try:
        conn = conectar()
        if conn:
            cursor=conn.cursor()
            query = "SELECT id_producto, nombre, precio FROM productos WHERE nombre LIKE %s;"
            cursor.execute(query, ("%" + filtro + "%",))
            resultados = cursor.fetchall()
            prod = [dict(zip(['id_producto', 'nombre','precio' ], fila)) for fila in resultados]
    except mysql.connector.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return prod
#inf de cada producto
def traer_prod_por_id(id):
    producto = None
    try:
        conn=conectar() #with obtener_conexion_bd(conf) as conn:
        if conn: #with conn.cursor() as cursor:
            cursor=conn.cursor()
            query = "select * FROM productos WHERE id_producto = %s;"
            cursor.execute(query, (int(id),))
            resultado = cursor.fetchone()
            if resultado:
                columnas = [desc[0] for desc in cursor.description]
                producto = dict(zip(columnas, resultado))
    except mysql.connector.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return producto

def get_stats():
    conexion = conectar()
    if not conexion:
        return {'usuarios': 0, 'productos': 0, 'pedidos': 0, 'inventario_bajo': 0}

    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM persona")
    usuarios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM productos")
    productos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM estados_generales WHERE nombre = 'pendiente'")
    pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM inventario WHERE cantidad_actual < 40")
    inventario_bajo = cursor.fetchone()[0]

    conexion.close()
    return {
        'usuarios': usuarios,
        'productos': productos,
        'pedidos': pedidos,
        'inventario_bajo': inventario_bajo
    }

def get_actividades():
    conexion = conectar()
    if not conexion:
        return []

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.nombre, r.tipo_movimiento, r.fecha, r.cantidad
        FROM registro_movimientos r
        JOIN persona p ON r.persona_id = p.id_persona
        ORDER BY r.fecha DESC
        LIMIT 10
    """)
    filas = cursor.fetchall()
    conexion.close()

    actividades = []
    for fila in filas:
        usuario, accion, fecha, cantidad = fila
        actividades.append({
            'usuario': usuario,
            'accion': accion,
            'fecha': fecha.strftime('%Y-%m-%d %H:%M'),
            'cantidad': cantidad
        })
    return actividades