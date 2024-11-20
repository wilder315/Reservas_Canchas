from flask import Blueprint, render_template, request, redirect, jsonify, make_response, session

import hashlib
import random
import os
from werkzeug.utils import secure_filename
from bd import obtener_conexion
import time

login_attempts = {}
router_main = Blueprint('router_main', __name__)

# Login


# Principal

@router_main.route("/index")
def index():
    return render_template("/dashboard/index.html")