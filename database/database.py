import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Ejecutándose como .exe (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Ejecutándose como script normal
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'restaurante.db')}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()