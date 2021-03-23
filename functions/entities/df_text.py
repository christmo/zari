class DFText:

    def __init__(self, message):
        self.message = message

    def toText(self):
        text = []
        text.append(self.message)

        text_wrapper = {}
        text_wrapper["text"] = text

        fullfillment = []
        fullfillment_message = {}
        fullfillment_message["text"] = text_wrapper
        fullfillment.append(fullfillment_message)

        return fullfillment
