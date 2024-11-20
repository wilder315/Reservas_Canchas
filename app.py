from flask import Flask
from routers.router_main import router_main
from routers.usuario import ws_usuario
from routers.sesion import ws_sesion
from routers.pago import ws_pagos

app = Flask(__name__)
app.debug = False
app.secret_key = 'super-secret'

app.register_blueprint(router_main)
app.register_blueprint(ws_usuario)
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_pagos)



#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
