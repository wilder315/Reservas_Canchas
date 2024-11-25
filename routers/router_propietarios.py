from flask import jsonify, render_template, request, redirect, url_for, flash
from controladores.controlador_propietarios import *
import hashlib

from flask import Flask
app = Flask(__name__)


def encriptar_contraseña(contraseña):
    """Encripta una contraseña usando SHA-256."""
    sha_signature = hashlib.sha256(contraseña.encode()).hexdigest()
    return sha_signature

# REGISTRAR AL NUEVO PROPIETARIO
@app.route("/registrar_propietario", methods=["POST"])
def registrar_propietario():
    try:
        #Capturar los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")

        if not contraseña:
            return jsonify(success= False, message="Ingrese una contraseña"), 400
        
        #Encriptar contraseña
        contraseña_encriptada = encriptar_contraseña(contraseña)

        # Insertar los datos del propietario a la base de datos
        registrar_propietario(nombre, correo, contraseña, apellido)
        return jsonify(success=True)
    except Exception as e:
        print(f"Error al registrar el propietario: {str(e)}")
        return jsonify(success=False, message="Error en la transaccion registrar propietario: " + str(e)), 500

# INICIO SESION
@app.route("/login_propietario", methods=["POST"])
def login():
    try:
        #Capturar los datos del formulario
        correo = request.form.get("correo")
        contraseña = request.form.get("contraseña")

        if not correo:
            return jsonify(success=False, message="Ingrese un correo"), 400
        
        if not contraseña:
            return jsonify(success=False, message="Ingrese una contraseña "), 400
        
        # Obtener id del propietario
        id_propietario = obtener_id_propietario(correo, contraseña)
        if not id_propietario:
            return jsonify(success=False, message="Credenciales incorrectas"), 401
        
        # obtener el estado propietario
        estado_usuario = validar_estado_usuario_propietario(id_propietario)

        # Validar el estado del propietario
        if estado_usuario == 0:
            return jsonify(success=False, message="Su usuario esta inactivado. Contacte al administrador!"), 400
        
        propietario = login_propietario(correo, contraseña)
        if not propietario:
            return jsonify(success=False, message="Credenciales incorrectas"), 401

        # Extraer nombre y apellido
        nombre = propietario['nombre']
        apellidos = propietario['apellido']

        return jsonify(success=True, message=f"Bienvenido al sistema {nombre} {apellidos}"), 200


    except Exception as e:
        print(f"Error al iniciar sesion: {str(e)}")
        return jsonify(success=False, message="Error al realizar la transaccion " + str(e)), 500