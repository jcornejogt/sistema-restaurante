from sqlalchemy import Column, Integer, Float, DateTime

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


    fecha = Column(
        DateTime,
        default=datetime.now
    )


    detalles = relationship(
        "SaleDetail",
        back_populates="venta",
        cascade="all, delete"
    )