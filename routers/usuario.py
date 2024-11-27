from flask import Blueprint, request, jsonify
from models.Usuario import Usuario
import json
import validarToken as vt  # Asume que tienes un validador de token

# Crear un módulo para gestionar los endpoints relacionados con usuario
ws_usuario = Blueprint('ws_usuario', __name__)

# Crear un endpoint para registrar usuarios
@ws_usuario.route('/usuario/registrar', methods=['POST'])
# @vt.validar
def registrar_usuario():
    if request.method == 'POST':
        # Validar los parámetros de entrada
        # campos_requeridos = {'nombre', 'apellido', 'correo', 'contraseña', 'tipo_usuario'}
        campos_requeridos = {'nombre', 'apellido', 'correo', 'contraseña'}
        if campos_requeridos - set(request.form.keys()):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400  # Bad Request

        # Leer los parámetros de entrada
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        # tipo_usuario = request.form['tipo_usuario']
        # ubicacion_latitud = request.form.get('ubicacion_latitud')  # Opcional
        # ubicacion_longitud = request.form.get('ubicacion_longitud')  # Opcional
        # foto_perfil = request.form.get('foto_perfil')  # Opcional

        # Instanciar un objeto de la clase Usuario
        obj = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=contraseña,
            # tipo_usuario=tipo_usuario,
            # ubicacion_latitud=ubicacion_latitud,
            # ubicacion_longitud=ubicacion_longitud,
            # foto_perfil=foto_perfil
        )

        # Ejecutar el método registrar
        resultadoJSONUsuario = json.loads(obj.registrar())

        # Mostrar el resultado
        if resultadoJSONUsuario['status']:
            return jsonify(resultadoJSONUsuario), 200  # OK
        else:
            return jsonify(resultadoJSONUsuario), 500  # Error
        

    
@ws_usuario.route('/usuarioMovil/registrar', methods=['POST'])
# @vt.validar
def registrar_usuarioMovil():
    if request.method == 'POST':
        # Validar los parámetros de entrada
        # campos_requeridos = {'nombre', 'apellido', 'correo', 'contraseña', 'tipo_usuario'}
        campos_requeridos = {'nombre', 'apellido', 'correo', 'contraseña','latitud', 'longitud'}
        if campos_requeridos - set(request.form.keys()):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan parámetros'}), 400  # Bad Request

        # Leer los parámetros de entrada
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        tipo_usuario = request.form['tipo_usuario']
        ubicacion_latitud = request.form['ubicacion_latitud']  # Opcional
        ubicacion_longitud = request.form['ubicacion_longitud']  # Opcional

        # Instanciar un objeto de la clase Usuario
        obj = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña=contraseña,
            tipo_usuario=tipo_usuario,
            ubicacion_latitud=ubicacion_latitud,
            ubicacion_longitud=ubicacion_longitud,
            # foto_perfil=foto_perfil
        )

        # Ejecutar el método registrar
        resultadoJSONUsuario = json.loads(obj.registrarUsuarioMovil())

        # Mostrar el resultado
        if resultadoJSONUsuario['status']:
            return jsonify(resultadoJSONUsuario), 200  # OK
        else:
            return jsonify(resultadoJSONUsuario), 500  # Error
