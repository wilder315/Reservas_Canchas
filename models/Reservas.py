from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

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
                SELECT c.id_cancha, e.nombre, c.estado
                FROM Canchas c
                INNER JOIN Establecimientos e
                ON  c.id_establecimiento = e.id_establecimiento
                WHERE c.id_cancha NOT IN (
                    SELECT c.id_cancha
                    FROM Reservas r
                    WHERE r.fecha_reserva = %s
                    AND (r.hora_inicio < %s AND r.hora_fin > %s)
                ) AND c.estado = 'disponible'
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
                SELECT r.id_reserva, r.fecha_reserva, r.hora_inicio, r.hora_fin, c.tipo_cancha, r.estado
                FROM Reservas r
                INNER JOIN DetalleReservas dr ON r.id_reserva = dr.id_reserva
                INNER JOIN Canchas c ON dr.id_cancha = c.id_cancha
                WHERE r.id_usuario = %s
                ORDER BY r.fecha_reserva DESC
            """
            cursor.execute(sql, [id_usuario])
            reservas = cursor.fetchall()

            # Verificamos que haya resultados
            if reservas:
                # Usamos CustomJsonEncoder para serializar correctamente los tipos de datos TIME y DATE
                return json.dumps({'status': True, 'data': reservas, 'message': 'Historial obtenido'}, cls=CustomJsonEncoder)
            else:
                return json.dumps({'status': False, 'message': 'El usuario no ha registrado ninguna reserva'})

        except Exception as e:
            return json.dumps({'status': False, 'message': f'Error: {str(e)}'})
        finally:
            cursor.close()
            con.close()

