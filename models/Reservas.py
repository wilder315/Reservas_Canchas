from conexionBD import Conexion as db
import json

class Reserva:
    def __init__(self, id=None, id_usuario=None, id_cancha=None, fecha_reserva=None, hora_inicio=None, hora_fin=None, estado='pendiente'):
        self.id = id
        self.id_usuario = id_usuario
        self.id_cancha = id_cancha
        self.fecha_reserva = fecha_reserva
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado

    def disponibilidad(self, fecha_reserva, hora_inicio, hora_fin):
        con = db().open
        cursor = con.cursor()
        try:
            sql = """
                SELECT id, nombre, estado
                FROM Canchas
                WHERE id NOT IN (
                    SELECT id_cancha
                    FROM Reservas
                    WHERE fecha_reserva = %s
                      AND (hora_inicio < %s AND hora_fin > %s)
                ) AND estado = 'disponible'
            """
            cursor.execute(sql, [fecha_reserva, hora_fin, hora_inicio])
            canchas = cursor.fetchall()
            return json.dumps({'status': True, 'data': canchas, 'message': 'Canchas disponibles'})
        except Exception as e:
            return json.dumps({'status': False, 'message': str(e)})
        finally:
            cursor.close()
            con.close()

    def registrar(self):
        con = db().open
        cursor = con.cursor()
        try:
            sql = """
                INSERT INTO Reservas (id_usuario, id_cancha, fecha_reserva, hora_inicio, hora_fin, estado)
                VALUES (%s, %s, %s, %s, %s, 'pendiente')
            """
            cursor.execute(sql, [self.id_usuario, self.id_cancha, self.fecha_reserva, self.hora_inicio, self.hora_fin])
            con.commit()
            return json.dumps({'status': True, 'message': 'Reserva registrada correctamente'})
        except Exception as e:
            con.rollback()
            return json.dumps({'status': False, 'message': str(e)})
        finally:
            cursor.close()
            con.close()

    def historial(self, id_usuario):
        con = db().open
        cursor = con.cursor()
        try:
            sql = """
                SELECT r.id, r.fecha_reserva, r.hora_inicio, r.hora_fin, c.nombre AS cancha, r.estado
                FROM Reservas r
                INNER JOIN Canchas c ON r.id_cancha = c.id
                WHERE r.id_usuario = %s
                ORDER BY r.fecha_reserva DESC
            """
            cursor.execute(sql, [id_usuario])
            reservas = cursor.fetchall()
            return json.dumps({'status': True, 'data': reservas, 'message': 'Historial de reservas obtenido'})
        except Exception as e:
            return json.dumps({'status': False, 'message': str(e)})
        finally:
            cursor.close()
            con.close()
