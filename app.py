import os
import sys

import customtkinter as ctk
from dotenv import load_dotenv
from brand import CREAM, apply_theme

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(os.path.join(APP_DIR, ".env.local"))

if not os.getenv("DATABASE_URL"):
    raise RuntimeError(
        f"No se encontró DATABASE_URL en {os.path.join(APP_DIR, '.env.local')}. "
        "La aplicación no puede iniciar usando SQLite por accidente."
    )

from database.database import Base, engine

from models.product import Product
from models.sale import Sale
from models.sale_detail import SaleDetail
from models.table import Table
from models.order import Order
from models.order_detail import OrderDetail
from models.user import User
from models.customer import Customer
from models.credit_account import CreditAccount
from models.credit_movement import CreditMovement
from models.kitchen_order import KitchenOrder
from models.expense import Expense

from controllers.user_controller import UserController

from views.login_view import LoginView
from views.main_view import MainView


Base.metadata.create_all(bind=engine)
apply_theme()

UserController.crear_admin_por_defecto()

print("Base de datos creada correctamente.")


class App(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.configure(fg_color=CREAM)

        self.title("Sistema Restaurante")
        self.geometry("1200x700")
        self.resizable(True, True)
        self.state("zoomed")

        self.mostrar_login()

    def _fijar_ventana_maximizada(self):
        self.update_idletasks()
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()
        self.geometry(f"{ancho}x{alto}+0+0")
        self.state("zoomed")
        self.update_idletasks()

    def limpiar_ventana(self):

        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()
        self.state("zoomed")

        LoginView(
            self,
            on_success=self.mostrar_main
        )

    def mostrar_main(self, usuario):

        self.limpiar_ventana()
        self.state("zoomed")

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