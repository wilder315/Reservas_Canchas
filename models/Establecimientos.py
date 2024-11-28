from conexionBD import Conexion as db
import json
from util import CustomJsonEncoder

class Establecimiento():
    def __init__(self, id_propietario=None, nombre=None, descripcion=None, ubicacion_latitud=None, ubicacion_longitud=None, horario_apertura=None, horario_cierre=None):
        self.id_propietario = id_propietario
        self.nombre = nombre
        self.descripcion = descripcion
        self.ubicacion_latitud = ubicacion_latitud
        self.ubicacion_longitud = ubicacion_longitud
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre

    def catalogo(self):
        #Abrir conexión a la BD
        con = db().open

        #Crear un cursor
        cursor = con.cursor()

        #Preparar la sentencia SQL
        sql = """
            SELECT
                id_establecimiento, nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre
            FROM
                Establecimientos
            ORDER BY
                id_establecimiento
        """

        try:
            #Ejecutar la sentencia
            cursor.execute(sql)

            #Recuperar los datos de la consulta
            datos = cursor.fetchall()

            #Retornar un mensaje con los datos de los productos
            if datos:
                return json.dumps({'status': True, 'data': datos, 'message': "Catálogo de establecimientos"}, cls=CustomJsonEncoder)
            else:
                return json.dumps({'status': True, 'data': None, 'message': "Sin registros"})
        
        except con.Error as error:
            #Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})

        finally:
            cursor.close()
            con.close()