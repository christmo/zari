from entities.producto import Producto


def get_username_telegram(request):
    if "payload" in request["originalDetectIntentRequest"]:
        if "data" in request["originalDetectIntentRequest"]["payload"]:
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]:
                if "username" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["username"]
                if "id" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["id"]
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
