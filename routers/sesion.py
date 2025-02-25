from flask import Blueprint, request, jsonify
from models.Sesion import Sesion
import json
import jwt #pyjwt
import datetime
from config import SecretKey

#Crear un módulo para gestionar los endpoints relacionados a la sesión del usuario
ws_sesion = Blueprint('ws_sesion', __name__)

#Crear un endpoint para el inicio de sesión
@ws_sesion.route('/usuario/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if {'correo', 'contraseña'} - set(request.form.keys()): #Validar que el usuario envíe los parámetros requeridos
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'}), 400 #Bad Request
        
        #Leer los parámetros email y clave
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        #Instanciar un objeto de la clase Sesion
        obj = Sesion(correo, contraseña)

        #Ejecutar el método iniciar sesión
        resultadoJSONString = obj.iniciarSesion()

        #Convertir el JSON string en JSON Object
        resultadoJSONObject = json.loads(resultadoJSONString)

        #Validar los datos del resultado enviado por el método iniciar sesión
        if resultadoJSONObject['status'] == True:
            #Almacenar el ID del usuario en una variable para enviarlo en el token
            id_usuario = resultadoJSONObject['data']['id_usuario']

            #Generar y otorgar el token al usuario que ha iniciado sesión satisfactoriamente
            token = jwt.encode({'id_usuario': id_usuario, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60)}, SecretKey.JWT_SECRET_KEY)

            #Incorporar el token en los datos de la sesión del usuario
            resultadoJSONObject['data']['token'] = token

            #Actualizar el token del usuario en la BD
            resultadoActualizarTokenJSONObject = json.loads(obj.actualizarToken(token, id_usuario))
            if resultadoActualizarTokenJSONObject['status'] == False: #Ocurrió un error al actualizar el token
                 return jsonify(resultadoActualizarTokenJSONObject), 500 #Internal Server Error

            #Imprimir la respuesta del servicio web
            return jsonify(resultadoJSONObject), 200 #ok
        else: #Credenciales fueron incorrectas o el estado del usuario es inactivo
            #Imprimir la respuesta del servicio web
            return jsonify(resultadoJSONObject), 401 #Unauthorized

@ws_sesion.route('/usuario/firebaseToken/actualizar', methods=['POST'])
def actualizarFirebaseToken():
    if request.method == 'POST':
        if {'id_usuario', 'firebase_token'} - set(request.form.keys()): #Validar que el usuario envíe los parámetros requeridos
            return jsonify({'status': False, 'data':None, 'message': 'Faltan parámetros'}), 400 #Bad Request
        
        #Leer los parámetros email y clave
        id_usuario = request.form['id_usuario']
        firebase_token = request.form['firebase_token']

        #Instanciar un objeto de la clase Sesion
        obj = Sesion(id_usuario, firebase_token)

        #Ejecutar el método iniciar sesión
        resultadoJSONString = obj.actualizarFirebaseToken(firebase_token, id_usuario)

        #Convertir el JSON string en JSON Object
        resultadoJSONObject = json.loads(resultadoJSONString)

        #Validar los datos del resultado enviado por el método iniciar sesión
        if resultadoJSONObject['status'] == True:
            return jsonify(resultadoJSONObject), 200 #ok
        else: #Credenciales fueron incorrectas o el estado del usuario es inactivo
            #Imprimir la respuesta del servicio web
            return jsonify(resultadoJSONObject), 401 #Unauthorized
        