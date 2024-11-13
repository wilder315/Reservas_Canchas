from flask import Flask
from routers.router_main import router_main

app = Flask(__name__)
app.debug = False
app.secret_key = 'super-secret'

app.register_blueprint(router_main)



#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
