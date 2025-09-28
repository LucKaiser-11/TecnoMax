import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="tecnomax"
        )
        print("✅ Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as error:
        print("❌ Error de conexión:", error)
        return None