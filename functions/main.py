import json

def ver_zapatos(parameters):
    print(parameters)
    return "Christian no se que zapatos quieres"

def compose_response(message):
    text = []
    text.append(message)

    text_wrapper = {}
    text_wrapper["text"] = text

    fullfillment = []
    fullfillment_message = {}
    fullfillment_message["text"] = text_wrapper
    fullfillment.append(fullfillment_message)

    response = {}
    response["fulfillmentMessages"] = fullfillment
    return json.dumps(response)

def zari_webhook(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    print(request_json)
    if request_json["queryResult"] != None:
        text = request_json["queryResult"]["queryText"]
        intent = request_json["queryResult"]["intent"]["displayName"]
        print(intent)
        print(intent == "VerZapatos")
        parameters = request_json["queryResult"]["parameters"]
        
        if intent == "VerZapatos":
            return compose_response(ver_zapatos(parameters))
    
    return compose_response(f"Hola mundo sin intent {text}")

    #if request.args and 'message' in request.args:
    #    return request.args.get('message')
    #elif request_json and 'message' in request_json:
    #    return request_json['message']
    #else:
    #    return f'Hello World!'