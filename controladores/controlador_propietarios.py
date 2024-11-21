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
            """), (nombre, correo, contraseña, apellido)

        # Confirmar la transaccion
        conexion.commit()

    except Exception as e:
        print(f"Error al registrar el propietario: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()