import datetime


class Orden:
    carrito = 0
    tarjeta = "4547"
    total = 0
    direccion = ''
    entrega = None

    def fecha_formateada(self):
        fecha = self.entrega + datetime.timedelta(days=5)
        return fecha.strftime('%Y-%m-%d')
