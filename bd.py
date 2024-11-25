# import pymysql
# import os

# def obtener_conexion():
#     try:
#         conexion = pymysql.connect(
#             host='junction.proxy.rlwy.net',
#             port=41697,
#             user='root',
#             password='zKvJnyPqfGLmaRiZqvqMRCePODgILIqr',
#             db='ReservasDeCanchas',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         print("Conexión exitosa a la base de datos.")
#         return conexion
#     #junction.proxy.rlwy.net:39981
#     except Exception as e:
#         print(f"Error al conectar a la base de datos: {e}")
#         return None 
    
import pymysql
import os

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host='localhost',  # Cambia esto si tu servidor no está en localhost
            user='root',       # Usuario de la base de datos
            password='Mendoza110427',  # Contraseña del usuario
            db='reservasdecanchas',    # Nombre de la base de datos
            port=3306                  # Puerto estándar para MySQL
        )
        print("Conexión exitosa a la base de datos.")
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Prueba la conexión
if __name__ == "__main__":
    conexion = obtener_conexion()
    if conexion:
        conexion.close()
        print("Conexión cerrada.")
