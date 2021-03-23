class Producto:
    precio = 0
    image = ''
    
    def __init__(self, nombre, talla, color):
        self.nombre = nombre
        self.talla = talla
        self.color = color

    def toCard(self):
        card = {}
        card["title"] = self.nombre
        card["subtitle"] = "self.nombre"
        card["imageUri"] = self.image

        buttons = []
        boton = {}
        boton["text"] = "Añadir al carrito"
        buttons.append(boton)
        card["buttons"] = buttons
        
        wrapper = {}
        wrapper["card"] = card
        wrapper["platform"] = "TELEGRAM"
        return wrapper