
class Usuario:
    nombre = ''
    apellido = ''
    talla_calzado = ''
    talla_pantalon = ''
    talla_polera = ''
    __genero = 0

    def __init__(self, username):
        self.username = username

    def genero(self, genero):
        if "hombre" == genero or genero == 1 or "M" == genero:
            self.__genero = 1
        if "mujer" == genero or genero == 2 or "F" == genero:
            self.__genero = 2
        if "niño" == genero or genero == 4 or "NM" == genero:
            self.__genero = 4
        if "niña" == genero or genero == 5 or "NF" == genero:
            self.__genero = 5

    def get_genero(self):
        return self.__genero
