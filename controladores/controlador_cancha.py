from bd import obtener_conexion

def insertar_cancha(id_establecimiento, tipo_cancha, precio, estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COALESCE(MAX(id_cancha) + 1, 1) FROM canchas")
            siguiente_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO canchas (id_cancha, id_establecimiento, tipo_cancha, precio, estado) 
                VALUES (%s, %s, %s, %s, %s)
            """, (siguiente_id, id_establecimiento, tipo_cancha, precio, estado))
        conexion.commit()
        return siguiente_id
    except Exception as e:
        print(f"Error al insertar cancha: {e}")
        conexion.rollback()
        return None
    finally:
        conexion.close()

def actualizar_cancha(id, id_establecimiento, tipo_cancha, precio, estado):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE canchas 
                SET id_establecimiento = %s, tipo_cancha = %s, precio = %s, estado = %s 
                WHERE id_cancha = %s
            """, (id_establecimiento, tipo_cancha, precio, estado, id))
        conexion.commit()
    except Exception as e:
        print(f"Error al actualizar cancha: {e}")
        conexion.rollback()
        raise
    finally:
        conexion.close()

def eliminar_cancha(id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM canchas WHERE id_cancha = %s", (id,))
        conexion.commit()
    except Exception as e:
        print(f"Error al eliminar cancha: {e}")
        conexion.rollback()
    finally:
        conexion.close()

def obtener_canchas():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT c.id_cancha, e.nombre AS establecimiento, c.tipo_cancha, c.precio, 
                       CASE WHEN c.estado = 'activo' THEN 'Activo' ELSE 'Inactivo' END AS estado
                FROM canchas c
                JOIN establecimientos e ON c.id_establecimiento = e.id_establecimiento
            """)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener canchas: {e}")
        return []
    finally:
        conexion.close()
