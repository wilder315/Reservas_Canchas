from flask import Flask


app = Flask(__name__)




@app.route('/')
def home():
    return 'Servicios web en ejecución'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
