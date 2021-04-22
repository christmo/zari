from telegram.tg_button import TGButton


def tg_inline_buttons(titulo, botones, fulfillment):
    payload = {}
    telegram = {}
    reply_markup = {}
    inline_keyboard = []
    inline_keyboard.append(
        [TGButton(boton, boton).telegram() for boton in botones]
    )
    reply_markup["inline_keyboard"] = inline_keyboard
    telegram["text"] = titulo
    telegram["reply_markup"] = reply_markup
    payload["telegram"] = telegram
    payload["platform"] = "TELEGRAM"
    wrap = {}
    wrap["payload"] = payload
    fulfillment.append(wrap)


def tg_inline_buttons_vertical(titulo, botones, fulfillment):
    payload = {}
    telegram = {}
    reply_markup = {}
    inline_keyboard = []
    for boton in botones:
        inline_keyboard.append(
            [{
                "callback_data": boton,
                "text": boton
            }]
        )
    reply_markup["inline_keyboard"] = inline_keyboard
    telegram["text"] = titulo
    telegram["reply_markup"] = reply_markup
    payload["telegram"] = telegram
    payload["platform"] = "TELEGRAM"
    wrap = {}
    wrap["payload"] = payload
    fulfillment.append(wrap)

    #self.response["fulfillmentMessages"] = fulfillment
    # x = """
    # {
    #    "payload": {
    #        "telegram": {
    #            "reply_markup": {
    #                "inline_keyboard": [
    #                    [
    #                    {
    #                        "callback_data": "news",
    #                        "text": "Daily News"
    #                    }
    #                    ],
    #                    [
    #                    {
    #                        "callback_data": "features",
    #                        "text": "New Features"
    #                    }
    #                    ]
    #                ]
    #            },
    #            "text": "What would you like help with?"
    #        }
    #    },
    #    "platform": "TELEGRAM"
    # }"""
    #fulfillment = self.response["fulfillmentMessages"]
    # fulfillment.append(json.loads(x))
    #self.response["fulfillmentMessages"] = fulfillment
