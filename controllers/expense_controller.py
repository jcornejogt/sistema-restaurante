from datetime import datetime, timedelta

from sqlalchemy import func

from database.database import SessionLocal
from models.expense import Expense


class ExpenseController:

    @staticmethod
    def crear(concepto, monto, categoria="General", fecha=None, notas=""):
        concepto = (concepto or "").strip()
        categoria = (categoria or "General").strip() or "General"
        if not concepto:
            raise ValueError("El concepto es obligatorio.")

        try:
            monto = float(monto)
        except (TypeError, ValueError):
            raise ValueError("El monto debe ser numérico.")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        if fecha is None:
            fecha = datetime.now()

        session = SessionLocal()
        try:
            salida = Expense(
                concepto=concepto,
                categoria=categoria,
                monto=monto,
                fecha=fecha,
                notas=(notas or "").strip()
            )
            session.add(salida)
            session.commit()
            session.refresh(salida)
            return salida
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def listar():
        session = SessionLocal()
        try:
            return session.query(Expense).order_by(Expense.fecha.desc()).all()
        finally:
            session.close()

    @staticmethod
    def eliminar(expense_id):
        session = SessionLocal()
        try:
            salida = session.query(Expense).filter(Expense.id == expense_id).first()
            if salida is None:
                raise ValueError("La salida no existe.")
            session.delete(salida)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def reporte_diario(fecha_inicio=None, fecha_fin=None):
        session = SessionLocal()
        try:
            query = session.query(
                func.date(Expense.fecha).label("fecha"),
                func.count(Expense.id).label("cantidad_salidas"),
                func.sum(Expense.monto).label("total_dia")
            )
            if fecha_inicio is not None:
                query = query.filter(func.date(Expense.fecha) >= fecha_inicio)
            if fecha_fin is not None:
                query = query.filter(func.date(Expense.fecha) <= fecha_fin)

            return [
                {
                    "fecha": str(fecha),
                    "cantidad_salidas": int(cantidad or 0),
                    "total_dia": float(total or 0.0)
                }
                for fecha, cantidad, total in query.group_by(
                    func.date(Expense.fecha)
                ).order_by(func.date(Expense.fecha).asc()).all()
            ]
        finally:
            session.close()

    @staticmethod
    def reporte_ultimos_dias(dias=7):
        fin = datetime.now().date()
        inicio = fin - timedelta(days=max(dias - 1, 0))
        return ExpenseController.reporte_diario(inicio, fin)

    @staticmethod
    def reporte_mes_actual():
        hoy = datetime.now().date()
        return ExpenseController.reporte_diario(hoy.replace(day=1), hoy)