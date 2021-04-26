import requests


class Sentimiento:

    def __init__(self, frase):
        self.frase = frase

    def __get_sentiment_rate(self):
        url = "https://us-central1-poc-df-01-299301.cloudfunctions.net/analizar_sentimiento"
        headers = {'Content-Type': 'application/json'}
        data = {
            "frase": self.frase
        }
        response = requests.post(url, json=data, headers=headers)
        json = response.json()
        return json

    def clasificar(self):
        response = self.__get_sentiment_rate()
        status = response["status"]
        text = "neutro"
        if status == "success":
            data = float(response["data"])
            if (data > 0):
                text = "positivo"
            elif (data < 0):
                text = "negativo"
        return text
