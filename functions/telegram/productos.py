from entities.producto import Producto
from entities.df_request import get_product_from_params, get_username_telegram
from entities.df_response import DFResponse
from database import consultas as query
from entities.df_context import get_user_context


def consultar_productos(request):
    """
        Procesa la respuesta del Intent Pantalones
    """
    response = DFResponse(request)
    producto = get_product_from_params(request)
    __cambiar_filtro_usuario(request, producto)
    if __check_buscar_producto(producto):
        print(producto)
        products = query.productos(producto)
        print(f"Numero de productos encontrados: {len(products)}")
        if len(products) > 0:
            response.cards(products)
        else:
            if producto.tipo == 5:
                response.text(f'No encontré productos de este tipo {producto.nombre} '
                              f'de color {producto.color}, para {producto.get_genero_texto()} de número {producto.numero}')
            else:
                response.text(f'No encontré productos de este tipo {producto.nombre} '
                              f'de color {producto.color}, para {producto.get_genero_texto()} de talla {producto.talla}')
    else:
        print("Completar parametros del producto Talla y Genero del cliente evento fill-parametros_producto")
        username = get_username_telegram(request)
        print(f"Username producto: {username}")
        if username != None:
            usuario = query.usuario(username)
            if usuario != None and len(usuario.get_nombre()) > 1:
                response.context_usuario(usuario)
            else:
                response.init_context_usuario()
        else:
            response.init_context_usuario()
        response.parametros_producto_event(producto)

    return response.to_json()


def __check_buscar_producto(producto: Producto):
    if producto != None:
        buscar = True
        if producto.tipo != 5:
            if producto.talla == None or len(producto.talla) == 0:
                buscar = False
        else:
            if producto.numero == None or producto.numero == 0:
                buscar = False
        if producto.color == None or len(producto.color) == 0:
            buscar = False
        if producto.nombre == None or len(producto.nombre) == 0:
            buscar = False
        if producto.get_genero() == 0:
            buscar = False
    else:
        buscar = False
    return buscar


def __cambiar_filtro_usuario(request, producto: Producto):
    user = get_user_context(request)
    if user != None and user.is_full():
        print(user)
        if producto.talla == None or len(producto.talla) == 0:
            if producto.tipo == 1 or producto.tipo == 4 or producto.tipo == 6:
                producto.talla = user.get_talla_pantalon()
            if producto.tipo == 2 or producto.tipo == 3 or producto.tipo == 7:
                producto.talla = user.get_talla_polera()
        if producto.numero == None or producto.numero == 0:
            producto.numero = user.get_talla_calzado()
        else:
            print('Se toma la talla del producto buscado no del cliente')
        if producto.get_genero() == 0:
            producto.genero(user.get_genero())
        else:
            print('Se toma el genero del producto buscado no del cliente')


def validar_parametros_producto(request):
    """
        Validar parametros Producto
    """
    response = DFResponse(request)
    producto = get_product_from_params(request)
    __cambiar_filtro_usuario(request, producto)
    if __check_buscar_producto(producto):
        print(producto)
        products = query.productos(producto)
        print(f"Numero de productos encontrados: {len(products)}")
        if len(products) > 0:
            response.cards(products)
        else:
            if producto.tipo == 5:
                response.text(f'No encontré productos de este tipo {producto.nombre} '
                              f'de color {producto.color}, para {producto.get_genero_texto()} de número {producto.numero}')
            else:
                response.text(f'No encontré productos de este tipo {producto.nombre} '
                              f'de color {producto.color}, para {producto.get_genero_texto()} de talla {producto.talla}')
    else:
        print("Completar parametros del producto Talla y Genero del cliente!!!")
        if producto.nombre == 'zapatos':
            response.fill_numero_zapatos_event(producto)
        else:
            response.fill_talla_productos_event(producto)

    return response.to_json()


def menu_productos(request):
    response = DFResponse(request)
    response.inline_buttons_vertical("Tengo estas opciones que te pueden interesar.",
                                     ["👖 ver pantalones", "👕 ver camisetas", "👗 ver vestidos", "👟 ver zapatos"])
    return response.to_json()
