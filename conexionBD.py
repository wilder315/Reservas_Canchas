from config import Config
import pymysql as dbc
import pymysql.cursors


class Conexion():
    def __init__(self):
        self.dblink = dbc.connect(host=Config.DB_HOST, user=Config.DB_USER, passwd=Config.DB_PASSWORD, db=Config.DB_NAME, port=Config.DB_PORT, cursorclass=dbc.cursors.DictCursor)
        
    @property
    def open(self):
        return self.dblink
