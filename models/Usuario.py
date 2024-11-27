from conexionBD import Conexion as db
import json
import base64
from util import CustomJsonEncoder
import os

class Usuario():
    def __init__(self, id=None, nombre=None, apellido=None, correo=None, contraseña=None, tipo_usuario=None, ubicacion_latitud=None, ubicacion_longitud=None, foto_perfil=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contraseña = contraseña
        self.tipo_usuario = tipo_usuario
        self.ubicacion_latitud = ubicacion_latitud
        self.ubicacion_longitud = ubicacion_longitud
        self.foto_perfil = foto_perfil

    def registrar(self):
        # Abrir conexión a la BD
        con = db().open

        # Crear un cursor para ejecutar la sentencia en la BD
        cursor = con.cursor()

        # Preparar la sentencia para insertar un nuevo usuario
        sql = """
            INSERT INTO Usuarios (nombre, apellido, correo, contraseña, tipo_usuario, ubicacion_latitud, ubicacion_longitud, foto_perfil, estado_usuario)
            VALUES (%s, %s, %s, %s, 'usuario', null, null, %s, 1)
        """

        try:
            # Inicio de la transacción
            con.autocommit = False

            # Cifrar la contraseña antes de almacenarla
            contraseña_cifrada = base64.b64encode(self.contraseña.encode()).decode()

            # Ejecutar la sentencia para agregar un nuevo usuario
            # cursor.execute(sql, [self.nombre, self.apellido, self.correo, contraseña_cifrada, self.tipo_usuario, self.ubicacion_latitud, self.ubicacion_longitud, None])
            cursor.execute(sql, [self.nombre, self.apellido, self.correo, contraseña_cifrada, None])

            # Obtener el ID del usuario registrado
            self.id = con.insert_id()

            # Cargar la foto de perfil si está presente
            if self.foto_perfil:
                self.cargarFoto(self.foto_perfil, self.id)

            # Confirmar la transacción
            con.commit()

            # Retornar un mensaje de éxito
            return json.dumps({'status': True, 'data': {'usuario_id': self.id}, 'message': 'Usuario registrado exitosamente'})

        except con.Error as error:
            # Revocar la transacción
            con.rollback()

            # Retornar un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            cursor.close()
            con.close()

    def cargarFoto(self, foto, id):
        # Decodificar la foto de perfil del usuario que viene en BASE64
        foto_bytes = base64.b64decode(foto)

        # Guardar la foto de perfil
        nombre_foto = f"{id}.jpg"
        ruta_foto = os.path.join('static/imgs-perfil', nombre_foto)

        # Crear la carpeta si no existe
        os.makedirs(os.path.dirname(ruta_foto), exist_ok=True)

        with open(ruta_foto, 'wb') as archivo:
            archivo.write(foto_bytes)

    def registrarUsuarioMovil(nombre, apellido, correo, contraseña, ubicacion_latitud, ubicacion_longitud, tipo_usuario, fecha_registro, estado_usuario):
        # Abrir conexión a la base de datos
        con = db().open

        # Crear un cursor para ejecutar la consulta SQL
        cursor = con.cursor()

        # Preparar la sentencia SQL para insertar un nuevo usuario
        sql = """
            INSERT INTO Usuarios (nombre, apellido, correo, contraseña, ubicacion_latitud, ubicacion_longitud, tipo_usuario, fecha_registro, estado_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, 'usuario', CURRENT_TIMESTAMP, 1)
        """
        
        try:
            # Configurar la transacción
            con.autocommit = False  # Indicar que la transacción se confirmará manualmente

            # Ejecutar la consulta SQL
            cursor.execute(sql, [nombre, apellido, correo, contraseña, ubicacion_latitud, ubicacion_longitud, tipo_usuario, fecha_registro, estado_usuario])

            # Confirmar la transacción
            con.commit()

            # Devolver un mensaje de éxito
            return json.dumps({'status': True, 'data': None, 'message': 'Usuario registrado exitosamente'})
        except con.Error as error:
            # Revocar la transacción en caso de error
            con.rollback()

            # Devolver un mensaje de error
            return json.dumps({'status': False, 'data': None, 'message': str(error)})
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            con.close()

