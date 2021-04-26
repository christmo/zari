from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

Base = declarative_base()


class Tarjeta(Base):
    __tablename__ = 'tarjetas'

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    marca = Column(String)
    numero = Column(String)
