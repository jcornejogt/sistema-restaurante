import customtkinter as ctk

from brand import CREAM, DANGER, DANGER_HOVER, GOLD, NAVY, SUCCESS, SUCCESS_HOVER, WHITE
from controllers.kitchen_controller import KitchenController


class KitchenView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=CREAM)
        self.after_id = None
        self.crear_vista()
        self.cargar_comandas()

    def crear_vista(self):
        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            encabezado,
            text="Comandas de cocina",
            text_color=NAVY,
            font=("Arial", 30, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            encabezado,
            text="Actualizar",
            width=110,
            command=self.cargar_comandas
        ).pack(side="right")

        self.contenedor = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.contenedor.pack(fill="both", expand=True, padx=15, pady=8)

    def cargar_comandas(self):
        if not self.winfo_exists():
            return

        for widget in self.contenedor.winfo_children():
            widget.destroy()

        comandas = KitchenController.listar_comandas()
        if not comandas:
            ctk.CTkLabel(
                self.contenedor,
                text="No hay comandas pendientes.",
                text_color=NAVY,
                font=("Arial", 20)
            ).pack(pady=50)
        else:
            for indice, comanda in enumerate(comandas):
                self.crear_comanda(comanda, indice)

        self.after_id = self.after(1000, self.cargar_comandas)

    def crear_comanda(self, comanda, indice):
        vencida = KitchenController.esta_vencida(comanda["fecha_creacion"])
        minutos = KitchenController.minutos_transcurridos(comanda["fecha_creacion"])
        segundos = int(minutos * 60) % 60
        horas = int(minutos // 60)
        minutos_entero = int(minutos) % 60
        color = DANGER if vencida else WHITE
        texto_tiempo = f"{horas:02d}:{minutos_entero:02d}:{segundos:02d}"

        ticket = ctk.CTkFrame(
            self.contenedor,
            fg_color=color,
            border_width=2 if vencida else 1,
            border_color=DANGER if vencida else "#D9D2C5",
            corner_radius=6
        )
        ticket.grid(row=indice // 3, column=indice % 3, padx=8, pady=8, sticky="nsew")
        self.contenedor.grid_columnconfigure(indice % 3, weight=1)

        titulo = f"COMANDA #{comanda['id']}  |  VENTA #{comanda['venta_id']}"
        ctk.CTkLabel(ticket, text=titulo, text_color=NAVY, font=("Arial", 17, "bold")).pack(anchor="w", padx=14, pady=(12, 2))
        ctk.CTkLabel(ticket, text=f"Tiempo: {texto_tiempo}", text_color=DANGER if vencida else GOLD, font=("Arial", 22, "bold")).pack(anchor="w", padx=14)
        ctk.CTkLabel(ticket, text="ATENCION: supera 15 minutos" if vencida else "En tiempo", text_color=DANGER if vencida else NAVY).pack(anchor="w", padx=14, pady=(0, 8))

        for item in comanda["items"]:
            ctk.CTkLabel(ticket, text=f"{item['cantidad']} x {item['nombre']}", text_color=NAVY, anchor="w").pack(fill="x", padx=14, pady=1)

        estado = ctk.StringVar(value=comanda["estado"])
        selector = ctk.CTkOptionMenu(ticket, variable=estado, values=["Pendiente", "Preparando", "Lista", "Entregada"], command=lambda valor, cid=comanda["id"]: self.actualizar_estado(cid, valor))
        selector.pack(fill="x", padx=14, pady=(12, 14))

    def actualizar_estado(self, comanda_id, estado):
        KitchenController.cambiar_estado(comanda_id, estado)

    def destruir(self):
        if self.after_id:
            self.after_cancel(self.after_id)