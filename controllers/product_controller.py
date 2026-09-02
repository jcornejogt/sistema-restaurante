from sqlalchemy import func

from database.database import SessionLocal
from models.product import Product
from models.sale_detail import SaleDetail


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
    def listar_disponibles(filtro=""):

        session = SessionLocal()

        try:
            query = (
                session.query(Product)
                .outerjoin(SaleDetail, SaleDetail.producto_id == Product.id)
                .filter(Product.stock > 0)
            )

            if filtro:
                query = query.filter(Product.nombre.ilike(f"%{filtro}%"))

            productos = (
                query
                .group_by(Product.id, Product.nombre, Product.precio, Product.stock)
                .order_by(
                    func.coalesce(func.sum(SaleDetail.cantidad), 0).desc(),
                    Product.nombre.asc()
                )
                .all()
            )

            return productos
        finally:
            session.close()

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