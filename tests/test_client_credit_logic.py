from database.database import Base, engine, SessionLocal
from controllers.customer_controller import CustomerController
from models.customer import Customer
from models.credit_account import CreditAccount
from models.product import Product
from database.sales_model import SalesModel


def test_crear_cliente_y_generar_credito_basico():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(CreditAccount).delete()
        db.query(Customer).delete()
        db.commit()

        cliente = CustomerController.crear(
            nombre="Ana Gómez",
            telefono="555-1001",
            documento="001-010101-0001A",
            email="ana@test.com",
            direccion="Calle 1"
        )

        cuenta = CustomerController.agregar_credito(
            cliente_id=cliente.id,
            monto=500.0,
            descripcion="Consumo del día"
        )

        assert cliente.id > 0
        assert cuenta.saldo == 500.0
        assert cuenta.estado == "Abierta"

        pago = CustomerController.registrar_pago(
            cuenta_id=cuenta.id,
            monto=200.0,
            descripcion="Abono parcial"
        )

        assert pago.monto == 200.0
        assert cuenta.saldo == 500.0
        assert CustomerController.obtener_saldo_cliente(cliente.id) == 300.0
    finally:
        db.close()


def test_listar_clientes_con_deuda():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(CreditAccount).delete()
        db.query(Customer).delete()
        db.commit()

        cliente1 = CustomerController.crear(
            nombre="Pedro",
            telefono="555-2001",
            documento="001-020202-0002B",
            email="pedro@test.com",
            direccion="Calle 2"
        )
        cliente2 = CustomerController.crear(
            nombre="Luis",
            telefono="555-2002",
            documento="001-020203-0003C",
            email="luis@test.com",
            direccion="Calle 3"
        )

        CustomerController.agregar_credito(cliente1.id, 250.0, "Pedido")
        CustomerController.agregar_credito(cliente2.id, 80.0, "Pedido")
        CustomerController.registrar_pago(
            CustomerController.listar_cuentas_por_cliente(cliente1.id)[0].id,
            50.0,
            "Abono"
        )

        deudores = CustomerController.listar_deudores()
        ids = [c.id for c in deudores]

        assert cliente1.id in ids
        assert cliente2.id in ids
        assert CustomerController.obtener_saldo_cliente(cliente1.id) == 200.0
        assert CustomerController.obtener_saldo_cliente(cliente2.id) == 80.0
    finally:
        db.close()


def test_registra_credito_automatico_al_guardar_venta_a_credito():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        db.query(CreditAccount).delete()
        db.query(Customer).delete()
        db.query(Product).delete()
        db.commit()

        cliente = CustomerController.crear(
            nombre="María López",
            telefono="555-3001",
            documento="001-030303-0003D",
            email="maria@test.com",
            direccion="Calle 5"
        )

        producto = Product(nombre="Pizza", precio=120.0, stock=10)
        db.add(producto)
        db.commit()
        db.refresh(producto)

        venta_id = SalesModel.guardar(
            total=120.0,
            productos=[{
                "id": producto.id,
                "cantidad": 1,
                "precio": producto.precio,
                "subtotal": 120.0,
            }],
            metodo_pago="Credito",
            customer_id=cliente.id,
        )

        assert venta_id > 0
        assert CustomerController.obtener_saldo_cliente(cliente.id) == 120.0
        assert len(CustomerController.listar_cuentas_por_cliente(cliente.id)) == 1
    finally:
        db.close()
