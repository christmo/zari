from entities.df_context import get_user_context
from entities.df_request import get_name, get_product_from_params, get_session, get_username, param_nombre_talla_color, param_product_id_costo
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
    username = get_username(request)
    print(f"username: {username}")
    if username != None:
        usuario = query.usuario(username)
        if len(usuario.nombre) > 1:
            response.text(bot_response.replace('{name}', usuario.nombre))
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
        f"user nombre: {user.nombre} - talla: {user.talla_pantalon} - genero: {user.get_genero()}")
    producto = get_product_from_params(request)
    producto.talla = user.talla_pantalon
    producto.genero(user.get_genero())
    print(
        f"producto nombre: {producto.nombre} - talla: {producto.talla} - color: {producto.color} - genero: {producto.get_genero()}")
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
        f"user nombre: {user.nombre} - talla: {user.talla_pantalon} - genero: {user.get_genero()}")
    producto = get_product_from_params(request)
    producto.talla = user.talla_polera
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
    producto, id_producto, costo = param_product_id_costo(request)
    #costo = query.costo_producto(id_producto)
    bot_response = request["queryResult"]["fulfillmentText"]
    response.text(f"{bot_response} - {id_producto} - {costo}")
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
