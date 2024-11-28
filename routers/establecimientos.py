from flask import Blueprint, render_template, request, jsonify
from controladores.controlador_establecimiento import *
import validarToken as vt
from models.Establecimientos import Establecimiento
import json

establecimientos = Blueprint('establecimientos', __name__)

# Página principal de gestión de establecimientos
@establecimientos.route("/gestionar_establecimiento", methods=["GET"])
def gestionar_establecimiento():
    try:
        establecimientos = obtener_establecimientos()
        return render_template("propietario/gestionar_establecimientos.html", establecimientos=establecimientos)
    except Exception as e:
        return jsonify(success=False, message="Error al cargar la página: " + str(e))

# Insertar un nuevo establecimiento
@establecimientos.route("/insertar_establecimiento", methods=["POST"])
def insertar_establecimiento():
    try:
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        ubicacion_latitud = request.form.get("ubicacion_latitud")
        ubicacion_longitud = request.form.get("ubicacion_longitud")
        horario_apertura = request.form.get("horario_apertura")
        horario_cierre = request.form.get("horario_cierre")

        if not all([nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre]):
            return jsonify(success=False, message="Todos los campos son obligatorios"), 400

        insertar_establecimiento(nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre)
        return jsonify(success=True, message="Establecimiento registrado exitosamente")
    except Exception as e:
        print(f"Error al insertar establecimiento: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar el establecimiento: {str(e)}"), 500

# Editar un establecimiento
@establecimientos.route("/actualizar_establecimiento", methods=["POST"])
def actualizar_establecimiento():
    try:
        id = request.form.get("id")
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        ubicacion_latitud = request.form.get("ubicacion_latitud")
        ubicacion_longitud = request.form.get("ubicacion_longitud")
        horario_apertura = request.form.get("horario_apertura")
        horario_cierre = request.form.get("horario_cierre")

        if not all([id, nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre]):
            return jsonify(success=False, message="Todos los campos son obligatorios"), 400

        actualizar_establecimiento(id, nombre, descripcion, ubicacion_latitud, ubicacion_longitud, horario_apertura, horario_cierre)
        return jsonify(success=True, message="Establecimiento actualizado exitosamente")
    except Exception as e:
        print(f"Error al actualizar establecimiento: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar el establecimiento: {str(e)}"), 500

# Eliminar un establecimiento
@establecimientos.route("/eliminar_establecimiento", methods=["POST"])
def eliminar_establecimiento():
    try:
        data = request.get_json()
        id = data.get("id")

        if not id:
            return jsonify(success=False, message="ID de establecimiento no proporcionado"), 400

        eliminar_establecimiento(id)
        return jsonify(success=True, message="Establecimiento eliminado exitosamente")
    except Exception as e:
        print(f"Error al eliminar establecimiento: {str(e)}")
        return jsonify(success=False, message=f"Error al procesar la eliminación: {str(e)}"), 500
    

@establecimientos.route('/establecimiento/mapa', methods=['GET'])
@vt.validar
def catalogo():
    if request.method == 'GET':
        
        #Instanciar a la clase establecimiento
        obj = Establecimiento()

        #Ejecutar el método catalogo para traer los datos
        resultadoCatalogoJSONObject = json.loads(obj.catalogo())

        #Imprimir el resultado del servicio web
        if resultadoCatalogoJSONObject['status'] == True:
            return jsonify(resultadoCatalogoJSONObject), 200 #ok
        else:
            return jsonify(resultadoCatalogoJSONObject), 500 #Error
