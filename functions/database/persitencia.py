from entities.tarjeta import Tarjeta
from entities.db_usuario import DBUsuario
from entities.producto import Producto
from entities.usuario import Usuario
from entities.car_detalle import CarDetalle
from database import conexion as pgsql
from sqlalchemy.orm import sessionmaker
from entities.carrito import Carrito
from sqlalchemy import and_
from random import randint
import datetime


def save_shopping_car(user: Usuario, producto: Producto) -> Carrito:
    # pylint: disable=maybe-no-member
    engine = pgsql.init_connection_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    car = session.query(Carrito).filter(
        and_(Carrito.usuario == user.get_id(), Carrito.estado == 'ACTIVO')
    ).first()

    if car == None:
        car = Carrito(usuario=user.get_id(), total=0,
                      estado='ACTIVO', fecha=date)
        session.add(car)
        car = session.query(Carrito).filter(
            and_(Carrito.usuario == user.get_id(), Carrito.estado == 'ACTIVO')
        ).first()
        print(f"car created  {car.id_car}")
    print(f"encontrado  {car.id_car}")

    detalle = CarDetalle(id_car=car.id_car, id_producto=producto.codigo,
                         costo=producto.costo, fecha=date)
    session.add(detalle)
    detalles = session.query(CarDetalle).filter_by(id_car=car.id_car).all()
    suma = sum(float(det.costo) for det in detalles)
    print(f"suma:  {suma}")
    car.total = suma
    session.add(car)
    session.commit()

    car.detalles = detalles

    return car


def save_usuario(user: DBUsuario):
    # pylint: disable=maybe-no-member
    engine = pgsql.init_connection_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    user_found = session.query(DBUsuario).filter(
        and_(DBUsuario.telegram == user.telegram)
    ).first()
    if user_found != None:
        print(
            f'usuario encontrado solo actualizar datos {user_found.id_usuario}')
        user.id_usuario = user_found.id_usuario
        session.merge(user)
    else:
        session.add(user)
    user = session.query(DBUsuario).filter(
        and_(DBUsuario.telegram == user.telegram)
    ).first()
    session.commit()
    print(f'usuario guardado se devuelve: {user.id_usuario}')
    return user


def save_tarjeta_usuario(user: Usuario, tarjeta_numero):
    # pylint: disable=maybe-no-member
    engine = pgsql.init_connection_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    tarjeta = Tarjeta()
    tarjeta.numero = tarjeta_numero
    tarjeta.id_usuario = user.get_id()
    tarjeta.marca = __marca_tarjeta_generador()
    session.add(tarjeta)
    session.commit()


def __marca_tarjeta_generador():
    marca = {
        0: "Visa 🔵",
        1: "Mastercard 🔴"
    }
    random = randint(0, 1)
    return marca[random]
