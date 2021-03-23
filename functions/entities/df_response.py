from entities.df_text import DFText
import json


class DFResponse:
    response = {}

    def text(self, message):
        self.response["fulfillmentMessages"] = DFText(message).toText()
        return json.dumps(self.response)

    def cards(self, products):
        fullfillment = []
        for prod in products:
            fullfillment.append(prod.toCard())
        self.response["fulfillmentMessages"] = fullfillment
        return json.dumps(self.response)
