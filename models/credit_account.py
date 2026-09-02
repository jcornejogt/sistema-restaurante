from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.database import Base


class CreditAccount(Base):

    __tablename__ = "credit_accounts"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)

    saldo = Column(Float, default=0.0, nullable=False)

    estado = Column(String(30), default="Abierta", nullable=False)

    descripcion = Column(String(200), nullable=True)

    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Customer", backref="cuentas")
