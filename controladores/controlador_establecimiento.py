import secrets
from bd import obtener_conexion

def generar_token():
    """Genera un token único para los establecimientos."""
    return secrets.token_hex(10)

def insertar_establecimiento(id_propietario,nombre, descripcion, latitud, longitud, apertura, cierre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Generar el siguiente ID automáticamente
            cursor.execute("SELECT COALESCE(MAX(id_establecimiento) + 1, 1) FROM Establecimientos")
            siguiente_id = cursor.fetchone()[0]

            # Insertar un nuevo establecimiento
            cursor.execute("""
                INSERT INTO Establecimientos (id_establecimiento, id_propietario,nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre) 
                VALUES (%s, %s, %s,%s, %s, %s, %s, %s)
            """, (siguiente_id,id_propietario, nombre, descripcion, latitud, longitud, apertura, cierre))
        
        conexion.commit()
        return siguiente_id
    except Exception as e:
        print(f"Error al insertar establecimiento: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def actualizar_establecimiento(id, id_propietario,nombre, descripcion, latitud, longitud, apertura, cierre):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE Establecimientos 
                SET id_propietario= %s, nombre = %s, descripcion = %s, ubicacion_latitud = %s, ubicacion_longitud = %s, horario_apertura = %s, horario_cierre = %s 
                WHERE id_establecimiento = %s
            """, ( id_propietario,nombre,descripcion, latitud, longitud, apertura, cierre, id))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar establecimiento: {e}")
        conexion.rollback()
        raise
    finally:
        conexion.close()

def eliminar_establecimiento(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM Establecimientos WHERE id_establecimiento = %s", (id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar establecimiento: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_establecimientos():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT id_establecimiento, nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre 
                FROM Establecimientos
            """)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener establecimientos: {e}")
        return []
    finally:
        conexion.close()
