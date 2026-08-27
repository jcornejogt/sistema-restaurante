from database.database import SessionLocal

from models.sale import Sale
from models.sale_detail import SaleDetail
from models.product import Product


class SalesModel:

    @staticmethod
    def guardar(total, productos):

        db = SessionLocal()

        try:

            # Crear venta principal
            venta = Sale(
                total=total
            )

            db.add(venta)

            # Obtener ID generado
            db.flush()


            # Guardar detalle de cada producto
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


            db.commit()

            return True


        except Exception as e:

            db.rollback()

            print("Error guardando venta:", e)

            raise e


        finally:

            db.close()