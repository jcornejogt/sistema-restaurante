from sqlalchemy.orm import joinedload

from database.database import SessionLocal
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.product import Product


class SaleController:

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