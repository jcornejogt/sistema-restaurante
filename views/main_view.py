import customtkinter as ctk
from datetime import datetime

from views.dashboard_view import DashboardView
from views.products_view import ProductsView
from views.sales_view import SalesView
from views.tables_view import TablesView
from views.order_view import OrderView
from views.users_view import UsersView
from views.inventory_view import InventoryView
from views.reports_view import ReportsView
from brand import CREAM, GOLD, GOLD_HOVER, MUTED, NAVY, NAVY_LIGHT, WHITE, logo_image


class MainView(ctk.CTkFrame):

    def __init__(self, master, usuario_actual, cerrar_sesion_callback=None):
        super().__init__(master)

        self.master = master
        self.usuario_actual = usuario_actual
        self.cerrar_sesion_callback = cerrar_sesion_callback

        self.pack(
            fill="both",
            expand=True
        )

        self.crear_menu()
        self.crear_contenedor()
        self.crear_barra_estado()

        self.dashboard()

        self.actualizar_hora()


    def crear_menu(self):

        self.menu = ctk.CTkFrame(
            self,
            width=220,
            fg_color=NAVY
        )

        self.menu.pack(
            side="left",
            fill="y"
        )


        titulo = ctk.CTkLabel(
            self.menu,
            text="",
            image=logo_image(92, 92),
            font=("Arial", 22, "bold")
        )

        titulo.pack(
            pady=(22, 5)
        )

        ctk.CTkLabel(
            self.menu,
            text="LA BAJONA",
            text_color=GOLD,
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 22))


        rol_actual = self.usuario_actual["rol"]

        # (texto, comando, lista de roles permitidos; None = todos los roles)
        botones = [

            ("🏠 Dashboard", self.dashboard, None),

            ("🪑 Mesas", self.mesas, None),

            ("🍔 Productos", self.mostrar_productos, ["Admin"]),

            ("🛒 Ventas", self.ventas, None),

            ("📦 Inventario", self.inventario, ["Admin"]),

            ("📊 Reportes", self.reportes, ["Admin"]),

            ("👤 Usuarios", self.usuarios, ["Admin"])

        ]


        for texto, comando, roles_permitidos in botones:

            if roles_permitidos is not None and rol_actual not in roles_permitidos:
                continue

            ctk.CTkButton(
                self.menu,
                text=texto,
                width=180,
                height=40,
                fg_color=NAVY_LIGHT,
                hover_color=GOLD_HOVER,
                text_color=WHITE,
                command=comando
            ).pack(
                pady=8,
                padx=20
            )


    def crear_contenedor(self):

        self.contenido = ctk.CTkFrame(self)

        self.contenido.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        self.contenido.configure(fg_color=CREAM)


    def crear_barra_estado(self):

        self.estado = ctk.CTkFrame(
            self,
            height=35,
            fg_color=NAVY
        )

        self.estado.pack(
            side="bottom",
            fill="x"
        )


        self.usuario_label = ctk.CTkLabel(
            self.estado,
            text=f"👤 {self.usuario_actual['nombre']} ({self.usuario_actual['rol']})",
            text_color=MUTED
        )

        self.usuario_label.pack(
            side="left",
            padx=20
        )


        self.hora_label = ctk.CTkLabel(
            self.estado,
            text="",
            text_color=MUTED
        )

        self.hora_label.pack(
            side="right",
            padx=20
        )


        ctk.CTkButton(
            self.estado,
            text="Cerrar sesión",
            width=110,
            height=24,
            fg_color=GOLD,
            hover_color=GOLD_HOVER,
            text_color=NAVY,
            command=self.cerrar_sesion
        ).pack(
            side="right",
            padx=10
        )


    def cerrar_sesion(self):

        if self.cerrar_sesion_callback:
            self.cerrar_sesion_callback()


    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()



    def dashboard(self):

        self.limpiar_contenido()

        vista = DashboardView(
            self.contenido
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def mesas(self):

        self.limpiar_contenido()

        vista = TablesView(
            self.contenido,
            abrir_cuenta_callback=self.abrir_orden
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def abrir_orden(self, mesa_id):

        self.limpiar_contenido()

        vista = OrderView(
            self.contenido,
            mesa_id=mesa_id,
            volver_callback=self.mesas
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def mostrar_productos(self):

        self.limpiar_contenido()

        vista = ProductsView(
            self.contenido
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def ventas(self):

        self.limpiar_contenido()

        vista = SalesView(
            self.contenido
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def inventario(self):

        self.limpiar_contenido()

        vista = InventoryView(self.contenido)
        vista.pack(fill="both", expand=True)



    def reportes(self):

        self.limpiar_contenido()

        vista = ReportsView(self.contenido)
        vista.pack(fill="both", expand=True)



    def usuarios(self):

        self.limpiar_contenido()

        vista = UsersView(
            self.contenido,
            usuario_actual=self.usuario_actual
        )

        vista.pack(
            fill="both",
            expand=True
        )



    def actualizar_hora(self):

        ahora = datetime.now().strftime(
            "%d/%m/%Y  %H:%M:%S"
        )

        self.hora_label.configure(
            text=ahora
        )

        self.after(
            1000,
            self.actualizar_hora
        )