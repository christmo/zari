from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

Base = declarative_base()


class Carrito(Base):
    __tablename__ = 'carrito'

    id_car = Column(Integer, primary_key=True)
    usuario = Column(Integer)
    total = Column(Numeric)
    estado = Column(String)
    fecha = Column(Date)

    detalles = []
    
#Carrito.detalles = relationship(CarDetalle, backref="carrito")