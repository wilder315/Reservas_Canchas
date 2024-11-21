import hashlib
from bd import obtener_conexion

def registrar_propietario():
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            # Registro del nuevo propietario
            cursor.execute("""
                INSERT INTO propietarios(nombre, email, clave)
                VALUES(%s, %s, %s)
            """)

        # Confirmar la transaccion
        conexion.commit()

    except Exception as e:
        print(f"Error al registrar el propietario: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()