from flask import Blueprint, render_template

propietarios = Blueprint('propietarios', __name__, template_folder='../templates/propietario')

@propietarios.route('/homeP')
def homeP():
    return render_template('homeP.html')
