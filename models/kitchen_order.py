from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base


class KitchenOrder(Base):

    __tablename__ = "kitchen_orders"

    id = Column(Integer, primary_key=True, index=True)

    sale_id = Column(
        Integer,
        ForeignKey("sales.id"),
        nullable=False,
        unique=True,
        index=True
    )

    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)

    estado = Column(String(20), nullable=False, default="Pendiente")

    venta = relationship("Sale")