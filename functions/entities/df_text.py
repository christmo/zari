class DFText:

    def toText(self, message):
        text = []
        text.append(message)

        text_wrapper = {}
        text_wrapper["text"] = text

        fullfillment = []
        fullfillment_message = {}
        fullfillment_message["text"] = text_wrapper
        fullfillment.append(fullfillment_message)

        return fullfillment

    def addItem(self, message, fullfillment):
        text = []
        text.append(message)

        text_wrapper = {}
        text_wrapper["text"] = text

        fullfillment_message = {}
        fullfillment_message["text"] = text_wrapper
        fullfillment.append(fullfillment_message)

        return fullfillment