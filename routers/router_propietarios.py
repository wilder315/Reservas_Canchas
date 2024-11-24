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