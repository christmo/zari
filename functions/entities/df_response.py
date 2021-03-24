from entities.df_text import DFText
import json


class DFResponse:
    response = {}

    def text(self, message):
        self.response["fulfillmentMessages"] = DFText().toText(message)
        return json.dumps(self.response)

    def cards(self, products):
        fullfillment = []
        for prod in products:
            fullfillment.append(prod.toCard())
        self.response["fulfillmentMessages"] = fullfillment
        return json.dumps(self.response)

    def products_text(self, products):
        fullfillment = []
        for prod in products:
            DFText().addItem(
                f"{prod.nombre} - {prod.talla} - {prod.precio} - {prod.descripcion}",
                fullfillment
            )
        self.response["fulfillmentMessages"] = fullfillment
        return json.dumps(self.response)
