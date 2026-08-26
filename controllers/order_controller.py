from sqlalchemy.orm import joinedload

from database.database import SessionLocal

from models.order import Order
from models.order_detail import OrderDetail
from models.product import Product
from models.table import Table
from models.sale import Sale
from models.sale_detail import SaleDetail


class OrderController:

    @staticmethod
    def abrir_cuenta(mesa_id):

        db = SessionLocal()

        try:

            mesa = db.query(Table).filter(
                Table.id == mesa_id
            ).first()

            if mesa is None:
                return None

            cuenta = db.query(Order).filter(
                Order.mesa_id == mesa_id,
                Order.estado == "Abierta"
            ).first()

            if cuenta:
                return cuenta

            cuenta = Order(
                mesa_id=mesa_id,
                estado="Abierta",
                total=0
            )

            db.add(cuenta)

            mesa.estado = "Ocupada"

            db.commit()

            db.refresh(cuenta)

            return cuenta

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def obtener_cuenta_abierta(mesa_id):

        db = SessionLocal()

        try:

            return db.query(Order).filter(
                Order.mesa_id == mesa_id,
                Order.estado == "Abierta"
            ).first()

        finally:

            db.close()

    @staticmethod
    def agregar_producto(order_id, producto_id, cantidad=1):

        db = SessionLocal()

        try:

            producto = db.query(Product).filter(
                Product.id == producto_id
            ).first()

            if producto is None:
                return

            detalle = db.query(OrderDetail).filter(
                OrderDetail.order_id == order_id,
                OrderDetail.producto_id == producto_id
            ).first()

            if detalle:

                detalle.cantidad += cantidad
                detalle.subtotal = detalle.cantidad * detalle.precio

            else:

                detalle = OrderDetail(
                    order_id=order_id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio=producto.precio,
                    subtotal=producto.precio * cantidad
                )

                db.add(detalle)

            total = 0

            detalles = db.query(OrderDetail).filter(
                OrderDetail.order_id == order_id
            ).all()

            for item in detalles:
                total += item.subtotal

            cuenta = db.query(Order).filter(
                Order.id == order_id
            ).first()

            cuenta.total = total

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def obtener_detalle(order_id):

        db = SessionLocal()

        try:

            detalles = (
                db.query(OrderDetail)
                .options(joinedload(OrderDetail.producto))
                .filter(OrderDetail.order_id == order_id)
                .all()
            )

            resultado = []

            for d in detalles:

                resultado.append({
                    "id": d.id,
                    "producto_id": d.producto_id,
                    "producto_nombre": d.producto.nombre,
                    "cantidad": d.cantidad,
                    "precio": d.precio,
                    "subtotal": d.subtotal
                })

            return resultado

        finally:

            db.close()

    @staticmethod
    def eliminar_producto(detalle_id):

        db = SessionLocal()

        try:

            detalle = db.query(OrderDetail).filter(
                OrderDetail.id == detalle_id
            ).first()

            if detalle is None:
                return

            order_id = detalle.order_id

            db.delete(detalle)

            db.commit()

            total = 0

            detalles = db.query(OrderDetail).filter(
                OrderDetail.order_id == order_id
            ).all()

            for item in detalles:
                total += item.subtotal

            cuenta = db.query(Order).filter(
                Order.id == order_id
            ).first()

            cuenta.total = total

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def cerrar_cuenta(order_id):
        """
        Cierra la cuenta de una mesa, generando una venta real:
        valida stock, crea Sale + SaleDetail, descuenta inventario,
        marca la orden como Cerrada y libera la mesa.
        Lanza una excepción con mensaje claro si algo falla
        (cuenta vacía, ya cerrada, o sin stock suficiente).
        """

        db = SessionLocal()

        try:

            cuenta = db.query(Order).filter(
                Order.id == order_id
            ).first()

            if cuenta is None:
                raise Exception("La cuenta no existe.")

            if cuenta.estado != "Abierta":
                raise Exception("Esta cuenta ya fue cerrada.")

            detalles = db.query(OrderDetail).filter(
                OrderDetail.order_id == order_id
            ).all()

            if len(detalles) == 0:
                raise Exception(
                    "No se puede cerrar una cuenta sin productos."
                )

            # Validar stock de TODOS los productos antes de tocar nada
            for item in detalles:

                producto = db.query(Product).filter(
                    Product.id == item.producto_id
                ).first()

                if producto is None:
                    raise Exception(
                        "Uno de los productos de la cuenta ya no existe."
                    )

                if producto.stock < item.cantidad:
                    raise Exception(
                        f"No hay suficiente stock de '{producto.nombre}'. "
                        f"Disponible: {producto.stock}, requerido: {item.cantidad}."
                    )

            # Crear la venta
            venta = Sale(total=cuenta.total)

            db.add(venta)
            db.flush()

            # Crear el detalle de venta y descontar stock
            for item in detalles:

                producto = db.query(Product).filter(
                    Product.id == item.producto_id
                ).first()

                detalle_venta = SaleDetail(
                    sale_id=venta.id,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio=item.precio,
                    subtotal=item.subtotal
                )

                db.add(detalle_venta)

                producto.stock -= item.cantidad

            mesa = db.query(Table).filter(
                Table.id == cuenta.mesa_id
            ).first()

            cuenta.estado = "Cerrada"
            cuenta.sale_id = venta.id

            if mesa:
                mesa.estado = "Libre"

            db.commit()

            return venta.id

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()