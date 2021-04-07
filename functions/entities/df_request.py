from entities.db_usuario import DBUsuario
from entities.usuario import Usuario
from entities.producto import Producto


def get_username_telegram(request):
    if "payload" in request["originalDetectIntentRequest"]:
        if "data" in request["originalDetectIntentRequest"]["payload"]:
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]:
                if "username" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["username"]
                if "id" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["id"]
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]["callback_query"]:
                if "username" in request["originalDetectIntentRequest"]["payload"]["data"]["callback_query"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["callback_query"]["from"]["username"]
                if "id" in request["originalDetectIntentRequest"]["payload"]["data"]["callback_query"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["callback_query"]["from"]["id"]                
    return None


def get_name(request):
    if "payload" in request["originalDetectIntentRequest"]:
        if "data" in request["originalDetectIntentRequest"]["payload"]:
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]:
                if "first_name" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["first_name"]
    return None


def get_session(request):
    if "session" in request:
        return request["session"]
    return None


def get_parameter(request, param):
    parameters = request["queryResult"]["parameters"]
    if param in parameters:
        return parameters[param]
    return None


def get_product_from_params(request) -> Producto:
    nombre, talla, color = param_nombre_talla_color(request)
    producto, id_producto, costo = param_product_id_costo(request)
    p = Producto(nombre, talla, color, producto)
    p.genero(get_parameter(request, "genero"))
    p.codigo = id_producto
    p.costo = costo
    return p


def param_nombre_talla_color(request):
    nombre = get_parameter(request, "producto")
    talla = get_parameter(request, "talla")
    color = get_parameter(request, "color")
    return nombre, talla, color


def param_product_id_costo(request):
    producto = get_parameter(request, "producto")
    id_producto = get_parameter(request, "id_producto")
    costo = get_parameter(request, "costo")
    return producto, id_producto, costo


def user_parameters(request):
    username = get_username_telegram(request)
    nombre_apellido = get_parameter(request, 'nombre').split(' ')
    if len(nombre_apellido) == 2:
        nombre = nombre_apellido[0]
        apellido = nombre_apellido[1]
    else:
        nombre = nombre_apellido[0]
        apellido = None
        print(f"No se envia nombre y apellido {nombre_apellido}")
    talla_pantalon = get_parameter(request, 'talla_pantalon')
    talla_polera = get_parameter(request, 'talla_camiseta')
    talla_calzado = get_parameter(request, 'talla_calzado')
    direccion = get_parameter(request, 'direccion')
    genero = __genero(get_parameter(request, 'genero'))
    user = DBUsuario(nombre=nombre, apellido=apellido, talla_pantalon=talla_pantalon,
                     talla_polera=talla_polera, talla_calzado=talla_calzado, genero=genero,
                     telegram=username, estado='ACTIVO', direccion=direccion)
    return user


def __genero(genero):
    if genero != None:
        if "hombre" == genero:
            genero = "M"
        if "mujer" == genero:
            genero = "F"
        if "niño" == genero:
            genero = "NM"
        if "niña" == genero:
            genero = "NF"
    return genero
