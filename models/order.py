from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Order(Base):

    __tablename__ = "orders"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    mesa_id = Column(
        Integer,
        ForeignKey("tables.id"),
        nullable=False
    )


    estado = Column(
        String,
        default="Abierta"
    )


    total = Column(
        Float,
        default=0
    )


    sale_id = Column(
        Integer,
        ForeignKey("sales.id"),
        nullable=True
    )


    mesa = relationship(
        "Table"
    )


    venta = relationship(
        "Sale"
    )