
from entities.db_usuario import DBUsuario


class Usuario:
    __nombre = ''
    __apellido = ''
    __talla_calzado = ''
    __talla_pantalon = ''
    __talla_polera = ''
    __genero = 0
    __id = 0

    def __init__(self, username):
        self.__username = username

    def __call__(self):
        print("username {self.__username}, nombre {self.__nombre},  \
            apellido {self.__apellido}, talla_calzado {self.__talla_calzado},  \
            talla_pantalon {self.__talla_pantalon}, talla_polera {self.__talla_polera},  \
            genero {self.__genero}")

    def genero(self, genero):
        if genero != None:
            if "hombre" == genero or genero == 1 or "M" == genero:
                self.__genero = 1
            if "mujer" == genero or genero == 2 or "F" == genero:
                self.__genero = 2
            if "niño" == genero or genero == 4 or "NM" == genero:
                self.__genero = 4
            if "niña" == genero or genero == 5 or "NF" == genero:
                self.__genero = 5
        else:
            self.__genero = 0

    def nombre(self, nombre):
        self.__nombre = nombre

    def apellido(self, apellido):
        self.__apellido = apellido

    def talla_calzado(self, talla_calzado):
        self.__talla_calzado = talla_calzado

    def talla_pantalon(self, talla_pantalon):
        self.__talla_pantalon = talla_pantalon

    def talla_polera(self, talla_polera):
        self.__talla_polera = talla_polera

    def id(self, id_usuario):
        self.__id = id_usuario

    def get_genero(self):
        return self.__genero

    def get_genero_letra(self):
        if self.__genero == 1:
            return "M"
        if self.__genero == 2:
            return "F"
        if self.__genero == 4:
            return "NM"
        if self.__genero == 5:
            return "NF"
        return None

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def get_talla_calzado(self):
        return self.__talla_calzado

    def get_talla_pantalon(self):
        return self.__talla_pantalon

    def get_talla_polera(self):
        return self.__talla_polera

    def get_username(self):
        return self.__username

    def get_id(self):
        return self.__id

    def is_full(self):
        return len(self.__username) > 0 and len(self.__nombre) > 0 \
            and len(self.__apellido) > 0 and len(self.__talla_calzado) > 0 \
            and len(self.__talla_pantalon) > 0 and len(self.__talla_polera) > 0 \
            and self.__genero > 0 and self.__id > 0

    def __repr__(self):
        return f"username: {self.__username} nombre: {self.__nombre} \
            apellido: {self.__apellido} talla_calzado: {self.__talla_calzado} \
            talla_pantalon: {self.__talla_pantalon} talla_polera: {self.__talla_polera} \
            genero: {self.__genero} id: {self.__id}"

    @classmethod
    def parse_usuario(cls, user: DBUsuario):
        usuario = cls(user.telegram)
        usuario.id(user.id_usuario)
        usuario.nombre(user.nombre)
        usuario.apellido(user.apellido)
        usuario.talla_pantalon(user.talla_pantalon)
        usuario.talla_polera(user.talla_polera)
        usuario.talla_calzado(user.talla_calzado)
        usuario.genero(user.genero)
        return usuario
