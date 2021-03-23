from entities.df_response import DFResponse
from entities.producto import Producto
from database import consultas as query


def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    name = request["originalDetectIntentRequest"]["payload"]["data"]["from"]["first_name"]
    bot_response = request["queryResult"]["fulfillmentText"]
    # TODO: consultar respuestas desde BD con nombre
    text = DFResponse().text(bot_response.replace('{name}', name))
    print(text)
    return text


def consultar_pantalones(request):
    """
        Procesa la respuesta del Intent Pantalones
    """
    parameters = request["queryResult"]["parameters"]
    #bot_response = request["queryResult"]["fulfillmentText"]
    nombre = parameters["Productos"][0]
    talla = parameters["talla"][0]
    color = parameters["color"][0]
    print(f"{nombre} - talla: {talla} - color: {color}")
    filter = Producto(nombre, talla, color, 1)
    products = query.productos(filter)
    print(f"Numero de productos: {len(products)}")
    text = DFResponse().cards(products)
    print(text)
    return text


def gateway(request):
    """
        Unifica la salida de los intents procesados con Webhook Telegram
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        if intent == "Welcome":
            response = saludo(request)
        if intent == "PeticionPantalones":
            response = consultar_pantalones(request)

    return response
