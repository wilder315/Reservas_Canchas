# class Config():
#     DB_HOST = 'junction.proxy.rlwy.net'
#     DB_PORT = 41697
#     DB_USER = 'root'
#     DB_PASSWORD = 'zKvJnyPqfGLmaRiZqvqMRCePODgILIqr'
#     DB_NAME = 'ReservasDeCanchas'


# class SecretKey():
#     JWT_SECRET_KEY = 'hmeraSecretKey'

# class Host():
#     URL_APP = 'http://127.0.0.1:3007'

import pymysql

class Config:
    """Configuración general de la aplicación."""
    # Configuración de la base de datos
    DB_HOST = 'junction.proxy.rlwy.net'  # Dirección del servidor de la base de datos
    DB_PORT = 41697                    # Puerto del servidor de la base de datos
    DB_USER = 'root'                    # Usuario de la base de datos
    DB_PASSWORD = 'zKvJnyPqfGLmaRiZqvqMRCePODgILIqr'  # Contraseña de la base de datos
    DB_NAME = 'ReservasDeCanchas'       # Nombre de la base de datos

class SecretKey():
    # Clave secreta para JWT
    JWT_SECRET_KEY = 'hmeraSecretKey'

class Host():
    # URL de la aplicación
    URL_APP = 'http://127.0.0.1:3007'


def obtener_conexion():
    """Crea y devuelve una conexión a la base de datos MySQL."""
    try:
        conexion = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor  # Devuelve los resultados como diccionarios
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
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SHOW TABLES;")
                tablas = cursor.fetchall()
                print("Tablas en la base de datos:")
                for tabla in tablas:
                    print(tabla)
        finally:
            conexion.close()

    
