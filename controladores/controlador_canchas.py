import hashlib
from bd import obtener_conexion

def insertar_cancha():
    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            # Insertar nueva cancha
            cursor.execute("""
                INSERT INTO canchas()
                VALUES(%s)
            """)
        
        # Confirmar la transaccion
        conexion.commit()
    except Exception as e:
        print(f"Error al registrar la cancha: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()