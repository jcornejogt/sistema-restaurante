from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from database.database import Base


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    concepto = Column(String(120), nullable=False)
    categoria = Column(String(60), nullable=False, default="General")
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    notas = Column(String(250), nullable=True)