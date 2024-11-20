from conexionBD import Conexion as db
import json
import os
import base64

class Pago:
    def __init__(self, id=None, id_reserva=None, metodo_pago=None, comprobante_foto=None, fecha_pago=None):
        self.id = id
        self.id_reserva = id_reserva
        self.metodo_pago = metodo_pago
        self.comprobante_foto = comprobante_foto
        self.fecha_pago = fecha_pago

    def registrar(self):
        """
        Registra un nuevo pago en la base de datos, junto con la foto del comprobante.
        """
        con = db().open
        cursor = con.cursor()
        try:
            # Guardar el comprobante como archivo en el sistema
            comprobante_path = f'static/comprobantes/{self.id_reserva}.jpg'
            os.makedirs(os.path.dirname(comprobante_path), exist_ok=True)
            with open(comprobante_path, 'wb') as f:
                f.write(base64.b64decode(self.comprobante_foto))

            # Insertar el registro en la base de datos
            sql = """
                INSERT INTO Pagos (id_reserva, metodo_pago, comprobante_foto)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, [self.id_reserva, self.metodo_pago, comprobante_path])
            con.commit()
            return json.dumps({'status': True, 'message': 'Pago registrado correctamente'})
        except Exception as e:
            con.rollback()
            return json.dumps({'status': False, 'message': str(e)})
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def obtener_por_reserva(id_reserva):
        """
        Obtiene todos los pagos asociados a una reserva específica.
        """
        con = db().open
        cursor = con.cursor()
        try:
            sql = """
                SELECT id, id_reserva, metodo_pago, comprobante_foto, fecha_pago
                FROM Pagos
                WHERE id_reserva = %s
            """
            cursor.execute(sql, [id_reserva])
            pagos = cursor.fetchall()
            return json.dumps({'status': True, 'data': pagos, 'message': 'Pagos obtenidos correctamente'})
        except Exception as e:
            return json.dumps({'status': False, 'message': str(e)})
        finally:
            cursor.close()
            con.close()
