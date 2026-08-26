from database.database import SessionLocal

from models.sale import Sale
from models.sale_detail import SaleDetail


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

                detalle = SaleDetail(

                    sale_id=venta.id,

                    producto_id=producto["id"],

                    cantidad=producto["cantidad"],

                    precio=producto["precio"],

                    subtotal=producto["subtotal"]

                )

                db.add(detalle)


            db.commit()

            return True


        except Exception as e:

            db.rollback()

            print("Error guardando venta:", e)

            raise e


        finally:

            db.close()