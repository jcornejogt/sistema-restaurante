import customtkinter as ctk

from database.database import Base, engine

from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.table import Table
from models.order import Order
from models.order_detail import OrderDetail
from models.user import User

from controllers.user_controller import UserController

from views.login_view import LoginView
from views.main_view import MainView


Base.metadata.create_all(bind=engine)

UserController.crear_admin_por_defecto()

print("Base de datos creada correctamente.")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Sistema Restaurante")

        self.geometry("1200x700")

        self.resizable(False, False)

        self.mostrar_login()

    def limpiar_ventana(self):

        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        LoginView(
            self,
            on_success=self.mostrar_main
        )

    def mostrar_main(self, usuario):

        self.limpiar_ventana()

        vista = MainView(
            self,
            usuario_actual=usuario,
            cerrar_sesion_callback=self.mostrar_login
        )

        vista.pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":

    app = App()

    app.mainloop()