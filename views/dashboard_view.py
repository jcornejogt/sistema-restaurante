import customtkinter as ctk
from datetime import datetime

from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController
from controllers.kitchen_controller import KitchenController
from controllers.expense_controller import ExpenseController
from brand import CREAM, NAVY, GOLD


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.crear_dashboard()

    def crear_dashboard(self):

        self.configure(fg_color=CREAM)

        titulo = ctk.CTkLabel(
            self,
            text="🏠 Dashboard",
            text_color=NAVY,
            font=("Arial", 32, "bold")
        )

        titulo.pack(pady=(20, 10))

        subtitulo = ctk.CTkLabel(
            self,
            text="Bienvenido al Sistema Restaurante",
            text_color=NAVY,
            font=("Arial", 20)
        )

        subtitulo.pack(pady=(0, 20))

        tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        tarjetas.pack(fill="x", padx=20)
        for columna in range(3):
            tarjetas.grid_columnconfigure(columna, weight=1)

        # Tarjeta Productos
        self.card_productos = self.crear_tarjeta(
            tarjetas,
            "🍔 Productos",
            str(len(ProductController.listar()))
        )

        self.card_productos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Tarjeta Ventas
        resumen = SaleController.resumen_hoy()

        self.card_ventas = self.crear_tarjeta(
            tarjetas,
            "🛒 Ventas Hoy",
            f"{resumen['cantidad']} / C$ {resumen['total']:.2f}",
            width=280,
            height=140
        )
        self.card_ventas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Tarjeta Clientes
        self.card_stock = self.crear_tarjeta(
            tarjetas,
            "📦 Stock bajo",
            str(sum(
                1 for producto in ProductController.listar()
                if producto.stock <= 5
            ))
        )
        self.card_stock.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        comandas = KitchenController.listar_comandas()
        activas = [comanda for comanda in comandas if comanda["estado"] != "Entregada"]
        atrasadas = [
            comanda for comanda in activas
            if KitchenController.esta_vencida(comanda["fecha_creacion"])
        ]

        self.crear_tarjeta(
            tarjetas,
            "🍳 Comandas activas",
            str(len(activas))
        ).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.crear_tarjeta(
            tarjetas,
            "🔴 Comandas atrasadas",
            str(len(atrasadas))
        ).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        gastos_hoy = sum(
            salida.monto for salida in ExpenseController.listar()
            if salida.fecha.date() == datetime.now().date()
        )
        self.crear_tarjeta(
            tarjetas,
            "💸 Salidas Hoy",
            f"C$ {gastos_hoy:.2f}"
        ).grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

    def crear_tarjeta(self, master, titulo, valor, width=220, height=120):

        card = ctk.CTkFrame(
            master,
            width=width,
            height=height,
            corner_radius=15
        )

        card.pack_propagate(False)

        lbl_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 20, "bold")
        )

        lbl_titulo.pack(pady=(15, 5))

        lbl_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 38, "bold")
        )

        lbl_valor.pack()

        return card