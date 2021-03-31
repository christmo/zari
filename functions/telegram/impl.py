from entities.df_context import get_user_context
from entities.df_request import get_name, get_product_from_params, get_username_telegram, get_product_from_params
from entities.df_response import DFResponse
from entities.producto import Producto
from database import consultas as query


def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    response = DFResponse(request)
    bot_response = request["queryResult"]["fulfillmentText"]
    name = get_name(request)
    username = get_username_telegram(request)
    print(f"username: {username}")
    if username != None:
        usuario = query.usuario(username)
        if len(usuario.get_nombre()) > 1:
            response.text(bot_response.replace('{name}', usuario.get_nombre()))
            response.context_usuario(usuario)
            return response.to_json()

    response.text(bot_response.replace('{name}', name))
    return response.to_json()


def consultar_pantalones(request):
    """
        Procesa la respuesta del Intent Pantalones
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    response = DFResponse(request)
    user = get_user_context(request)
    print(
        f"user nombre: {user.get_nombre()} - talla: {user.get_talla_pantalon()} - genero: {user.get_genero()}")
    producto = get_product_from_params(request)
    producto.talla = user.get_talla_pantalon()
    producto.genero(user.get_genero())
    print(f"producto nombre: {producto.nombre} - talla: {producto.talla} \
            - color: {producto.color} - genero: {producto.get_genero()}")
    print(f"TIPO: {producto.tipo}")
    products = query.productos(producto)
    print(f"Numero de productos: {len(products)}")
    response.cards(products)
    return response.to_json()


def consultar_camisetas(request):
    """
        Procesa la respuesta del Intent Camisetas
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    response = DFResponse(request)
    user = get_user_context(request)
    print(
        f"user nombre: {user.get_nombre()} - talla: {user.get_talla_polera()} - genero: {user.get_genero()}")
    producto = get_product_from_params(request)
    producto.talla = user.get_talla_polera()
    producto.genero(user.get_genero())
    print(
        f"producto nombre: {producto.nombre} - talla: {producto.talla} - color: {producto.color} - genero: {producto.get_genero()}")
    products = query.productos(producto)
    print(f"Numero de productos: {len(products)}")
    response.cards(products)
    return response.to_json()


def agregar_producto(request):
    """
        Agregar producto al carrito de compras
    """
    response = DFResponse(request)
    user = get_user_context(request)
    if user != None:
        producto = get_product_from_params(request)
        cesta = 0
        #costo = query.costo_producto(id_producto)
        bot_response = request["queryResult"]["fulfillmentText"]
        response.text(
            f"Se agregar producto - código: {producto.codigo} - costo: {producto.costo}")
        response.context_cesta()
    else:
        response.register_event()
    return response.to_json()


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
        if intent == "AgregarProducto":
            response = agregar_producto(request)

    return response
