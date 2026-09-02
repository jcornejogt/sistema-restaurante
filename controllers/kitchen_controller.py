from datetime import datetime

from database.database import SessionLocal
from models.kitchen_order import KitchenOrder
from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail


class KitchenController:

    @staticmethod
    def listar_comandas():
        session = SessionLocal()

        try:
            comandas = session.query(KitchenOrder).join(
                Sale, Sale.id == KitchenOrder.sale_id
            ).order_by(KitchenOrder.fecha_creacion.asc()).all()

            resultado = []
            for comanda in comandas:
                detalles = session.query(SaleDetail, Product.nombre).join(
                    Product, Product.id == SaleDetail.producto_id
                ).filter(SaleDetail.sale_id == comanda.sale_id).all()

                resultado.append({
                    "id": comanda.id,
                    "venta_id": comanda.sale_id,
                    "fecha_creacion": comanda.fecha_creacion,
                    "estado": comanda.estado,
                    "items": [
                        {"nombre": nombre, "cantidad": detalle.cantidad}
                        for detalle, nombre in detalles
                    ]
                })

            return resultado
        finally:
            session.close()

    @staticmethod
    def cambiar_estado(comanda_id, estado):
        estados_validos = {"Pendiente", "Preparando", "Lista", "Entregada"}
        if estado not in estados_validos:
            raise ValueError("Estado de comanda inválido.")

        session = SessionLocal()
        try:
            comanda = session.query(KitchenOrder).filter(
                KitchenOrder.id == comanda_id
            ).first()
            if comanda is None:
                raise ValueError("La comanda no existe.")

            comanda.estado = estado
            session.commit()
        finally:
            session.close()

    @staticmethod
    def minutos_transcurridos(fecha_creacion, ahora=None):
        ahora = ahora or datetime.now()
        return max((ahora - fecha_creacion).total_seconds() / 60, 0)

    @staticmethod
    def esta_vencida(fecha_creacion, ahora=None):
        return KitchenController.minutos_transcurridos(fecha_creacion, ahora) > 15