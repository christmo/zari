from general.pantalones import consultar_pantalones
from entities.usuario import Usuario
from database.command import limpiar_carrito, pagar_carrito
from database.persitencia import save_shopping_car, save_usuario
from entities.df_context import get_carrito_context, get_user_context
from entities.df_request import get_product_from_params, user_parameters
from entities.df_response import DFResponse
from database import consultas as query


def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    response = DFResponse(request)
    print(response)
    bot_response = request["queryResult"]["fulfillmentText"]
    response.text(bot_response.replace('{name}', ''))
    usuario = query.usuario("christmo")
    response.context_usuario(usuario)
    return response.to_json()


# def consultar_pantalones(request):
#    """
#        Procesa la respuesta del Intent Pantalones
#    """
#    response = DFResponse(request)
#    user = get_user_context(request)
#    print(f"user nombre: {user.get_nombre()} - talla: {user.get_talla_pantalon()} \
#        - genero: {user.get_genero()}")
#    producto = get_product_from_params(request)
#    producto.talla = user.get_talla_pantalon()
#    producto.genero(user.get_genero())
#    print(f"producto nombre: {producto.nombre} - talla: {producto.talla} \
#            - color: {producto.color} - genero: {producto.get_genero()}")
#    products = query.productos(producto)
#    print(f"Numero de productos: {len(products)}")
#    response.products_text(products)
#    return response.to_json()


def consultar_camisetas(request):
    """
        Procesa la respuesta del Intent Camisetas
    """
    response = DFResponse(request)
    user = get_user_context(request)
    print(f"user nombre: {user.get_nombre()} - talla: {user.get_talla_polera()} \
            - genero: {user.get_genero()}")
    producto = get_product_from_params(request)
    producto.talla = user.get_talla_polera()
    producto.genero(user.get_genero())
    print(f"producto nombre: {producto.nombre} - talla: {producto.talla} \
            - color: {producto.color} - genero: {producto.get_genero()}")
    products = query.productos(producto)
    print(f"Numero de productos: {len(products)}")
    response.products_text(products)
    return response.to_json()


def agregar_producto(request):
    """
        Agregar producto al carrito de compras
    """
    response = DFResponse(request)
    user = get_user_context(request)
    if user != None:
        producto = get_product_from_params(request)
        car = save_shopping_car(user, producto)
        response.text(
            f"Productos en el carrito {len(car.detalles)} por un total de {car.total}€")
        response.context_shoppingcar(car)
    else:
        response.register_event()
    return response.to_json()


def eliminar_carrito(request):
    """
        Proceso para desactivar el carrito de compras enviado, y generar uno nuevo
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    response = DFResponse(request)
    car = get_carrito_context(request)
    result = limpiar_carrito(car.id_car)
    if result:
        response.text(
            "Carrito de compras listo para recibir nuevos productos!")
    else:
        response.text(
            "Tu carrito de compras no se ha podido limpiar, intenta nuevamente!")
    return response.to_json()


def consultar_carrito(request):
    """
        Consultar los productos del carrito y el total a pagar
    """
    response = DFResponse(request)
    user = get_user_context(request)
    if user != None:
        productos = query.shopping_cart(user)
        response.shopping_cart_text(productos)
    else:
        response.register_event()
    return response.to_json()


def comprar(request):
    """
        Proceso para comprar todos los productos del carrito
    """
    response = DFResponse(request)
    user = get_user_context(request)
    if user != None:
        orden = pagar_carrito(user)
        #entrega = datetime.datetime.today() + datetime.timedelta(days=5)
        if orden != None:
            response.text(
                f"Se ha procesado el pago con tú tarjeta terminada en {orden.tarjeta}, "
                f"el número de orden es {orden.carrito}, tus productos se entregarán el {orden.fecha_formateada()} "
                f"en tu dirección registrada: {orden.direccion}"
            )
        else:
            response.text("No encontramos tu información")
    else:
        response.register_event()
    return response.to_json()


def registrar_usuario(request):
    """
        Registrar Usuario en el sistema
    """
    response = DFResponse(request)
    user = user_parameters(request)
    user = save_usuario(user)
    usuario = Usuario.parse_usuario(user)
    response.context_usuario(usuario)
    response.text(
        "Listo, ahora puedes preguntarme cualquier cosa y buscaré lo que te quede mejor a ti")
    return response.to_json()


def gateway(request):
    """
        Unifica la salida de los intents procesados con Webhook
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        print(f"Intent invocado Dialogflow: {intent}")
        if intent == "Welcome":
            response = saludo(request)
        if intent == "PeticionPantalones" or intent == "pantalones-parameters":
            response = consultar_pantalones(request)
        if intent == "PeticionCamiseta":
            response = consultar_camisetas(request)
        if intent == "AgregarProducto":
            response = agregar_producto(request)
        if intent == "EliminarCarrito":
            response = eliminar_carrito(request)
        if intent == "VerCarrito":
            response = consultar_carrito(request)
        if intent == "Comprar":
            response = comprar(request)
        if intent == "RegistrarUsuario":
            response = registrar_usuario(request)
    return response
