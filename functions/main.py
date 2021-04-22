from entities.producto import Producto
from entities.usuario import Usuario
from entities.carrito import Carrito
from database.persitencia import save_shopping_car
from entities.df_text import DFText
import json
from typing import Text
from telegram import impl as telegram
from general import impl as general


def respuesta(message):
    response = {}
    response["fulfillmentMessages"] = DFText().toText(message)
    return json.dumps(response)


def zari_webhook(request):
    """
        Entrada del Webhook de Dialogflow, en este se van a enviar los parametros
        a las otras funciones para realizar las acciones de respuesta.
    """
    text = ""
    request_json = request.get_json()
    print(request_json)
    if request_json != None and request_json["queryResult"] != None and request_json["originalDetectIntentRequest"] != None:
        #text = request_json["queryResult"]["queryText"]
        source = request_json["originalDetectIntentRequest"]["source"]
        if source == "telegram":
            return telegram.gateway(request_json)
        else:
            return general.gateway(request_json)
    else:
        text = "Respuesta sin procesar"
        #user = Usuario("christmo")
        #user.id(3)
        #prod = Producto("pantalones", "M", "azul", 1)
        #prod.costo = 62.7
        #prod.codigo = 100
        #save_shopping_car(user, prod)

    return respuesta(text)
