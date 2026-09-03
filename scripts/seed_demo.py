from datetime import datetime
from pathlib import Path
import sys

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
load_dotenv(ROOT_DIR / ".env.local")

from database.database import Base, SessionLocal, engine
from models.credit_account import CreditAccount
from models.credit_movement import CreditMovement
from models.customer import Customer
from models.expense import Expense
from models.kitchen_order import KitchenOrder
from models.order import Order
from models.order_detail import OrderDetail
from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.table import Table
from models.user import User
from controllers.user_controller import UserController


def get_or_create(session, model, filters, values):
    instance = session.query(model).filter_by(**filters).first()
    if instance is None:
        instance = model(**filters, **values)
        session.add(instance)
        session.flush()
    return instance


def seed_demo_data():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        UserController.crear_admin_por_defecto()

        customer = get_or_create(
            session,
            Customer,
            {"email": "demo@restaurante.local"},
            {
                "nombre": "Cliente Demo",
                "telefono": "3000000000",
                "documento": "DEMO-001",
                "direccion": "Calle Principal 123",
            },
        )

        products = {
            product.nombre: product
            for product in [
                get_or_create(
                    session,
                    Product,
                    {"nombre": "Hamburguesa Demo"},
                    {"precio": 18000.0, "stock": 25},
                ),
                get_or_create(
                    session,
                    Product,
                    {"nombre": "Limonada Demo"},
                    {"precio": 7000.0, "stock": 40},
                ),
                get_or_create(
                    session,
                    Product,
                    {"nombre": "Brownie Demo"},
                    {"precio": 9000.0, "stock": 18},
                ),
            ]
        }

        for number in (1, 2, 3, 4, 5):
            get_or_create(
                session,
                Table,
                {"numero": number},
                {"estado": "Libre"},
            )

        expense = get_or_create(
            session,
            Expense,
            {"concepto": "Compra demo de insumos"},
            {
                "categoria": "Insumos",
                "monto": 85000.0,
                "fecha": datetime(2026, 9, 1, 9, 0),
                "notas": "Registro inicial de prueba",
            },
        )

        account = get_or_create(
            session,
            CreditAccount,
            {"customer_id": customer.id},
            {
                "saldo": 12000.0,
                "estado": "Abierta",
                "descripcion": "Cuenta demo",
            },
        )
        get_or_create(
            session,
            CreditMovement,
            {"account_id": account.id, "tipo": "Credito", "monto": 12000.0},
            {"descripcion": "Consumo demo"},
        )

        sale = session.query(Sale).filter_by(total=43000.0, customer_id=customer.id).first()
        if sale is None:
            sale = Sale(
                total=43000.0,
                metodo_pago="Efectivo",
                customer_id=customer.id,
                fecha=datetime(2026, 9, 1, 13, 30),
            )
            session.add(sale)
            session.flush()
            session.add_all(
                [
                    SaleDetail(
                        sale_id=sale.id,
                        producto_id=products["Hamburguesa Demo"].id,
                        cantidad=2,
                        precio=18000.0,
                        subtotal=36000.0,
                    ),
                    SaleDetail(
                        sale_id=sale.id,
                        producto_id=products["Limonada Demo"].id,
                        cantidad=1,
                        precio=7000.0,
                        subtotal=7000.0,
                    ),
                ]
            )
            session.add(KitchenOrder(sale_id=sale.id, estado="Entregada"))

        table = session.query(Table).filter_by(numero=1).first()
        order = session.query(Order).filter_by(mesa_id=table.id, estado="Abierta").first()
        if order is None:
            order = Order(mesa_id=table.id, estado="Abierta", total=16000.0)
            session.add(order)
            session.flush()
            session.add(
                OrderDetail(
                    order_id=order.id,
                    producto_id=products["Brownie Demo"].id,
                    cantidad=1,
                    precio=9000.0,
                    subtotal=9000.0,
                )
            )
            session.add(
                OrderDetail(
                    order_id=order.id,
                    producto_id=products["Limonada Demo"].id,
                    cantidad=1,
                    precio=7000.0,
                    subtotal=7000.0,
                )
            )
            table.estado = "Ocupada"

        session.commit()
        print("Esquema creado y datos demo disponibles en Neon.")
        print(f"Clientes: {session.query(Customer).count()}")
        print(f"Productos: {session.query(Product).count()}")
        print(f"Ventas: {session.query(Sale).count()}")
        print(f"Mesas: {session.query(Table).count()}")
        print(f"Gastos: {session.query(Expense).count()}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_demo_data()
