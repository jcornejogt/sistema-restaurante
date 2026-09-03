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
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'restaurante.db')}"
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)


def ensure_database_schema():
    if not DATABASE_URL.startswith("sqlite://"):
        return

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


engine_options = {"echo": False, "pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite://"):
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_options)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
ensure_database_schema()