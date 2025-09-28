from bottle import redirect, response
import hashlib
from db.conexion import conectar

def login_usuario(request):
    correo = request.forms.get('correo')
    contraseña = request.forms.get('password')
    print("📩 Datos recibidos:")
    print("correo =", repr(correo))
    print("contraseña =", repr(contraseña))
    if not correo or not contraseña:
        return "⚠️ Faltan datos en el formulario"
    conexion = conectar()
    if not conexion:
        print("❌ Error al conectar con la base de datos")
        return "Error al conectar con la base de datos"

    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM persona WHERE correo_ = %s AND contrase = %s", (correo, contraseña))
    usuario = cursor.fetchone()
    conexion.close()
    if usuario:
        print("✅ Usuario encontrado:", usuario)
        response.set_cookie("usuario_id", str(usuario[0]), path='/')
        return redirect('/')
    else:
        print("⚠️ Credenciales incorrectas")
        return "Credenciales incorrectas"

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