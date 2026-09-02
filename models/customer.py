from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from database.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String(120), nullable=False)

    telefono = Column(String(50), nullable=True)

    documento = Column(String(80), nullable=True)

    email = Column(String(120), nullable=True)

    direccion = Column(String(200), nullable=True)

    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
