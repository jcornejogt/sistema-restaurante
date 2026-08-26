import hashlib

from database.database import SessionLocal
from models.user import User


class UserController:

    @staticmethod
    def _hash(password):

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def crear_admin_por_defecto():
        """
        Si no existe ningún usuario en el sistema, crea un Admin
        con credenciales por defecto para poder entrar la primera vez.
        """

        db = SessionLocal()

        try:

            existe = db.query(User).count()

            if existe > 0:
                return

            admin = User(
                nombre="Administrador",
                usuario="admin",
                password_hash=UserController._hash("admin123"),
                rol="Admin"
            )

            db.add(admin)
            db.commit()

        finally:

            db.close()

    @staticmethod
    def autenticar(usuario, password):
        """
        Devuelve un diccionario con los datos del usuario si las
        credenciales son correctas, o None si no lo son.
        """

        db = SessionLocal()

        try:

            user = db.query(User).filter(
                User.usuario == usuario
            ).first()

            if user is None:
                return None

            if user.password_hash != UserController._hash(password):
                return None

            return {
                "id": user.id,
                "nombre": user.nombre,
                "usuario": user.usuario,
                "rol": user.rol
            }

        finally:

            db.close()

    @staticmethod
    def crear(nombre, usuario, password, rol):

        db = SessionLocal()

        try:

            existe = db.query(User).filter(
                User.usuario == usuario
            ).first()

            if existe:
                raise Exception("Ese nombre de usuario ya existe.")

            nuevo = User(
                nombre=nombre,
                usuario=usuario,
                password_hash=UserController._hash(password),
                rol=rol
            )

            db.add(nuevo)
            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def listar():

        db = SessionLocal()

        try:

            return db.query(User).order_by(User.nombre).all()

        finally:

            db.close()