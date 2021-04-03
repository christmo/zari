from entities.car_detalle import CarDetalle
from entities.carrito import Carrito
from entities.usuario import Usuario
from entities.df_context import add_car_context, add_user_context
from entities.df_request import get_session
from entities.df_text import DFText
import json


class DFResponse:
    response = {}

    def __init__(self, request):
        self.request = request

    def to_json(self):
        print(self.response)
        return json.dumps(self.response)

    def text(self, message):
        self.response["fulfillmentMessages"] = DFText().toText(message)

    def context_usuario(self, usuario: Usuario):
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
        fullfillment = []
        for prod in products:
            fullfillment.append(prod.toCard())
        self.response["fulfillmentMessages"] = fullfillment

    def products_text(self, products):
        fulfillment = []
        for prod in products:
            DFText().addItem(
                f"{prod.nombre} - {prod.talla} - {prod.precio} - {prod.descripcion}",
                fulfillment
            )
        self.response["fulfillmentMessages"] = fulfillment

    def register_event(self):
        followup = {}
        followup["name"] = "register-event"
        parameters = {}
        # parameters[""]
        followup["parameters"] = parameters
        self.response["followupEventInput"] = followup
