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
def get_usuarios():
    conexion = conectar()
    if not conexion:
        return []

    cursor = conexion.cursor()
    cursor.execute("""
        SELECT p.nombre, p.correo_, r.nombre AS rol
        FROM persona p
        JOIN rol r ON p.rol_id = r.id_rol
    """)
    usuarios = [{'nombre': u[0], 'correo': u[1], 'rol': u[2]} for u in cursor.fetchall()]
    conexion.close()
    return usuarios
#carrito
def agregar_al_carrito(persona_id, producto_id, cantidad):#agrgar producto al carrito
    """Agrega un producto al carrito"""
    resultado = False
    mensaje = ""
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            
            # Verificar stock disponible
            query_stock = " SELECT cantidad_actual FROM inventario  WHERE producto_id = %s "
            cursor.execute(query_stock, (producto_id,))
            stock = cursor.fetchone()
            
            if not stock or stock[0] < cantidad:
                mensaje = "Stock insuficiente"
                return False, mensaje      
            # Verificar si el producto ya está en el carrito
            query_existe = "SELECT id_carrito, cantidad  FROM carrito WHERE persona_id = %s AND producto_id = %s"
            cursor.execute(query_existe, (persona_id, producto_id))
            carrito_existente = cursor.fetchone()
            
            if carrito_existente:
                # Actualizar cantidad
                nueva_cantidad = carrito_existente[1] + cantidad
                if stock[0] < nueva_cantidad:
                    mensaje = f"Stock insuficiente. Disponible: {stock[0]}"
                    return False, mensaje
                
                query_update = " UPDATE carrito  SET cantidad = %s, fecha_agregado = NOW() WHERE id_carrito = %s "
                cursor.execute(query_update, (nueva_cantidad, carrito_existente[0]))
                mensaje = "Cantidad actualizada en el carrito"
            else:
                query_insert = "  INSERT INTO carrito (persona_id, producto_id, cantidad, fecha_agregado)  VALUES (%s, %s, %s, NOW())"
                cursor.execute(query_insert, (persona_id, producto_id, cantidad))
                mensaje = "Producto agregado al carrito"
            
            conn.commit()
            resultado = True
            
    except mysql.connector.Error as e:
        print(f"Error al agregar al carrito: {e}")
        mensaje = f"Error: {e}"
    except Exception as e:
        print(f"Error inesperado: {e}")
        mensaje = f"Error inesperado: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()
    
    return resultado, mensaje


def obtener_carrito(persona_id):
    """Obtiene todos los productos del carrito de un usuario"""
    carrito = []
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            query = """ SELECT c.id_carrito, c.cantidad, c.fecha_agregado, p.id_producto, p.nombre, p.precio, (c.cantidad * p.precio) as subtotal
                FROM carrito c
                INNER JOIN productos p ON c.producto_id = p.id_producto
                WHERE c.persona_id = %s
                ORDER BY c.fecha_agregado DESC
            """
            cursor.execute(query, (persona_id,))
            resultados = cursor.fetchall()
            
            if resultados:
                columnas = [desc[0] for desc in cursor.description]
                carrito = [dict(zip(columnas, fila)) for fila in resultados]
                
    except mysql.connector.Error as e:
        print(f"Error al obtener carrito: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()   
    return carrito


def calcular_total_carrito(persona_id):
    """Calcula el total del carrito"""
    total = 0.0
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT SUM(c.cantidad * p.precio) as total FROM carrito c
                INNER JOIN productos p ON c.producto_id = p.id_producto WHERE c.persona_id = %s
            """
            cursor.execute(query, (persona_id,))
            resultado = cursor.fetchone()
            
            if resultado and resultado[0]:
                total = float(resultado[0])
                
    except mysql.connector.Error as e:
        print(f"Error al calcular total: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    
    return total

def actualizar_cantidad_carrito(id_carrito, nueva_cantidad):
    """Actualiza la cantidad de un producto en el carrito"""
    resultado = False
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            
            # Primero obtenemos el producto_id del carrito
            cursor.execute("SELECT producto_id FROM carrito WHERE id_carrito = %s", (id_carrito,))
            carrito_item = cursor.fetchone()
            
            if carrito_item:
                producto_id = carrito_item[0]
                
                # Verificamos el stock disponible
                cursor.execute("SELECT cantidad_actual FROM inventario WHERE producto_id = %s", (producto_id,))
                stock = cursor.fetchone()
                
                if stock and stock[0] >= nueva_cantidad:
                    # Si hay suficiente stock, actualizamos la cantidad
                    query = "UPDATE carrito SET cantidad = %s, fecha_agregado = NOW() WHERE id_carrito = %s"
                    cursor.execute(query, (nueva_cantidad, id_carrito))
                    conn.commit()
                    resultado = True
                    print(f"✅ Cantidad actualizada: {nueva_cantidad} para carrito_id: {id_carrito}")
                else:
                    print(f"❌ Stock insuficiente. Disponible: {stock[0] if stock else 0}")
            else:
                print(f"❌ No se encontró el item en el carrito: {id_carrito}")
            
    except mysql.connector.Error as e:
        print(f"Error al actualizar cantidad: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()  
    return resultado

def eliminar_del_carrito(id_carrito):
    """Elimina un producto del carrito"""
    resultado = False
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            query = "DELETE FROM carrito WHERE id_carrito = %s"
            cursor.execute(query, (id_carrito,))
            conn.commit()
            resultado = True
            
    except mysql.connector.Error as e:
        print(f"Error al eliminar del carrito: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    
    return resultado

def contar_items_carrito(persona_id):
    """Cuenta cuántos productos hay en el carrito"""
    cantidad = 0
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM carrito WHERE persona_id = %s"
            cursor.execute(query, (persona_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                cantidad = resultado[0]
                
    except mysql.connector.Error as e:
        print(f"Error al contar items: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    
    return cantidad 
def finalizar_compra(persona_id, metodo_pago, direccion_entrega):
    """ Proceso completo de compra:  1. Crear pedido 2. Mover carrito a detalle_pedido
    3. Vaciar carrito  4. Registrar en bitácora (automático por trigger)
    """
    resultado = False
    pedido_id = None
    
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
        
            query_verificar = "  SELECT COUNT(*) FROM carrito WHERE persona_id = %s  " #verificar que hay productos en el carrito
            cursor.execute(query_verificar, (persona_id,))
            cantidad_items = cursor.fetchone()[0]
            
            if cantidad_items == 0:
                return False, "El carrito está vacío"
            
            # 2. Crear el pedido
            query_pedido = "INSERT INTO pedidos (persona_id, fecha, estado_general)  VALUES (%s, NOW(), 'pendiente')"
            cursor.execute(query_pedido, (persona_id,))
            pedido_id = cursor.lastrowid
            
            # 3. Mover productos del carrito a detalle_pedido
            query_detalle = """ INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario)
                SELECT %s, c.producto_id, c.cantidad, p.precio  FROM carrito c
                INNER JOIN productos p ON c.producto_id = p.id_producto
                WHERE c.persona_id = %s
            """
            cursor.execute(query_detalle, (pedido_id, persona_id))
            
            # 4. Crear registro de pago
            query_pago = """  INSERT INTO pagos (pedido_id, fecha_pago, monto, estado_id)
                SELECT %s, NOW(), SUM(c.cantidad * p.precio), 1 FROM carrito c
                INNER JOIN productos p ON c.producto_id = p.id_producto
                WHERE c.persona_id = %s
            """
            cursor.execute(query_pago, (pedido_id, persona_id))
            
            # 5. Crear registro de envío
            query_envio = " INSERT INTO envios (pedido_id, direccion_entrega, fecha_envio, estado_id) VALUES (%s, %s, NOW(), 1)"
            cursor.execute(query_envio, (pedido_id, direccion_entrega))
            
            query_vaciar = " DELETE FROM carrito WHERE persona_id = %s"# 6. VACIAR el carrito (ya completó la compra)
            cursor.execute(query_vaciar, (persona_id,))  
        
            conn.commit()#confirmar transacción
            resultado = True
            
    except mysql.connector.Error as e:
        print(f"Error al finalizar compra: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Error inesperado: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cursor.close()
            conn.close()
    return resultado, pedido_id
def traer_persona_por_id(persona_id):
    persona = None
    try:
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT id_persona, nombre, apellidoPat, apellidoMat, correo_, direccion, telefono
                FROM persona
                WHERE id_persona = %s
            """
            cursor.execute(query, (persona_id,))
            resultado = cursor.fetchone()
            if resultado:
                columnas = [desc[0] for desc in cursor.description]
                persona = dict(zip(columnas, resultado))
    except mysql.connector.Error as e:
        print(f"Error al obtener persona: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()
    return persona