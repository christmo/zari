def tg_quick_replies(titulo, botones, fulfillment):
    #fulfillment = []
    quickReplies = {}
    reply = {}
    reply["title"] = titulo
    reply["quickReplies"] = botones
    quickReplies["quickReplies"] = reply
    quickReplies["platform"] = "TELEGRAM"
    fulfillment.append(quickReplies)

    #self.response["fulfillmentMessages"] = fulfillment
