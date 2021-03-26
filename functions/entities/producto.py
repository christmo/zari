class Producto:
    precio = 0
    image = ''
    gender = ''
    descripcion = ''

    def __init__(self, nombre, talla, color, tipo):
        self.nombre = nombre
        self.talla = self.convertir_talla(talla)
        self.color = color
        self.tipo = tipo # 1 es pantalones

    def convertir_talla(self, talla):
        """
            TODO: Crear funcion que convierta las tallas desde Numero a Letra,
            para buscar en la base de datos como Texto
        """
        #if talla not in ('L','M','S','XS','XL','XXS', 'XXL'):
        return talla

    def toCard(self):
        card = {}
        card["title"] = self.nombre
        card["subtitle"] = f"{self.descripcion} - {self.precio}"
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