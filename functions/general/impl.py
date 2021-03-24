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
    text = DFResponse().products_text(products)
    return text


def consultar_camisetas(request):
    """
        Procesa la respuesta del Intent Camisetas
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    nombre, talla, color = parameters(request)
    print(f"nombre: {nombre} - talla: {talla} - color: {color}")
    filter = Producto(nombre, talla, color, 2)
    products = query.productos(filter)
    print(f"Numero de productos: {len(products)}")
    text = DFResponse().products_text(products)
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
        if intent == "PeticionCamiseta":
            response = consultar_camisetas(request)
    return response
