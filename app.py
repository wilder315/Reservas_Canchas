from flask import Flask, render_template, request, redirect, url_for
from routers.router_main import router_main
from routers.usuario import ws_usuario
from routers.sesion import ws_sesion
from routers.pago import ws_pagos
from routers.propietarios import propietarios
from routers.establecimientos import establecimientos
from routers.canchas import canchas
from routers.reservas import ws_reservas

app = Flask(__name__)
app.debug = False
app.secret_key = 'super-secret'

# Ruta para la página de inicio de sesión
@app.route('/')
def raiz():
    return render_template('index.html')

app.register_blueprint(router_main)
app.register_blueprint(ws_usuario)
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_pagos)
app.register_blueprint(ws_reservas)


# Registrar Blueprints
app.register_blueprint(propietarios, url_prefix='/propietarios')
app.register_blueprint(establecimientos)
app.register_blueprint(canchas, url_prefix='/canchas')




# Ruta para renderizar home.html
@app.route('/')
def home():
    return render_template('index.html')

# Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
