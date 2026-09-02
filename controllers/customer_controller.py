from database.database import SessionLocal
from models.customer import Customer
from models.credit_account import CreditAccount
from models.credit_movement import CreditMovement


class CustomerController:

    @staticmethod
    def _agregar_credito_db(db, cliente_id, monto, descripcion=""):
        if monto is None or float(monto) <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        cliente = db.query(Customer).filter(Customer.id == cliente_id).first()
        if cliente is None:
            raise ValueError("El cliente no existe.")

        cuenta = (
            db.query(CreditAccount)
            .filter(CreditAccount.customer_id == cliente_id, CreditAccount.estado == "Abierta")
            .order_by(CreditAccount.id.desc())
            .first()
        )

        if cuenta is None:
            cuenta = CreditAccount(
                customer_id=cliente_id,
                saldo=0.0,
                estado="Abierta",
                descripcion=descripcion or "Cuenta de crédito"
            )
            db.add(cuenta)
            db.flush()

        cuenta.saldo += float(monto)

        movimiento = CreditMovement(
            account_id=cuenta.id,
            tipo="Credito",
            monto=float(monto),
            descripcion=descripcion or "Crédito registrado"
        )
        db.add(movimiento)
        db.flush()
        return cuenta

    @staticmethod
    def crear(nombre, telefono="", documento="", email="", direccion=""):
        db = SessionLocal()

        try:
            if not nombre or not nombre.strip():
                raise ValueError("El nombre del cliente es obligatorio.")

            cliente = Customer(
                nombre=nombre.strip(),
                telefono=telefono.strip() if telefono else "",
                documento=documento.strip() if documento else "",
                email=email.strip() if email else "",
                direccion=direccion.strip() if direccion else ""
            )
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return cliente
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def listar():
        db = SessionLocal()
        try:
            return db.query(Customer).order_by(Customer.nombre.asc()).all()
        finally:
            db.close()

    @staticmethod
    def obtener_por_id(cliente_id):
        db = SessionLocal()
        try:
            return db.query(Customer).filter(Customer.id == cliente_id).first()
        finally:
            db.close()

    @staticmethod
    def listar_cuentas_por_cliente(cliente_id):
        db = SessionLocal()
        try:
            return (
                db.query(CreditAccount)
                .filter(CreditAccount.customer_id == cliente_id)
                .order_by(CreditAccount.id.asc())
                .all()
            )
        finally:
            db.close()

    @staticmethod
    def obtener_saldo_cliente(cliente_id):
        db = SessionLocal()
        try:
            total = (
                db.query(CreditAccount)
                .filter(CreditAccount.customer_id == cliente_id)
                .with_entities(CreditAccount.saldo)
                .all()
            )
            return sum(float(saldo[0] or 0.0) for saldo in total)
        finally:
            db.close()

    @staticmethod
    def agregar_credito(cliente_id, monto, descripcion=""):
        db = SessionLocal()
        try:
            cuenta = CustomerController._agregar_credito_db(db, cliente_id, monto, descripcion)
            db.commit()
            db.refresh(cuenta)
            return cuenta
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def registrar_pago(cuenta_id, monto, descripcion=""):
        if monto is None or float(monto) <= 0:
            raise ValueError("El monto del pago debe ser mayor que cero.")

        db = SessionLocal()
        try:
            cuenta = db.query(CreditAccount).filter(CreditAccount.id == cuenta_id).first()
            if cuenta is None:
                raise ValueError("La cuenta no existe.")

            pago = float(monto)
            if cuenta.saldo <= 0:
                cuenta.saldo = 0.0
            else:
                cuenta.saldo = max(0.0, cuenta.saldo - pago)

            movimiento = CreditMovement(
                account_id=cuenta.id,
                tipo="Pago",
                monto=pago,
                descripcion=descripcion or "Abono registrado"
            )
            db.add(movimiento)
            db.commit()
            db.refresh(movimiento)
            db.refresh(cuenta)
            return movimiento
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def listar_deudores():
        db = SessionLocal()
        try:
            cuentas = (
                db.query(CreditAccount)
                .filter(CreditAccount.saldo > 0)
                .all()
            )
            clientes = []
            for cuenta in cuentas:
                cliente = db.query(Customer).filter(Customer.id == cuenta.customer_id).first()
                if cliente and cliente not in clientes:
                    clientes.append(cliente)
            return sorted(clientes, key=lambda c: c.nombre.lower())
        finally:
            db.close()
