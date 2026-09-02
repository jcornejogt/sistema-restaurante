from datetime import datetime

from database.database import SessionLocal

from models.sale import Sale
from models.sale_detail import SaleDetail
from models.product import Product
from models.kitchen_order import KitchenOrder
from controllers.customer_controller import CustomerController


class SalesModel:

    @staticmethod
    def guardar(total, productos, metodo_pago="Efectivo", customer_id=None):

        db = SessionLocal()

        try:
            metodo = (metodo_pago or "Efectivo").strip().title()
            if metodo not in {"Efectivo", "Tarjeta", "Transferencia", "Credito"}:
                raise ValueError("Método de pago inválido.")

            if metodo == "Credito" and customer_id is None:
                raise ValueError("Debe seleccionar un cliente para ventas a crédito.")

            venta = Sale(
                total=total,
                metodo_pago=metodo,
                customer_id=customer_id
            )

            db.add(venta)
            db.flush()

            for producto in productos:

                registro = db.query(Product).filter(
                    Product.id == producto["id"]
                ).first()

                if registro is None:
                    raise Exception("Producto no encontrado.")

                if registro.stock < producto["cantidad"]:
                    raise Exception(
                        f"No hay suficiente stock de '{registro.nombre}'."
                    )

                detalle = SaleDetail(
                    sale_id=venta.id,
                    producto_id=producto["id"],
                    cantidad=producto["cantidad"],
                    precio=producto["precio"],
                    subtotal=producto["subtotal"]
                )

                db.add(detalle)
                registro.stock -= producto["cantidad"]

            if metodo == "Credito":
                CustomerController._agregar_credito_db(db, customer_id, total, f"Venta #{venta.id}")

            comanda = db.query(KitchenOrder).filter(
                KitchenOrder.sale_id == venta.id
            ).first()
            if comanda is None:
                comanda = KitchenOrder(sale_id=venta.id)
                db.add(comanda)
            else:
                comanda.fecha_creacion = datetime.now()
                comanda.estado = "Pendiente"

            db.commit()
            return venta.id

        except Exception as e:
            db.rollback()
            print("Error guardando venta:", e)
            raise e
        finally:
            db.close()