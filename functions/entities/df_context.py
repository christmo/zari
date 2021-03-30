from entities.usuario import Usuario
from entities.df_request import get_username


class DFContext:

    """
    "message": "Webhook call failed. Error: [ResourceName error] Path 'name' does not match template 
    'projects/{project_id=*}/locations/{location_id=*}/agent/environments/{environment_id=*}/users/{user_id=*}/sessions/{session_id=*}/contexts/{context_id=*}'.."
    """

    def addUsuarioContext(self, parameters, session):
        output = []

        context = {}
        context["name"] = f'{session}/contexts/__usuario__'
        context["lifespanCount"] = 8
        context["parameters"] = parameters

        output.append(context)
        return output


def get_user_context(request) -> Usuario:
    username = get_username(request)
    user = Usuario(username)
    params = get_context_parameter(request, "__usuario__")
    if params != None:
        user.genero(params["genero"])
        user.talla_polera = params["talla_polera"]
        user.talla_pantalon = params["talla_pantalon"]
        user.talla_calzado = params["talla_calzado"]
        user.nombre = params["nombre"]
        user.apellido = params["apellido"]
    else:
        print("Context not found __usuario__")
    return user

def get_context_parameter(request, context_name):
    if "queryResult" in request and "outputContexts" in request["queryResult"]:
        context_list = request["queryResult"]["outputContexts"]
        filter_context = filter(lambda context: context_name in context["name"], context_list)
        context_filtered = list(filter_context)
        if len(context_filtered) == 1:
            return context_filtered[0]["parameters"]
    return None