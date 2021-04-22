from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

Base = declarative_base()


class DBUsuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    telegram = Column(String)
    estado = Column(String)
    talla_calzado = Column(Integer)
    talla_pantalon = Column(String)
    talla_polera = Column(String)
    genero = Column(String)
    direccion = Column(String)
    tarjeta = Column(String)
    fecha_nacimiento = Column(Date)
