from database.consultas import usuario
from entities.usuario import Usuario
from entities.df_request import get_parameter, get_username_telegram


def add_user_context(parameters, session):
    output = []
    context = {}
    context["name"] = f'{session}/contexts/__usuario__'
    context["lifespanCount"] = 8
    context["parameters"] = parameters
    output.append(context)
    return output


def get_user_context(request) -> Usuario:
    params = get_context_parameter(request, "__usuario__")
    if params != None:
        user = __load_user_from_params(params)
        if user.is_full():
            print("Usuario full por contexto __usuario__")
            return user

    username = get_parameter(request, "usuario")
    if username != None:
        user = usuario(username)
        if user.is_full():
            print("Usuario full por consulta en BD usuario de parametros")
            return user

    username = get_username_telegram(request)
    if username != None:
        user = usuario(username)
        if user.is_full():
            print("Usuario full por consulta en BD usuario de telegram")
            return user
    print("Usuario no encontrado en en contexto, parametros, payload telegram redireccionar a intent de Presentacion")
    return None


def __load_user_from_params(params) -> Usuario:
    if "usuario" in params and len(params["usuario"]) > 0:
        username = params["usuario"]
        user = Usuario(username)
        if "genero" in params and params["genero"] > 0:
            genero = params["genero"]
            user.genero(genero)
        if "talla_polera" in params and len(params["talla_polera"]) > 0:
            talla_polera = params["talla_polera"]
            user.talla_polera(talla_polera)
        if "talla_pantalon" in params and len(params["talla_pantalon"]) > 0:
            talla_pantalon = params["talla_pantalon"]
            user.talla_pantalon(talla_pantalon)
        if "talla_calzado" in params and len(params["talla_calzado"]) > 0:
            talla_calzado = params["talla_calzado"]
            user.talla_calzado(talla_calzado)
        if "nombre" in params and len(params["nombre"]) > 0:
            nombre = params["nombre"]
            user.nombre(nombre)
        if "apellido" in params and len(params["apellido"]) > 0:
            apellido = params["apellido"]
            user.apellido(apellido)
    return user


def get_context_parameter(request, context_name):
    if "queryResult" in request and "outputContexts" in request["queryResult"]:
        context_list = request["queryResult"]["outputContexts"]
        filter_context = filter(
            lambda context: context_name in context["name"], context_list)
        context_filtered = list(filter_context)
        if len(context_filtered) == 1:
            return context_filtered[0]["parameters"]
    return None
