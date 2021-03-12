
def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    name = request["originalDetectIntentRequest"]["payload"]["data"]["from"]["first_name"]
    bot_response = request["queryResult"]["fulfillmentText"]
    #TODO: consultar respuestas desde BD con nombre
    text = bot_response.replace('{name}',name)
    print(text)
    return text

def gateway(request):
    """
        Unifica la salida de los intents procesados con Webhook
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        if intent == "Welcome":
            response = saludo(request)
    return response