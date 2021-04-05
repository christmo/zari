from entities.orden import Orden
from entities.usuario import Usuario
from entities.carrito import Carrito
from database import conexion as pgsql


def limpiar_carrito(car_id: int):
    return __cambiar_estado_carrito('INACTIVO', car_id)


def __cambiar_estado_carrito(estado, car_id):
    if estado != None and car_id != None:
        sql = f"update carrito set estado='{estado}' where id_car = {car_id}"
        db = pgsql.init_connection_engine()
        with db.connect() as conn:
            conn.execute(sql)
            return True
    else:
        print(f"Faltan parametros {estado} - {car_id}")
        return False


def pagar_carrito(user: Usuario) -> Orden:
    sql = f"""
select c.id_car, u.tarjeta, c.total, u.direccion, CURRENT_DATE, c.id_car
from usuario u, carrito c
where u.id_usuario = c.usuario
and c.estado = 'ACTIVO'
and u.id_usuario = {user.get_id()}
    """
    db = pgsql.init_connection_engine()
    with db.connect() as conn:
        result = conn.execute(sql).fetchone()
        if result != None:
            orden = Orden()
            orden.carrito = result[0]
            orden.tarjeta = result[1]
            orden.total = result[2]
            orden.direccion = result[3]
            orden.entrega = result[4]
            update = __cambiar_estado_carrito('PAGADO', result[5])
            if update:
                return orden

        return None


#def persistir_usuario_inicio(user: Usuario):
#    sql = f"""
#insert into usuario(nombre, apellido, telegram, estado, talla_pantalon, talla_polera, talla_calzado, genero)
#values('{user.get_nombre()}','{user.get_apellido()}','{user.get_username()}','ACTIVO',
#'{user.get_talla_pantalon()}','{user.get_talla_polera()}',{user.talla_calzado},'{user.get_genero_letra()}')
#    """
#    db = pgsql.init_connection_engine()
#    with db.connect() as conn:
#        conn.execute(sql)
