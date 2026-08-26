import customtkinter as ctk

from controllers.product_controller import ProductController


class DashboardView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.crear_dashboard()

    def crear_dashboard(self):

        titulo = ctk.CTkLabel(
            self,
            text="🏠 Dashboard",
            font=("Arial", 30, "bold")
        )

        titulo.pack(pady=(20, 10))

        subtitulo = ctk.CTkLabel(
            self,
            text="Bienvenido al Sistema Restaurante",
            font=("Arial", 18)
        )

        subtitulo.pack(pady=(0, 20))

        # Contenedor de tarjetas
        tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        tarjetas.pack(fill="x", padx=20)

        # Tarjeta Productos
        self.card_productos = self.crear_tarjeta(
            tarjetas,
            "🍔 Productos",
            str(len(ProductController.listar()))
        )

        self.card_productos.pack(side="left", padx=10)

        # Tarjeta Ventas
        self.crear_tarjeta(
            tarjetas,
            "🛒 Ventas Hoy",
            "0"
        ).pack(side="left", padx=10)

        # Tarjeta Clientes
        self.crear_tarjeta(
            tarjetas,
            "👥 Clientes",
            "0"
        ).pack(side="left", padx=10)

    def crear_tarjeta(self, master, titulo, valor):

        card = ctk.CTkFrame(
            master,
            width=220,
            height=120,
            corner_radius=15
        )

        card.pack_propagate(False)

        lbl_titulo = ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 18, "bold")
        )

        lbl_titulo.pack(pady=(15, 5))

        lbl_valor = ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 36, "bold")
        )

        lbl_valor.pack()

        return card