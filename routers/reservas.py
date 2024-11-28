from flask import Blueprint, request, jsonify
from models.Reservas import Reserva
from models.Pago import Pago
import json

ws_reservas = Blueprint('ws_reservas', __name__)

# Disponibilidad de canchas
@ws_reservas.route('/reserva/disponibilidad', methods=['POST'])
def disponibilidad():
    if {'fecha_reserva', 'hora_inicio', 'hora_fin'} - set(request.json.keys()):
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    reserva = Reserva()
    resultado = reserva.disponibilidad(
        fecha_reserva=request.json['fecha_reserva'],
        hora_inicio=request.json['hora_inicio'],
        hora_fin=request.json['hora_fin']
    )
    return jsonify(json.loads(resultado))

# Registrar una reserva
# Registrar una reserva
@ws_reservas.route('/reserva/registrar', methods=['POST'])
def registrar_reserva():
    # Verificamos que los parámetros estén en el form-data
    if {'id_usuario', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'id_cancha'} - set(request.form.keys()):
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    # Obtener los valores del form-data
    id_usuario = request.form['id_usuario']
    fecha_reserva = request.form['fecha_reserva']
    hora_inicio = request.form['hora_inicio']
    hora_fin = request.form['hora_fin']
    id_cancha = request.form['id_cancha']  # Ahora también se toma el id_cancha

    # Crear la reserva
    reserva = Reserva(
        id_usuario=id_usuario,
        fecha_reserva=fecha_reserva,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        id_cancha=id_cancha  # Asegúrate de pasar el id_cancha al crear la instancia
    )

    # Llamar al método para registrar la reserva
    resultado = reserva.registrar()

    # Retornar la respuesta
    return jsonify(json.loads(resultado))


# Registrar un pago
@ws_reservas.route('/pago/registrar', methods=['POST'])
def registrar_pago():
    if {'id_reserva', 'metodo_pago', 'comprobante_foto'} - set(request.json.keys()):
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    pago = Pago(
        id_reserva=request.json['id_reserva'],
        metodo_pago=request.json['metodo_pago'],
        comprobante_foto=request.json['comprobante_foto']
    )
    resultado = pago.registrar()
    return jsonify(json.loads(resultado))

# Historial de reservas
@ws_reservas.route('/reserva/historial/<int:id_usuario>', methods=['GET'])
def historial_reservas(id_usuario):
    reserva = Reserva()
    resultado = reserva.historial(id_usuario=id_usuario)
    return jsonify(json.loads(resultado))

