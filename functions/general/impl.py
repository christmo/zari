from entities.df_response import DFResponse
from entities.producto import Producto
from database import consultas as query


def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    # TODO: consultar respuestas desde BD sin nombre
    bot_response = request["queryResult"]["fulfillmentText"]
    text = DFResponse().text(bot_response.replace('{name}', ''))
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
        Unifica la salida de los intents procesados con Webhook
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        #parameters = request["queryResult"]["parameters"]
        if intent == "Welcome":
            response = saludo(request)
        if intent == "PeticionPantalones":
            response = consultar_pantalones(request)
    return response
