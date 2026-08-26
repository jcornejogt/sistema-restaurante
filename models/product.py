from sqlalchemy import Column, Integer, String, Float

from database.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(100), nullable=False)

    precio = Column(Float, nullable=False)

    stock = Column(Integer, nullable=False)