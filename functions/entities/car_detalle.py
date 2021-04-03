from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class CarDetalle(Base):
    __tablename__ = 'car_detalle'

    id_det = Column(Integer, primary_key=True)
    id_car = Column(Integer)
    id_producto = Column(Integer)
    costo = Column(Numeric)
    fecha = Column(Date)


#CarDetalle.carrito = relationship(Carrito, backref="detalles")