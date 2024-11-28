#Clase MD5Hash
import hashlib

class MD5Hash():
    def md5_password(password):
        pwdBytes = password.encode(encoding='UTF-8', errors='strict')
        h = hashlib.md5()
        h.update(pwdBytes)
        return h.hexdigest()



#Clase CustomJsonEncoder
import json
from decimal import Decimal
import datetime

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        # Serializar objetos Decimal como float
        if isinstance(obj, Decimal):
            return float(obj)

        # Serializar objetos datetime.date como string en formato ISO
        if isinstance(obj, datetime.date):
            return obj.isoformat()

        # Serializar objetos timedelta como el número total de segundos
        if isinstance(obj, datetime.timedelta):
            return str(obj)  # O puedes devolver obj.total_seconds() para obtener un valor numérico

        # Si no se puede serializar, llamar al método default de la clase base
        return super(CustomJsonEncoder, self).default(obj)