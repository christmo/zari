from telegram.productos import consultar_productos, validar_parametros_producto
from database.command import limpiar_carrito, pagar_carrito
from database.persitencia import save_shopping_car, save_usuario
from entities.df_context import get_carrito_context, get_user_context
from entities.df_request import get_name, get_parameter, get_product_from_params, get_username_telegram, get_product_from_params, user_parameters
from entities.df_response import DFResponse
from database import consultas as query
from entities.usuario import Usuario


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
        if usuario != None and len(usuario.get_nombre()) > 1:
            response.text(bot_response.replace('{name}', usuario.get_nombre()))
            response.context_usuario(usuario)
            return response.to_json()
        # else:
            # response.register_event()

    nombre = name if name != None else username
    response.text(bot_response.replace('{name}', nombre))
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
        response.inline_buttons("A donde quieres ir?", [
                                "Pagar", "Ver Carrito"])
    else:
        print('Enviar a registrar al cliente')
        response.text(
            "Necesitamos registrarte como usuario para agregar productos a tu carrito, "
            "completa las preguntas para poderte dar mejores recomendaciones "
            "y ajustar las búsquedas a tu información solo tardará 1 minuto."
            '\n\nPara empezar tu registro dime "zari agregame como cliente"'
            '\n(Si al iniciar no quieres continuar siempre me puedes decir "cancelar" y detendré las preguntas)'
        )
        response.inline_buttons("A donde quieres ir?", [
                                "Registrarme", "Promociones"])
        # response.register_event()
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
        response.inline_buttons("A donde quieres ir?", ["Limpiar Carrito", "Pagar"])
    else:
        response.register_event()
    return response.to_json()


def tarjetas(request):
    """
        Consultar las tarjetas del cliente para el pago
    """
    response = DFResponse(request)
    user = get_user_context(request)
    if user != None:
        user = query.tarjetas(user)
        if len(user.get_tarjetas()) > 0:
            response.quick_replies(
                'Con que tarjeta quieres pagar?',
                user.get_tarjetas()
            )
        else:
            response.register_card_event(user)
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
        if orden != None:
            tarjeta = get_parameter(request, 'tarjeta')
            response.text(
                f"Se ha procesado el pago con tú tarjeta terminada en {tarjeta}, "
                f"el número de orden es {orden.carrito}, tus productos se entregarán el {orden.fecha_formateada()} "
                f"en tu dirección registrada: {orden.direccion}"
            )
            response.inline_buttons("A donde quieres ir?", ["Promociones"])
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
        "Genial, ahora puedes agregar productos a tu carrito!!!"
    )
    response.inline_buttons("A donde quieres ir?", ["Promociones"])
    return response.to_json()


def gateway(request):
    """
        Unifica la salida de los intents procesados con Webhook Telegram
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        print(f"Intent invocado Telegram: {intent}")
        if intent == "Welcome":
            response = saludo(request)
        # if intent == "PeticionCamiseta":
        #    response = consultar_camisetas(request)
        if intent == "AgregarProducto":
            response = agregar_producto(request)
        if intent == "EliminarCarrito":
            response = eliminar_carrito(request)
        if intent == "VerCarrito":
            response = consultar_carrito(request)
        if intent == "Comprar":
            response = tarjetas(request)
        if intent == "Comprar-tarjeta":
            response = comprar(request)
        if intent == "RegistrarUsuario":
            response = registrar_usuario(request)
        # if intent == "PeticionPantalones" or intent == "pantalones-parameters" \
        if intent == "SolicitarProducto" or intent == "parametros-producto-talla" \
                or intent == "parametros-producto-numero" or intent == "producto-root":
            response = consultar_productos(request)
        if intent == "parametros-producto":
            response = validar_parametros_producto(request)
    return response
