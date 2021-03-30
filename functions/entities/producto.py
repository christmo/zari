class Producto:
    precio = 0
    image = ''
    __genero = 0
    descripcion = ''
    codigo = 0

    def tipo_producto(self, tipo) -> int:
        if "pantalones" == tipo or 1 == tipo:
            return 1
        if "camiseta" == tipo or 2 == tipo:
            return 2
        return 0

    def __init__(self, nombre, talla, color, tipo):
        self.nombre = nombre
        self.talla = self.convertir_talla(talla)
        self.color = color
        self.tipo = self.tipo_producto(tipo)

    def convertir_talla(self, talla):
        """
            TODO: Crear funcion que convierta las tallas desde Numero a Letra,
            para buscar en la base de datos como Texto
        """
        # if talla not in ('L','M','S','XS','XL','XXS', 'XXL'):
        return talla

    def genero(self, genero):
        if "hombre" == genero or genero == 1 or "M" == genero:
            self.__genero = 1
        if "mujer" == genero or genero == 2 or "F" == genero:
            self.__genero = 2
        if "niño" == genero or genero == 4 or "NM" == genero:
            self.__genero = 4
        if "niña" == genero or genero == 5 or "NF" == genero:
            self.__genero = 5
    
    def get_genero(self) -> int:
        return self.__genero

    def toCard(self):
        card = {}
        card["title"] = self.nombre
        card["subtitle"] = f"{self.descripcion} - {self.precio}"
        card["imageUri"] = self.image

        buttons = []
        boton = {}
        boton["text"] = "Agregar al Carrito"
        boton["postback"] = f"Agregar {self.descripcion} {self.codigo} {self.precio}"
        buttons.append(boton)
        card["buttons"] = buttons

        wrapper = {}
        wrapper["card"] = card
        wrapper["platform"] = "TELEGRAM"
        return wrapper
