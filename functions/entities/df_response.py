from entities.df_request import get_session
from entities.df_text import DFText
from entities.df_context import DFContext
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

    def context_usuario(self, usuario):
        parameters = {}
        parameters["nombre"] = usuario.nombre
        parameters["apellido"] = usuario.apellido
        parameters["usuario"] = usuario.username
        parameters["talla_calzado"] = str(usuario.talla_calzado)
        parameters["talla_pantalon"] = str(usuario.talla_pantalon)
        parameters["talla_polera"] = str(usuario.talla_polera)
        parameters["genero"] = usuario.get_genero()
        self.response["outputContexts"] = DFContext().addUsuarioContext(
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
