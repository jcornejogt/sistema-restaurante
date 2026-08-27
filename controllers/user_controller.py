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

    @staticmethod
    def obtener_por_id(user_id):

        db = SessionLocal()

        try:

            return db.query(User).filter(
                User.id == user_id
            ).first()

        finally:

            db.close()

    @staticmethod
    def contar_admins():

        db = SessionLocal()

        try:

            return db.query(User).filter(
                User.rol == "Admin"
            ).count()

        finally:

            db.close()

    @staticmethod
    def actualizar(user_id, nombre, usuario, rol, password=None):

        db = SessionLocal()

        try:

            user = db.query(User).filter(
                User.id == user_id
            ).first()

            if user is None:
                raise Exception("El usuario no existe.")

            duplicado = db.query(User).filter(
                User.usuario == usuario,
                User.id != user_id
            ).first()

            if duplicado:
                raise Exception("Ese nombre de usuario ya existe.")

            # Si se le está bajando el rol de Admin a otra cosa,
            # verificar que no sea el último Admin del sistema
            if user.rol == "Admin" and rol != "Admin":

                admins = db.query(User).filter(
                    User.rol == "Admin"
                ).count()

                if admins <= 1:
                    raise Exception(
                        "No se puede quitar el rol de Admin: "
                        "es el único administrador del sistema."
                    )

            user.nombre = nombre
            user.usuario = usuario
            user.rol = rol

            if password:
                user.password_hash = UserController._hash(password)

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    @staticmethod
    def eliminar(user_id, usuario_actual_id):

        db = SessionLocal()

        try:

            if user_id == usuario_actual_id:
                raise Exception(
                    "No puedes eliminar tu propio usuario mientras "
                    "tienes la sesión iniciada."
                )

            user = db.query(User).filter(
                User.id == user_id
            ).first()

            if user is None:
                raise Exception("El usuario no existe.")

            if user.rol == "Admin":

                admins = db.query(User).filter(
                    User.rol == "Admin"
                ).count()

                if admins <= 1:
                    raise Exception(
                        "No se puede eliminar: es el único "
                        "administrador del sistema."
                    )

            db.delete(user)
            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()