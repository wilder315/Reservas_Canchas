import hashlib
from bd import obtener_conexion

# REGISTRAR UN NUEVO PROPIETARIO
def registrar_propietario(nombre, correo, contraseña, apellido):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            # Registro del nuevo propietario
            cursor.execute("""
                INSERT INTO Usuarios(nombre, correo, contraseña, ubicacion_latitud, ubicacion_longitud, foto_perfil, tipo_usuario, apellido, estado_usuario)
                VALUES(%s, %s, %s, null, null, null, 'PROPIETARIO', %s, 0)
            """, (nombre, correo, contraseña, apellido))

        # Confirmar la transaccion
        conexion.commit()

    except Exception as e:
        print(f"Error al registrar el propietario: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def login_propietario(correo, contraseña):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("select nombre, apellido from Usuarios where correo = %s and contraseña = %s and tipo_usuario='propietario'", 
            (correo, contraseña))

            propietario = cursor.fetchall()
        
        return propietario

    except Exception as e:
        print(f"Error al iniciar sesion: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def validar_estado_usuario_propietario(id_usuario):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("select estado_usuario from Usuarios where id_usuario = %s and tipo_usuario='propietario'",
            (id_usuario))

            estado_usuario =cursor.fetchone()

        return estado_usuario
    
    except Exception as e:
        print(f"Error al validad el estado del usuario: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def obtener_id_propietario(correo, contraseña):
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("select id_usuario from Usuarios where correo = %s and contraseña = %s and tipo_usuario='propietario'",
            (correo, contraseña))

            id_usuario = cursor.fetchone()

        return id_usuario
    except Exception as e:
        print(f"Error al obtener el id del propietario: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()