from entities.df_text import DFText
from entities.df_context import DFContext
import json


class DFResponse:
    response = {}

    def text(self, message):
        self.response["fulfillmentMessages"] = DFText().toText(message)
        return json.dumps(self.response)

    def text_user_context(self, message, usuario, session):
        self.response["fulfillmentMessages"] = DFText().toText(message)
        parameters = {}
        parameters["nombre"] = usuario.nombre
        parameters["apellido"] = usuario.apellido
        parameters["talla_calzado"] = str(usuario.talla_calzado)
        parameters["talla_pantalon"] = str(usuario.talla_pantalon)
        parameters["talla_polera"] = str(usuario.talla_polera)
        parameters["genero"] = usuario.genero
        self.response["outputContexts"] = DFContext().addContext(
            parameters, session
        )

        return json.dumps(self.response)

    def cards(self, products):
        fullfillment = []
        for prod in products:
            fullfillment.append(prod.toCard())
        self.response["fulfillmentMessages"] = fullfillment
        return json.dumps(self.response)

    def products_text(self, products):
        fulfillment = []
        for prod in products:
            DFText().addItem(
                f"{prod.nombre} - {prod.talla} - {prod.precio} - {prod.descripcion}",
                fulfillment
            )
        self.response["fulfillmentMessages"] = fulfillment
        return json.dumps(self.response)
