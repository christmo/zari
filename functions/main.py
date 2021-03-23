from entities.df_text import DFText
import json
from typing import Text
from telegram import impl as telegram
from general import impl as general

def respuesta(message):
    response = {}
    response["fulfillmentMessages"] = DFText(message).toText()
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

    return respuesta(text)
