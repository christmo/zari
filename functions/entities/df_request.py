def get_username(request):
    if "payload" in request["originalDetectIntentRequest"]:
        if "data" in request["originalDetectIntentRequest"]["payload"]:
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]:
                if "username" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["username"]
                if "id" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["id"]
    return None


def get_name(request):
    if "payload" in request["originalDetectIntentRequest"]:
        if "data" in request["originalDetectIntentRequest"]["payload"]:
            if "from" in request["originalDetectIntentRequest"]["payload"]["data"]:
                if "first_name" in request["originalDetectIntentRequest"]["payload"]["data"]["from"]:
                    return request["originalDetectIntentRequest"]["payload"]["data"]["from"]["first_name"]
    return None


def get_session(request):
    if "session" in request:
        return request["session"]
    return None
