from telegram.tg_inline_buttons import tg_inline_buttons
from telegram.tg_quick_replies import tg_quick_replies
from entities.producto import Producto
from entities.car_detalle import CarDetalle
from entities.carrito import Carrito
from entities.usuario import Usuario
from entities.df_context import add_car_context, add_user_context
from entities.df_request import get_session
from entities.df_text import DFText
import json


class DFResponse:
    response = {}
    fulfillment = []

    def __init__(self, request):
        self.request = request
        self.response = {}
        self.fulfillment = []

    def to_json(self):
        self.response["fulfillmentMessages"] = self.fulfillment
        print(self.response)
        return json.dumps(self.response)

    def text(self, message):
        #self.response["fulfillmentMessages"] = DFText().toText(message)
        self.fulfillment = DFText().toText(message)

    def context_usuario(self, usuario: Usuario):
        if usuario != None:
            parameters = {}
            parameters["nombre"] = usuario.get_nombre()
            parameters["apellido"] = usuario.get_apellido()
            parameters["usuario"] = usuario.get_username()
            parameters["talla_calzado"] = str(usuario.get_talla_calzado())
            parameters["talla_pantalon"] = str(usuario.get_talla_pantalon())
            parameters["talla_polera"] = str(usuario.get_talla_polera())
            parameters["genero"] = usuario.get_genero()
            parameters["id_usuario"] = usuario.get_id()
            self.response["outputContexts"] = add_user_context(
                parameters, get_session(self.request)
            )
        else:
            print("No hay usuario para poner en contexto __usuario__")

    def context_shoppingcar(self, car: Carrito):
        parameters = {}
        parameters["car"] = car.id_car
        parameters["car_total"] = float(car.total)
        parameters["car_numero_items"] = len(car.detalles)
        parameters["car_items"] = [prod.id_producto for prod in car.detalles]
        self.response["outputContexts"] = add_car_context(
            parameters, get_session(self.request)
        )

    def cards(self, products):
        #fulfillment = []
        for prod in products:
            self.fulfillment.append(prod.toCard())
        #self.response["fulfillmentMessages"] = fulfillment

    def products_text(self, products):
        #fulfillment = []
        for prod in products:
            DFText().addItem(
                f"{prod.codigo} - {prod.nombre} - {prod.talla} - {prod.precio} - {prod.descripcion}",
                self.fulfillment
            )
        #self.response["fulfillmentMessages"] = fulfillment

    def shopping_cart_text(self, products):
        #fulfillment = []
        total = 0
        numero = 0
        if len(products) > 0:
            DFText().addItem(
                "Voy a listar los productos que tienes en tu carrito:",
                self.fulfillment
            )
            for prod in products:
                DFText().addItem(
                    f"{numero + 1}. - {prod.descripcion} código {prod.codigo} - {prod.nombre}, "
                    f"en talla {prod.talla} y cuesta {'{:.2f}€'.format(prod.precio)}",
                    self.fulfillment
                )
                total += float(prod.precio)
                numero += 1
            DFText().addItem(
                f"En total tus {numero} productos suman {'{:.2f}€'.format(total)}",
                self.fulfillment
            )
            DFText().addItem(
                f'\nRecuerda si quieres limpiar tu carrito usa frases como "zari elimina mi carrito" ',
                self.fulfillment
            )
        else:
            DFText().addItem(
                'Actualmente no tienes productos en tu carrito, si quieres agregar items, '
                'busca lo que te guste y pulsa el botón de "Agregar al Carrito".',
                self.fulfillment
            )
        #self.response["fulfillmentMessages"] = fulfillment

    def register_event(self):
        followup = {}
        followup["name"] = "register-event"
        parameters = {}
        # parameters[""]
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def register_card_event(self, user: Usuario):
        followup = {}
        followup["name"] = "register-card-event"
        parameters = {}
        parameters["user"] = user.get_id()
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def presentarse_event(self):
        followup = {}
        followup["name"] = "presentarse_event"
        parameters = {}
        # parameters[""]
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def talla_pantalones_event(self, producto: Producto):
        print(producto)
        followup = {}
        followup["name"] = "get-talla-pantalones"
        parameters = {}
        if producto.color != None:
            parameters["color"] = producto.color
        if producto.nombre != None:
            parameters["producto"] = producto.nombre
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def parametros_producto_event(self, producto: Producto):
        print(producto)
        followup = {}
        followup["name"] = "fill-parametros_producto"
        parameters = {}
        if producto.color != None:
            parameters["color"] = producto.color
        if producto.nombre != None:
            parameters["producto"] = producto.nombre
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def fill_numero_zapatos_event(self, producto: Producto):
        print(producto)
        followup = {}
        followup["name"] = "fill-numero-zapatos"
        parameters = {}
        if producto.color != None:
            parameters["color"] = producto.color
        if producto.nombre != None:
            parameters["producto"] = producto.nombre
        if producto.get_genero() != 0:
            parameters["genero"] = producto.get_genero_texto()
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def fill_talla_productos_event(self, producto: Producto):
        print(producto)
        followup = {}
        followup["name"] = "fill-talla_productos"
        parameters = {}
        if producto.color != None:
            parameters["color"] = producto.color
        if producto.nombre != None:
            parameters["producto"] = producto.nombre
        if producto.get_genero() != 0:
            parameters["genero"] = producto.get_genero_texto()
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup

    def quick_replies(self, titulo, botones):
        tg_quick_replies(titulo, botones, self.fulfillment)

    def inline_buttons(self, titulo, botones):
        tg_inline_buttons(titulo, botones, self.fulfillment)
