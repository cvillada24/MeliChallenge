from flask import Flask
from flask_cors import CORS 
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson.json_util import dumps
import os #libreria para poder leer el entorno
import requests

load_dotenv() #Traer el archivo con variables de entorno
name_database = os.getenv("DATABASE")
user = os.getenv("ADMIN") #entorno
password = os.getenv("PASSWORD")


try:
    client = MongoClient(f"mongodb+srv://{user}:{password}@cluster0.sdgxli1.mongodb.net/?retryWrites=true&w=majority", ServerSelectionTimeoutMS=5) #conexion bdd - extraido de mongocloud

    db = client.dbuser
    collectionmeli = db.sec #collection
    info = client.server_info()
    print(info)

except ServerSelectionTimeoutError:
    print(f"Conexion no exitosa")

appmeli = Flask(__name__)
cors = CORS(appmeli, resource={r"/*": {"origins": "*"}}) #lsita de acceso a la ruta

@appmeli.route("/insertusers", methods=['POST','GET'])
def adicionar():   
    r = requests.get("https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios")
    data = r.json()

    for informacion in data:

        collectionmeli.insert_one({"id":informacion['id'],"fec_alta":informacion['fec_alta'],"user_name":informacion['user_name'],"codigo_zip":informacion['codigo_zip'],"credit_card_num":informacion['credit_card_num'],"credit_card_ccv":informacion['credit_card_ccv'],"cuenta_numero":informacion['cuenta_numero'],"direccion":informacion['direccion'],"geo_latitud":informacion['geo_latitud'],"geo_longitud":informacion['geo_longitud'],"color_favorito":informacion['color_favorito'],"foto_dni":informacion['foto_dni'],"ip":informacion['ip'],"auto":informacion['auto'],"auto_modelo":informacion['auto_modelo'],"auto_tipo":informacion['auto_tipo'],"auto_color":informacion['auto_color'],"cantidad_compras_realizadas":informacion['cantidad_compras_realizadas'],"avatar":informacion['avatar'],"fec_birthday":informacion['fec_birthday']})

    return dumps({"Process": "insert", "status": 201}), 201

@appmeli.route("/viewdata", methods=['GET'])
def mostrar():
    m =[] #declarar un arreglo "coco" , lista
    #formato = m.json()

    for view in collectionmeli.find({}): #formato json y llamo a collection
        m.append(view)
    return dumps(m), 200



if __name__=='__main__':
    appmeli.run(host='0.0.0.0', port='4000', debug=True)