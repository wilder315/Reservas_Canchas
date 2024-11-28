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
@ws_reservas.route('/reserva/registrar', methods=['POST'])
def registrar_reserva():
    if {'id_usuario', 'id_cancha', 'fecha_reserva', 'hora_inicio', 'hora_fin'} - set(request.json.keys()):
        return jsonify({'status': False, 'message': 'Faltan parámetros'}), 400

    reserva = Reserva(
        id_usuario=request.json['id_usuario'],
        id_cancha=request.json['id_cancha'],
        fecha_reserva=request.json['fecha_reserva'],
        hora_inicio=request.json['hora_inicio'],
        hora_fin=request.json['hora_fin']
    )
    resultado = reserva.registrar()
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

