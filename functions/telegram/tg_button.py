import json


class TGButton():
    callback_data = ''
    text = ''

    def __init__(self, text, callback):
        self.text = text
        self.callback_data = callback

    def telegram(self):
        buttom = {}
        buttom["text"] = self.text
        buttom["callback_data"] = self.callback_data
        return buttom
