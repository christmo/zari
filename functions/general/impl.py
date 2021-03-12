
def saludo(request):
    """
        Procesa la respuesta del Intent Welcome de saludo
    """
    #TODO: consultar respuestas desde BD sin nombre
    bot_response = request["queryResult"]["fulfillmentText"]
    text = bot_response.replace('{name}','')
    print(text)
    return text

def gateway(request):
    """
        Unifica la salida de los intents procesados con Webhook
    """
    response = ""
    if request["queryResult"]["intent"] != None:
        intent = request["queryResult"]["intent"]["displayName"]
        #parameters = request["queryResult"]["parameters"]
        if intent == "Welcome":
            response = saludo(request)
    return response