from entities.producto import Producto
from entities.df_request import get_product_from_params
from entities.df_response import DFResponse
from database import consultas as query
from entities.df_context import get_user_context


def consultar_pantalones(request):
    """
        Procesa la respuesta del Intent Pantalones
    """
    #bot_response = request["queryResult"]["fulfillmentText"]
    response = DFResponse(request)
    producto = get_product_from_params(request)
    __cambiar_filtro_usuario(request, producto)
    if __check_buscar_producto(producto):
        print(producto)
        products = query.productos(producto)
        print(f"Numero de productos encontrados: {len(products)}")
        if len(products) > 0:
            response.products_text(products)
        else:
            response.text(f'No encontré productos de este tipo {producto.nombre}'
                          f' de color {producto.color}, para {producto.get_genero_texto()} de talla {producto.talla}')
    else:
        print("Completar parametros del producto Talla y Genero del cliente!!!")
        response.talla_pantalones_event(producto)

    return response.to_json()


def __check_buscar_producto(producto: Producto):
    if producto != None:
        buscar = True
        if producto.talla != None and len(producto.talla) == 0:
            buscar = False
        if producto.color != None and len(producto.color) == 0:
            buscar = False
        if producto.nombre != None and len(producto.nombre) == 0:
            buscar = False
        if producto.get_genero() == 0:
            buscar = False
    else:
        buscar = False
    return buscar

"""
    TODO: Poner en el contexto si la busqueda es para el usuario o para terceros
"""
def __cambiar_filtro_usuario(request, producto):
    user = get_user_context(request)
    if user != None and user.is_full():
        print(user)
        producto.talla = user.get_talla_pantalon()
        producto.genero(user.get_genero())
