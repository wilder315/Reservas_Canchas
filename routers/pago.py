from flask import Blueprint, request, jsonify
from models.Pago import Pago
import json

ws_pagos = Blueprint('ws_pagos', __name__)

# Endpoint para registrar un pago
@ws_pagos.route('/pago/registrar', methods=['POST'])
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

# Endpoint para obtener los pagos asociados a una reserva
@ws_pagos.route('/pago/<int:id_reserva>', methods=['GET'])
def obtener_pagos(id_reserva):
    resultado = Pago.obtener_por_reserva(id_reserva)
    return jsonify(json.loads(resultado))
