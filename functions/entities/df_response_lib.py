# Responses for Telegram
class telegram_response():

    # class variable initializer initializer
    def __init__(self):
        self.platform = "TELEGRAM"

    def text_response(self, texts):
        # text should contain at least one string
        if len(texts) <= 0:
            raise Exception("Provide the text for the text response")
        else:
            # text_obj list for storing the text variations
            text_obj = []
            for text in texts:
                text_obj.append(str(text))

            # return the text response
            return {
                "text": {
                    "text": text_obj
                },
                "platform": self.platform
            }

    def quick_replies(self, title, quick_replies_list):
        if title == "":
            raise Exception("Title is required for basic card in facebook.")
        # quick_replies_list must contains at least one string
        elif len(quick_replies_list) <= 0:
            raise Exception(
                "Quick replies response must contain at least on text string.")
        else:
            # quick replies list to store the quick replie text
            quick_replies = []
            for quick_reply in quick_replies_list:
                # append to the list
                quick_replies.append(
                    str(quick_reply)
                )

            # return the response JSON
            return {
                "quickReplies": {
                    "title": str(title),
                    "quickReplies": quick_replies
                },
                "platform": self.platform
            }

    def image_response(self, url):
        # check url
        if url == "":
            raise Exception("URL in the image response is required.")
        else:
            # return the JSON response
            return {
                "image": {
                    "imageUri": str(url)
                },
                "platform": self.platform
            }

    def card_response(self, title, buttons):
        buttons_json = []
        for button in buttons:
            buttons_json.append(
                {
                    "text": str(button[0]),
                    "postback": str(button[1])
                }
            )

        return {
            "card": {
                "title": str(title),
                "buttons": buttons_json
            },
            "platform": self.platform
        }


# dialogflow fulfillment response
class fulfillment_response():

    def __init__(self):
        pass

    # fulfillment text builder
    # @param fulfillmentText = string
    def fulfillment_text(self, fulfillmentText):
        if fulfillmentText == "":
            raise Exception("Fulfillment text should not be empty.")
        else:
            return {
                "fulfillment_text": str(fulfillmentText)
            }

    # fulfillment messages builder
    # @param response_objects (AOG response, FB response, Telegram response)
    def fulfillment_messages(self, response_objects):
        if len(response_objects) <= 0:
            raise Exception(
                "Response objects must contain at least one response object.")
        else:
            return {
                "fulfillment_messages": response_objects
            }

    # dialogflow output contexts
    # @param session = dialogflow session id
    # @param contexts = context name (string)
    def output_contexts(self, session, contexts):
        contexts_json = []
        for context in contexts:
            contexts_json.append({
                "name": session + "/contexts/" + context[0],
                "lifespanCount": context[1],
                "parameters": context[2]
            })

        # return the output context json
        return {
            "output_contexts": contexts_json
        }

    # dialogflow followup event JSON
    # @param name = event name
    # @param parameters = key value pair of parameters to be passed
    def followup_event_input(self, name, parameters):
        return {
            "followup_event_input": {
                "name": str(name),
                "parameters": parameters
            }
        }

    # main response with fulfillment text and fulfillment messages
    # @param fulfillment_text = fulfillment_text JSON
    # @param fulfillment_messages = fulfillment_messages JSON
    # @param output_contexts = output_contexts JSON
    # @param followup_event_input = followup_event_input JSON
    def main_response(self, fulfillment_text, fulfillment_messages=None, output_contexts=None, followup_event_input=None):
        if followup_event_input is not None:
            if output_contexts is not None:
                if fulfillment_messages is not None:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "fulfillmentMessages": fulfillment_messages['fulfillment_messages'],
                        "outputContexts": output_contexts['output_contexts'],
                        "followupEventInput": followup_event_input['followup_event_input']
                    }
                else:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "outputContexts": output_contexts['output_contexts'],
                        "followupEventInput": followup_event_input['followup_event_input']
                    }
            else:
                if fulfillment_messages is not None:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "fulfillmentMessages": fulfillment_messages['fulfillment_messages'],
                        "followupEventInput": followup_event_input['followup_event_input']
                    }
                else:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "followupEventInput": followup_event_input['followup_event_input']
                    }
        else:
            if output_contexts is not None:
                if fulfillment_messages is not None:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "fulfillmentMessages": fulfillment_messages['fulfillment_messages'],
                        "outputContexts": output_contexts['output_contexts']
                    }
                else:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "outputContexts": output_contexts['output_contexts']
                    }
            else:
                if fulfillment_messages is not None:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text'],
                        "fulfillmentMessages": fulfillment_messages['fulfillment_messages']
                    }
                else:
                    response = {
                        "fulfillmentText": fulfillment_text['fulfillment_text']
                    }

        # return the main dialogflow response
        return response
