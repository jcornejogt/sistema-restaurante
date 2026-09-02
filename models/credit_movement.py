from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime

from database.database import Base


class CreditMovement(Base):

    __tablename__ = "credit_movements"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(Integer, ForeignKey("credit_accounts.id"), nullable=False, index=True)

    tipo = Column(String(20), nullable=False)  # Credito, Pago

    monto = Column(Float, nullable=False)

    descripcion = Column(String(200), nullable=True)

    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
