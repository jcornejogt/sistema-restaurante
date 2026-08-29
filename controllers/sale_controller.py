from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from database.database import SessionLocal
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.product import Product


class SaleController:

    @staticmethod
    def listar():

        session = SessionLocal()

        try:
            return session.query(Sale).order_by(Sale.fecha.desc()).all()
        finally:
            session.close()

    @staticmethod
    def resumen_hoy():

        from datetime import datetime, time

        inicio = datetime.combine(datetime.now().date(), time.min)
        session = SessionLocal()

        try:
            ventas = session.query(Sale).filter(Sale.fecha >= inicio).all()
            return {
                "cantidad": len(ventas),
                "total": sum(venta.total for venta in ventas)
            }
        finally:
            session.close()

    @staticmethod
    def reporte_diario(fecha_inicio=None, fecha_fin=None):
        """
        Devuelve un resumen agrupado por fecha para mostrar totales por día.
        Si se envían fechas, filtra el rango indicado.
        """

        session = SessionLocal()

        try:
            query = session.query(
                func.date(Sale.fecha).label("fecha"),
                func.count(Sale.id).label("cantidad_ventas"),
                func.sum(Sale.total).label("total_dia")
            )

            if fecha_inicio is not None:
                query = query.filter(func.date(Sale.fecha) >= fecha_inicio)

            if fecha_fin is not None:
                query = query.filter(func.date(Sale.fecha) <= fecha_fin)

            filas = (
                query.group_by(func.date(Sale.fecha))
                .order_by(func.date(Sale.fecha).asc())
                .all()
            )

            resultado = []
            for fecha, cantidad, total_dia in filas:
                resultado.append({
                    "fecha": str(fecha),
                    "cantidad_ventas": int(cantidad or 0),
                    "total_dia": float(total_dia or 0.0)
                })

            return resultado

        finally:
            session.close()

    @staticmethod
    def reporte_por_rango(fecha_inicio, fecha_fin):
        if fecha_inicio is None and fecha_fin is None:
            return SaleController.reporte_diario()

        if fecha_inicio is None:
            fecha_inicio = fecha_fin

        if fecha_fin is None:
            fecha_fin = fecha_inicio

        return SaleController.reporte_diario(fecha_inicio, fecha_fin)

    @staticmethod
    def reporte_ultimos_dias(dias=7):
        fecha_fin = datetime.now().date()
        fecha_inicio = fecha_fin - timedelta(days=max(dias - 1, 0))
        return SaleController.reporte_por_rango(fecha_inicio, fecha_fin)

    @staticmethod
    def reporte_mes_actual():
        hoy = datetime.now().date()
        fecha_inicio = hoy.replace(day=1)
        return SaleController.reporte_por_rango(fecha_inicio, hoy)

    @staticmethod
    def cobrar(pedido):

        session = SessionLocal()

        try:

            total = 0

            for item in pedido.values():

                producto = session.query(Product).filter_by(
                    id=item["producto"].id
                ).first()

                if producto is None:
                    raise Exception("Producto no encontrado.")

                if producto.stock < item["cantidad"]:
                    raise Exception(
                        f"No hay suficiente stock de '{producto.nombre}'."
                    )

                total += producto.precio * item["cantidad"]

            venta = Sale(total=total)
            session.add(venta)
            session.flush()

            for item in pedido.values():

                producto = session.query(Product).filter_by(
                    id=item["producto"].id
                ).first()

                detalle = SaleDetail(
                    sale_id=venta.id,
                    producto_id=producto.id,
                    cantidad=item["cantidad"],
                    precio=producto.precio,
                    subtotal=producto.precio * item["cantidad"]
                )

                session.add(detalle)

                producto.stock -= item["cantidad"]

            session.commit()

            return venta.id

        except Exception:

            session.rollback()
            raise

        finally:

            session.close()

    @staticmethod
    def obtener_venta(venta_id):
        """
        Devuelve un diccionario con los datos completos de una venta
        (fecha, total, y sus items con nombre de producto), listo
        para armar un recibo. None si la venta no existe.
        """

        session = SessionLocal()

        try:

            venta = session.query(Sale).filter(
                Sale.id == venta_id
            ).first()

            if venta is None:
                return None

            filas = (
                session.query(SaleDetail, Product.nombre)
                .join(Product, Product.id == SaleDetail.producto_id)
                .filter(SaleDetail.sale_id == venta_id)
                .all()
            )

            items = []

            for detalle, nombre_producto in filas:

                items.append({
                    "producto_nombre": nombre_producto,
                    "cantidad": detalle.cantidad,
                    "precio": detalle.precio,
                    "subtotal": detalle.subtotal
                })

            return {
                "id": venta.id,
                "fecha": venta.fecha,
                "total": venta.total,
                "items": items
            }

        finally:

            session.close()