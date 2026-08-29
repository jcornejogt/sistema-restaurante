from datetime import datetime

from database.database import Base, engine, SessionLocal
from models.order import Order
from models.sale import Sale
from models.table import Table
from controllers.order_controller import OrderController
from controllers.sale_controller import SaleController
from views.tables_view import TablesView


def test_next_table_number_after_existing_tables():
    assert TablesView._next_table_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 11


def test_next_table_number_when_no_tables_exist():
    assert TablesView._next_table_number([]) == 1


def test_closing_empty_open_order_releases_table_without_sale():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(Order).delete()
        db.query(Table).delete()
        db.commit()

        mesa = Table(numero=1, estado="Ocupada")
        db.add(mesa)
        db.commit()
        db.refresh(mesa)

        cuenta = Order(mesa_id=mesa.id, estado="Abierta", total=0)
        db.add(cuenta)
        db.commit()
        db.refresh(cuenta)

        result = OrderController.cerrar_cuenta(cuenta.id)

        db.refresh(mesa)
        db.refresh(cuenta)

        assert result is None
        assert cuenta.estado == "Cerrada"
        assert mesa.estado == "Libre"
    finally:
        db.close()


def test_reporte_diario_agrupa_ventas_por_fecha_y_calcula_total_neto():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(Sale).delete()
        db.commit()

        db.add_all([
            Sale(total=150.00, fecha=datetime(2026, 8, 28, 12, 0, 0)),
            Sale(total=75.50, fecha=datetime(2026, 8, 28, 18, 30, 0)),
            Sale(total=200.00, fecha=datetime(2026, 8, 29, 9, 0, 0)),
        ])
        db.commit()

        reporte = SaleController.reporte_diario()

        assert reporte[0]["fecha"] == "2026-08-28"
        assert reporte[0]["cantidad_ventas"] == 2
        assert reporte[0]["total_dia"] == 225.5

        assert reporte[1]["fecha"] == "2026-08-29"
        assert reporte[1]["cantidad_ventas"] == 1
        assert reporte[1]["total_dia"] == 200.0

        assert sum(item["total_dia"] for item in reporte) == 425.5
    finally:
        db.close()


def test_reporte_por_rango_filtra_ventas_entre_fechas():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(Sale).delete()
        db.commit()

        db.add_all([
            Sale(total=100.00, fecha=datetime(2026, 8, 20, 10, 0, 0)),
            Sale(total=300.00, fecha=datetime(2026, 8, 25, 12, 0, 0)),
            Sale(total=500.00, fecha=datetime(2026, 8, 29, 10, 0, 0)),
        ])
        db.commit()

        reporte = SaleController.reporte_por_rango(
            datetime(2026, 8, 21).date(),
            datetime(2026, 8, 29).date()
        )

        assert len(reporte) == 2
        assert sum(item["total_dia"] for item in reporte) == 800.0
        assert reporte[0]["fecha"] == "2026-08-25"
        assert reporte[1]["fecha"] == "2026-08-29"
    finally:
        db.close()
