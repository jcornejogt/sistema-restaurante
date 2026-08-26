from sqlalchemy import Column, Integer, String

from database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    usuario = Column(
        String(50),
        nullable=False,
        unique=True
    )

    password_hash = Column(
        String(64),
        nullable=False
    )

    rol = Column(
        String(20),
        nullable=False,
        default="Mesero"
    )