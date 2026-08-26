
from sqlalchemy import Column, Integer, String

from database.database import Base


class Table(Base):

    __tablename__ = "tables"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    numero = Column(
        Integer,
        nullable=False
    )


    estado = Column(
        String,
        default="Libre"
    )