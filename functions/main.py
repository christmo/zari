import json
from telegram import impl as telegram
from general import impl as general
from database import conexion as pgsql

def respuesta(message):
    text = []
    text.append(message)

    text_wrapper = {}
    text_wrapper["text"] = text

    fullfillment = []
    fullfillment_message = {}
    fullfillment_message["text"] = text_wrapper
    fullfillment.append(fullfillment_message)

    response = {}
    response["fulfillmentMessages"] = fullfillment
    return json.dumps(response)

def db():
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        usuarios = conn.execute(
            "SELECT * FROM usuarios "
        ).fetchall()
        for usuario in usuarios:
            print(usuario)

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
            text = telegram.gateway(request_json)
        else:
            text = general.gateway(request_json)
    else:
        text = "Respuesta sin procesar"
        db()

    return respuesta(text)
