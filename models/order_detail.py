from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class OrderDetail(Base):

    __tablename__ = "order_details"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    producto_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False,
        default=1
    )

    precio = Column(
        Float,
        nullable=False
    )

    subtotal = Column(
        Float,
        nullable=False
    )

    order = relationship("Order")

    producto = relationship("Product")