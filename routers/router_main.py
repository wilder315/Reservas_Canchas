from flask import Blueprint, render_template, request, redirect, jsonify, make_response, session

import hashlib
import random
import os
from werkzeug.utils import secure_filename
from bd import obtener_conexion
import time

login_attempts = {}
router_main = Blueprint('router_main', __name__)

# Login

@router_main.route("/")
@router_main.route("/login", methods=["GET", "POST"])
def login():
    return render_template("/dashboard/login.html")

@router_main.route("/procesar_login", methods=["POST"])
def procesar_login():
    try:
        conexion = obtener_conexion()
        if not conexion:
            return jsonify({
                'logeo': False,
                'mensaje': 'El servicio se encuentra inactivo.'
            }), 500

        username = request.json.get('username')
        password = request.json.get('password')
        usuario = controlador_usuario.obtener_usuario_con_tipopersona_por_username(username)
        if username not in login_attempts:
            login_attempts[username] = {'attempts': 0, 'last_attempt_time': 0}
        if login_attempts[username]['attempts'] >= 3 and (time.time() - login_attempts[username]['last_attempt_time']) < 300:
            return jsonify({'mensaje': 'Cuenta bloqueada. Intente de nuevo más tarde.', 'logeo': False})      
        if usuario is None:
            return jsonify({'mensaje': 'El usuario no existe', 'logeo': False})
        elif usuario[2] == "I":
            return jsonify({'mensaje': 'El usuario está inactivo', 'logeo': False})
        else:
            h = hashlib.new("sha256")
            h.update(bytes(password, encoding="utf-8"))
            encpassword = h.hexdigest()

            if encpassword == usuario[3]:
                login_attempts[username] = {'attempts': 0, 'last_attempt_time': 0}
                persona = controlador_usuario.obtener_datos_usuario(usuario[0])
                nombre = persona[0].split()[0]
                apellido = persona[1].split()[0]
                foto = persona[2]
                session['user_id'] = usuario[0]
                return jsonify({
                    'logeo': True,
                    'nombre': nombre,
                    'apellido': apellido,
                    'foto': foto
                })
            else:
                login_attempts[username]['attempts'] += 1
                login_attempts[username]['last_attempt_time'] = time.time()
                return jsonify({'mensaje': 'La contraseña es incorrecta', 'logeo': False})
    except Exception as e:
        return jsonify({'mensaje': f'Error al procesar el login: {str(e)}', 'logeo': False})

# Principal

@router_main.route("/index")
def index():
    return render_template("/dashboard/index.html")