from database.database import SessionLocal
from models.product import Product


class ProductController:

    @staticmethod
    def guardar(nombre, precio, stock):

        session = SessionLocal()

        producto = Product(
            nombre=nombre,
            precio=precio,
            stock=stock
        )

        session.add(producto)
        session.commit()
        session.close()

    @staticmethod
    def listar():

        session = SessionLocal()

        productos = (
            session.query(Product)
            .order_by(Product.nombre)
            .all()
        )

        session.close()

        return productos

    @staticmethod
    def listar_disponibles():

        session = SessionLocal()

        productos = (
            session.query(Product)
            .filter(Product.stock > 0)
            .order_by(Product.nombre)
            .all()
        )

        session.close()

        return productos

    @staticmethod
    def obtener_por_id(id_producto):

        session = SessionLocal()

        producto = (
            session.query(Product)
            .filter_by(id=id_producto)
            .first()
        )

        session.close()

        return producto

    @staticmethod
    def actualizar(id_producto, nombre, precio, stock):

        session = SessionLocal()

        producto = (
            session.query(Product)
            .filter_by(id=id_producto)
            .first()
        )

        if producto:

            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock

            session.commit()

        session.close()

    @staticmethod
    def actualizar_stock(id_producto, stock):

        session = SessionLocal()

        producto = (
            session.query(Product)
            .filter_by(id=id_producto)
            .first()
        )

        if producto:

            producto.stock = stock

            session.commit()

        session.close()

    @staticmethod
    def eliminar(id_producto):

        session = SessionLocal()

        producto = (
            session.query(Product)
            .filter_by(id=id_producto)
            .first()
        )

        if producto:

            session.delete(producto)
            session.commit()

        session.close()