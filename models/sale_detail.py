from sqlalchemy import Column, Integer, Float, ForeignKey

from sqlalchemy.orm import relationship

from database.database import Base


class SaleDetail(Base):

    __tablename__ = "sale_details"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    sale_id = Column(
        Integer,
        ForeignKey("sales.id"),
        nullable=False
    )


    producto_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )


    cantidad = Column(
        Integer,
        nullable=False
    )


    precio = Column(
        Float,
        nullable=False
    )


    subtotal = Column(
        Float,
        nullable=False
    )


    venta = relationship(
        "Sale",
        back_populates="detalles"
    )