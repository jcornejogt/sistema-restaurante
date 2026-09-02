from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey

from sqlalchemy.orm import relationship

from datetime import datetime

from database.database import Base


class Sale(Base):

    __tablename__ = "sales"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    total = Column(
        Float,
        nullable=False
    )

    metodo_pago = Column(
        String(20),
        nullable=False,
        default="Efectivo"
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True,
        index=True
    )

    fecha = Column(
        DateTime,
        default=datetime.now
    )

    detalles = relationship(
        "SaleDetail",
        back_populates="venta",
        cascade="all, delete"
    )

    cliente = relationship("Customer", backref="ventas")