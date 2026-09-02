from datetime import datetime

from controllers.expense_controller import ExpenseController
from database.database import Base, SessionLocal, engine
from models.expense import Expense


def test_registrar_reportar_y_eliminar_salida():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(Expense).delete()
        db.commit()

        salida = ExpenseController.crear(
            "Compra de gas",
            350,
            "Servicios",
            fecha=datetime(2026, 8, 29, 10, 0),
            notas="Cilindro de cocina"
        )
        ExpenseController.crear(
            "Compra de hielo",
            150,
            "Insumos",
            fecha=datetime(2026, 8, 29, 12, 0)
        )

        reporte = ExpenseController.reporte_diario(
            datetime(2026, 8, 29).date(),
            datetime(2026, 8, 29).date()
        )

        assert salida.id > 0
        assert reporte == [{
            "fecha": "2026-08-29",
            "cantidad_salidas": 2,
            "total_dia": 500.0
        }]

        ExpenseController.eliminar(salida.id)
        assert all(item.id != salida.id for item in ExpenseController.listar())
    finally:
        db.close()
