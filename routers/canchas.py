from flask import Blueprint, render_template, request, jsonify
from controladores.controlador_cancha import *

canchas = Blueprint('canchas', __name__)

# Página principal de gestión de canchas
@canchas.route("/gestionar_cancha", methods=["GET"])
def gestionar_cancha():
    try:
        canchas = obtener_canchas()
        establecimientos = obtener_establecimientos()
        return render_template("cancha/gestionar_cancha.html", canchas=canchas, establecimientos=establecimientos)
    except Exception as e:
        return jsonify(success=False, message="Error al cargar la página: " + str(e))

# Insertar una nueva cancha
@canchas.route("/insertar_cancha", methods=["POST"])
def insertar_cancha():
    try:
        id_establecimiento = request.form.get("id_establecimiento")
        tipo_cancha = request.form.get("tipo_cancha")
        precio = request.form.get("precio")
        estado = request.form.get("estado")

        if not all([id_establecimiento, tipo_cancha, precio, estado]):
            return jsonify(success=False, message="Todos los campos son obligatorios"), 400

        insertar_cancha(id_establecimiento, tipo_cancha, precio, estado)
        return jsonify(success=True, message="Cancha registrada exitosamente")
    except Exception as e:
        print(f"Error al insertar cancha: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar la cancha: {str(e)}"), 500

# Editar una cancha
@canchas.route("/procesar_actualizar_cancha", methods=["POST"])
def actualizar_cancha():
    try:
        id = request.form.get("id")
        id_establecimiento = request.form.get("id_establecimiento")
        tipo_cancha = request.form.get("tipo_cancha")
        precio = request.form.get("precio")
        estado = request.form.get("estado")

        if not all([id, id_establecimiento, tipo_cancha, precio, estado]):
            return jsonify(success=False, message="Todos los campos son obligatorios"), 400

        actualizar_cancha_bd(id, id_establecimiento, tipo_cancha, precio, estado)
        return jsonify(success=True, message="Cancha actualizada exitosamente")
    except Exception as e:
        print(f"Error al actualizar cancha: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar la cancha: {str(e)}"), 500

# Eliminar una cancha
@canchas.route("/eliminar_cancha", methods=["POST"])
def eliminar_cancha():
    try:
        data = request.get_json()
        id = data.get("id")

        if not id:
            return jsonify(success=False, message="ID de la cancha no proporcionado"), 400

        eliminar_cancha_bd(id)
        return jsonify(success=True, message="Cancha eliminada exitosamente")
    except Exception as e:
        print(f"Error al eliminar cancha: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar la eliminación: {str(e)}"), 500
