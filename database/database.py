import os
import sys
import sqlite3
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


def ensure_database_schema():
    db_path = DATABASE_URL.replace("sqlite:///", "", 1)
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    try:
        columnas = [row[1] for row in conn.execute("PRAGMA table_info('sales')").fetchall()]
        if "sales" not in [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
            return

        if "metodo_pago" not in columnas:
            conn.execute("ALTER TABLE sales ADD COLUMN metodo_pago VARCHAR(20) NOT NULL DEFAULT 'Efectivo'")

        if "customer_id" not in columnas:
            conn.execute("ALTER TABLE sales ADD COLUMN customer_id INTEGER")

        conn.commit()
    finally:
        conn.close()


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
ensure_database_schema()