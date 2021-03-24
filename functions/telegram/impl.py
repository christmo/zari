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


def parameters(request):
    parameters = request["queryResult"]["parameters"]
    nombre = None
    talla = None
    color = None
    if "productos" in parameters:
        nombre = parameters["productos"]
    if "talla" in parameters:
        talla = parameters["talla"]
    if "color" in parameters:
        color = parameters["color"]
    return nombre, talla, color


def consultar_pantalones(request):
    """
        Procesa la respuesta del Intent Pantalones
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    nombre, talla, color = parameters(request)
    print(f"{nombre} - talla: {talla} - color: {color}")
    filter = Producto(nombre, talla, color, 1)
    products = query.productos(filter)
    print(f"Numero de productos: {len(products)}")
    text = DFResponse().cards(products)
    return text


def consultar_camisetas(request):
    """
        Procesa la respuesta del Intent Camisetas
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    nombre, talla, color = parameters(request)
    print(f"{nombre} - talla: {talla} - color: {color}")
    filter = Producto(nombre, talla, color, 2)
    products = query.productos(filter)
    print(f"Numero de productos: {len(products)}")
    text = DFResponse().cards(products)
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
        if intent == "PeticionCamiseta":
            response = consultar_camisetas(request)

    return response
