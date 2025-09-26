import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="TecnoMax"
        )
        return conexion
    except mysql.connector.Error as error:
        print("Error de conexión:", error)
        return None